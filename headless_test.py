#!/usr/bin/env python3
"""
Headless test for AudioSlicer slicing logic.
Synthesizes audio with silences, detects them, and exports segments.
"""
import os
import sys
from pydub import AudioSegment, silence, utils
from pydub.generators import Sine

def main():
    print("=== AudioSlicer Headless Test ===\n")

    # Check ffmpeg
    if not utils.which("ffmpeg"):
        print("WARNING: ffmpeg not found in PATH. Export may fail.")
        return 1

    # Create test output directory
    test_out = "test_output"
    if not os.path.exists(test_out):
        os.makedirs(test_out)
    print(f"Output directory: {test_out}\n")

    # Generate synthetic audio: 1s tone + 1s silence + 1s tone + 1s silence + 1s tone
    print("Generating synthetic audio...")
    duration_ms = 1000

    # Create segments: tone, silence, tone, silence, tone
    tone_1 = Sine(440).to_audio_segment(duration=duration_ms)
    silence_1 = AudioSegment.silent(duration=600)  # 600ms silence (> 500ms threshold)
    tone_2 = Sine(440).to_audio_segment(duration=duration_ms)
    silence_2 = AudioSegment.silent(duration=800)  # 800ms silence (> 500ms threshold)
    tone_3 = Sine(440).to_audio_segment(duration=duration_ms)

    audio = tone_1 + silence_1 + tone_2 + silence_2 + tone_3
    total_duration = len(audio)
    print(f"Total audio duration: {total_duration}ms")

    # Save input for reference
    input_path = os.path.join(test_out, "input_test.mp3")
    audio.export(input_path, format="mp3")
    print(f"Saved input audio to: {input_path}\n")

    # Detect silence at -50 dB, min duration 500ms
    print("Detecting silence (-50 dB, min 500ms)...")
    thresh_db = -50
    min_silence_len = 500

    silence_ranges = silence.detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=thresh_db)
    print(f"Found {len(silence_ranges)} silence range(s):")
    for i, (s, e) in enumerate(silence_ranges, start=1):
        print(f"  Silence {i}: {s}ms – {e}ms (duration: {e-s}ms)")
    print()

    # Build segments between silences
    segments = []
    prev = 0
    for s, e in silence_ranges:
        if s - prev > 10:  # skip very short segments
            segments.append((prev, s))
        prev = e
    if len(audio) - prev > 10:
        segments.append((prev, len(audio)))

    # If no silence found, export whole file as single segment
    if not segments:
        print("No silence detected; exporting entire audio as one segment.")
        segments = [(0, len(audio))]

    print(f"Extracted {len(segments)} audio segment(s):\n")

    # Export segments
    for i, (st, ed) in enumerate(segments, start=1):
        seg = audio[st:ed]
        filename = f"{i:03d}.mp3"
        out_path = os.path.join(test_out, filename)
        print(f"  [{i}/{len(segments)}] Exporting {filename} ({ed-st}ms)")
        seg.export(out_path, format="mp3")

    print(f"\n✓ Test completed. Files saved to: {test_out}/")
    return 0

if __name__ == "__main__":
    sys.exit(main())
