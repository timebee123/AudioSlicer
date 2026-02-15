#!/usr/bin/env python3
import os
import sys
import threading
import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pydub import AudioSegment, silence, utils


class AudioSlicerApp:
    def __init__(self, root):
        self.root = root
        root.title("AudioSlicer V-0.3")
        root.geometry("640x300")

        self.input_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.min_silence_ms = tk.IntVar(value=500)
        self.status_text = tk.StringVar(value="Idle")

        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        # File selection
        ttk.Label(frm, text="Input File:").grid(row=0, column=0, sticky=tk.W)
        self.input_label = ttk.Label(frm, textvariable=self.input_path)
        self.input_label.grid(row=0, column=1, sticky=tk.W, columnspan=3)
        ttk.Button(frm, text="Choose Audio File", command=self.choose_file).grid(row=0, column=4)

        # Output directory
        ttk.Label(frm, text="Output Directory:").grid(row=1, column=0, sticky=tk.W)
        self.output_label = ttk.Label(frm, textvariable=self.output_dir)
        self.output_label.grid(row=1, column=1, sticky=tk.W, columnspan=3)
        ttk.Button(frm, text="Choose Output Dir", command=self.choose_output_dir).grid(row=1, column=4)

        # Silence threshold scale (ms)
        ttk.Label(frm, text="Min silence duration (ms):").grid(row=2, column=0, sticky=tk.W)
        self.scale = ttk.Scale(frm, from_=300, to=1000, orient=tk.HORIZONTAL, command=self._on_scale)
        self.scale.set(self.min_silence_ms.get())
        self.scale.grid(row=2, column=1, columnspan=3, sticky=tk.EW)
        self.scale_value = ttk.Label(frm, textvariable=self.min_silence_ms)
        self.scale_value.grid(row=2, column=4, sticky=tk.W)

        # Start button
        self.start_btn = ttk.Button(frm, text="Start Slicing", command=self.start_slicing)
        self.start_btn.grid(row=3, column=0, pady=12)

        # Progressbar and status
        self.progress = ttk.Progressbar(frm, mode='determinate')
        self.progress.grid(row=3, column=1, columnspan=3, sticky=tk.EW, padx=6)
        self.status = ttk.Label(frm, textvariable=self.status_text)
        self.status.grid(row=3, column=4, sticky=tk.W)

        # Make columns resize nicely
        for i in range(5):
            frm.columnconfigure(i, weight=1 if i in (1,2,3) else 0)

    def _on_scale(self, val):
        try:
            self.min_silence_ms.set(int(float(val)))
        except Exception:
            pass

    def choose_file(self):
        path = filedialog.askopenfilename(filetypes=[("Audio", "*.mp3 *.m4a")])
        if path:
            self.input_path.set(path)

    def choose_output_dir(self):
        d = filedialog.askdirectory()
        if d:
            self.output_dir.set(d)

    def start_slicing(self):
        if not self.input_path.get():
            messagebox.showwarning("No file", "Please select an input audio file.")
            return
        if not self.output_dir.get():
            messagebox.showwarning("No output dir", "Please select an output directory.")
            return

        # Check ffmpeg availability
        if not utils.which("ffmpeg"):
            if not messagebox.askyesno("ffmpeg not found", "ffmpeg not found in PATH. Exporting may fail. Continue?"):
                return

        self.start_btn.config(state=tk.DISABLED)
        self.status_text.set("Preparing...")
        t = threading.Thread(target=self._slice_worker, daemon=True)
        t.start()

    def _slice_worker(self):
        try:
            self.status_text.set("Loading audio...")
            audio = AudioSegment.from_file(self.input_path.get())

            thresh_db = -50  # fixed threshold per spec
            min_silence_len = int(self.min_silence_ms.get())

            self.status_text.set("Detecting silence...")
            silence_ranges = silence.detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=thresh_db)
            # detect_silence returns list of [start_ms, end_ms]

            # Build segments between silence ranges
            segments = []
            prev = 0
            for s, e in silence_ranges:
                # segment is audio[prev:s]
                if s - prev > 10:
                    segments.append((prev, s))
                prev = e
            # last segment
            if len(audio) - prev > 10:
                segments.append((prev, len(audio)))

            # If no silence found, export whole file as single segment
            if not segments:
                segments = [(0, len(audio))]

            total = len(segments)
            self.progress['maximum'] = total
            out_dir = self.output_dir.get()

            for i, (st, ed) in enumerate(segments, start=1):
                seg = audio[st:ed]
                filename = f"{i:03d}.mp3"
                out_path = os.path.join(out_dir, filename)
                self.status_text.set(f"Exporting {filename} ({i}/{total})")
                seg.export(out_path, format="mp3")
                self.progress['value'] = i

            self.status_text.set("Completed")
            messagebox.showinfo("Done", f"Exported {total} segments to:\n{out_dir}")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_text.set("Error")
        finally:
            self.start_btn.config(state=tk.NORMAL)
            self.progress['value'] = 0


def main():
    try:
        root = tk.Tk()
    except RuntimeError as e:
        if "macOS" in str(e) or "version" in str(e).lower():
            print("\n" + "="*60)
            print("GUI ERROR: Tkinter requires a newer macOS version.")
            print("="*60)
            print("\nAlternative: Use the web-based version or command-line mode.")
            print("For now, run your audio files through the slicing logic manually.")
            print("See README.md for headless options.")
            print("="*60 + "\n")
            return 1
        raise

    style = ttk.Style()
    try:
        # Use native platform theme for macOS simple look
        style.theme_use('aqua')
    except Exception:
        pass
    app = AudioSlicerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
