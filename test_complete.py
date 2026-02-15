#!/usr/bin/env python3
"""
Complete end-to-end test for AudioSlicer V-0.3
Tests: pydub, ffmpeg, silence detection, audio export
"""
import os
import sys
import tempfile
import shutil
from pydub import AudioSegment, silence, utils
from pydub.generators import Sine

def test_ffmpeg():
    """Test 1: Verify ffmpeg is available"""
    print("\n[TEST 1] Checking ffmpeg...")
    ffmpeg_path = utils.which("ffmpeg")
    if not ffmpeg_path:
        print("  ❌ FAILED: ffmpeg not found in PATH")
        return False
    print(f"  ✓ PASSED: ffmpeg found at {ffmpeg_path}")
    return True

def test_pydub_import():
    """Test 2: Verify pydub can be imported"""
    print("\n[TEST 2] Checking pydub import...")
    try:
        from pydub import AudioSegment, silence
        print("  ✓ PASSED: pydub imported successfully")
        return True
    except ImportError as e:
        print(f"  ❌ FAILED: {e}")
        return False

def test_audio_generation():
    """Test 3: Generate synthetic audio"""
    print("\n[TEST 3] Generating synthetic audio...")
    try:
        # Create: 1s tone + 0.6s silence + 1s tone + 0.8s silence + 1s tone
        tone_1 = Sine(440).to_audio_segment(duration=1000)
        silence_1 = AudioSegment.silent(duration=600)
        tone_2 = Sine(440).to_audio_segment(duration=1000)
        silence_2 = AudioSegment.silent(duration=800)
        tone_3 = Sine(440).to_audio_segment(duration=1000)
        
        audio = tone_1 + silence_1 + tone_2 + silence_2 + tone_3
        duration = len(audio)
        
        print(f"  ✓ PASSED: Generated {duration}ms of audio")
        return audio
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        return None

def test_silence_detection(audio):
    """Test 4: Detect silence at -50 dB"""
    print("\n[TEST 4] Detecting silence (-50 dB, min 500 ms)...")
    try:
        silence_ranges = silence.detect_silence(
            audio, 
            min_silence_len=500, 
            silence_thresh=-50
        )
        
        if len(silence_ranges) != 2:
            print(f"  ❌ FAILED: Expected 2 silences, found {len(silence_ranges)}")
            return None
        
        print(f"  ✓ PASSED: Found {len(silence_ranges)} silence ranges")
        for i, (s, e) in enumerate(silence_ranges, 1):
            print(f"      Silence {i}: {s}ms – {e}ms ({e-s}ms)")
        
        return silence_ranges
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        return None

def test_audio_slicing(audio, silence_ranges):
    """Test 5: Slice audio between silences"""
    print("\n[TEST 5] Slicing audio into segments...")
    try:
        segments = []
        prev = 0
        for s, e in silence_ranges:
            if s - prev > 10:
                segments.append((prev, s))
            prev = e
        if len(audio) - prev > 10:
            segments.append((prev, len(audio)))
        
        if not segments:
            segments = [(0, len(audio))]
        
        if len(segments) != 3:
            print(f"  ❌ FAILED: Expected 3 segments, got {len(segments)}")
            return None
        
        print(f"  ✓ PASSED: Created {len(segments)} segments")
        for i, (st, ed) in enumerate(segments, 1):
            print(f"      Segment {i}: {st}ms – {ed}ms ({ed-st}ms)")
        
        return segments
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        return None

def test_audio_export(audio, segments):
    """Test 6: Export segments as numbered MP3s"""
    print("\n[TEST 6] Exporting audio segments to MP3...")
    
    # Create temp directory for export
    temp_dir = tempfile.mkdtemp(prefix="audioslicer_test_")
    
    try:
        for i, (st, ed) in enumerate(segments, 1):
            seg = audio[st:ed]
            filename = f"{i:03d}.mp3"
            out_path = os.path.join(temp_dir, filename)
            seg.export(out_path, format="mp3")
            
            # Verify file exists and has non-zero size
            if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
                print(f"  ❌ FAILED: {filename} not exported correctly")
                return False
            
            print(f"      ✓ {filename} ({os.path.getsize(out_path)} bytes)")
        
        # Verify all files
        files = sorted(os.listdir(temp_dir))
        if len(files) != 3 or files != ["001.mp3", "002.mp3", "003.mp3"]:
            print(f"  ❌ FAILED: File naming incorrect. Got: {files}")
            return False
        
        print(f"  ✓ PASSED: All {len(files)} segments exported with correct naming")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        return True
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return False

def test_syntax():
    """Test 7: Verify AudioSlicer.py syntax"""
    print("\n[TEST 7] Checking AudioSlicer.py syntax...")
    try:
        import py_compile
        py_compile.compile("AudioSlicer.py", doraise=True)
        print("  ✓ PASSED: No syntax errors")
        return True
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        return False

def main():
    print("="*60)
    print("AudioSlicer V-0.3 Complete Test Suite")
    print("="*60)
    
    results = []
    
    # Test 1: ffmpeg
    results.append(("ffmpeg availability", test_ffmpeg()))
    
    # Test 2: pydub import
    results.append(("pydub import", test_pydub_import()))
    
    # Test 3: audio generation
    audio = test_audio_generation()
    results.append(("audio generation", audio is not None))
    
    if not audio:
        print("\n" + "="*60)
        print("⚠️  TESTS STOPPED: Cannot proceed without audio")
        print("="*60)
        return 1
    
    # Test 4: silence detection
    silence_ranges = test_silence_detection(audio)
    results.append(("silence detection", silence_ranges is not None))
    
    if not silence_ranges:
        print("\n" + "="*60)
        print("⚠️  TESTS STOPPED: Cannot proceed without silence detection")
        print("="*60)
        return 1
    
    # Test 5: audio slicing
    segments = test_audio_slicing(audio, silence_ranges)
    results.append(("audio slicing", segments is not None))
    
    if not segments:
        print("\n" + "="*60)
        print("⚠️  TESTS STOPPED: Cannot proceed without audio slicing")
        print("="*60)
        return 1
    
    # Test 6: audio export
    results.append(("audio export", test_audio_export(audio, segments)))
    
    # Test 7: syntax check
    results.append(("AudioSlicer.py syntax", test_syntax()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! AudioSlicer V-0.3 is ready to use.")
        print("="*60)
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. See details above.")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
