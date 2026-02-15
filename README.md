# AudioSlicer V-0.3

A small Tkinter desktop app to split long audio files into shorter clips by detecting silent gaps.

## Requirements

- Python 3.8+
- ffmpeg present in PATH (required by pydub for importing/exporting some formats)
- Install Python deps:

```bash
pip install -r requirements.txt
```

## Installation & Setup

### macOS with Homebrew

```bash
# Install ffmpeg
brew install ffmpeg

# Install Python 3.11 with Tkinter support
brew install python@3.11
brew install python-tk@3.11

# Install Python dependencies
pip3.11 install pydub
```

### Verify Setup

```bash
python3 - <<'PY'
from pydub import utils
print('ffmpeg path:', utils.which('ffmpeg') or 'not found')
PY
```

## Usage

### GUI Mode (Recommended)

```bash
python3.11 "AudioSlicer.py"
```

1. Choose an input `.mp3` or `.m4a` file.
2. Choose an output directory.
3. Adjust the minimum silence duration slider (300–1000 ms).
4. Click `Start Slicing`.

Output files are named `001.mp3`, `002.mp3`, ... and saved in the chosen output directory.

### Headless/Test Mode

If you encounter GUI issues or want to test the slicing logic without the GUI:

```bash
python3 headless_test.py
```

This will create synthetic audio with silences and export three 1-second segments to `test_output/`.

## Notes

- The app uses a fixed silence level of **-50 dB** as specified.
- If `ffmpeg` is not in PATH, export may fail — install ffmpeg and add it to PATH.
- Minimum silence duration ranges from 300 ms to 1000 ms (adjustable via slider).
- All output files are exported in MP3 format.

## Troubleshooting

**"command not found: ffmpeg"**
- Install ffmpeg: `brew install ffmpeg`
- Or ensure ffmpeg is in your PATH

**GUI won't start (macOS version error)**
- The Tkinter version may require a newer macOS SDK. As a workaround:
  - Upgrade macOS to the latest version, or
  - Process audio files in headless mode using the `headless_test.py` script as a template

**"No module named 'pydub'"**
- Install dependencies: `pip install -r requirements.txt`

