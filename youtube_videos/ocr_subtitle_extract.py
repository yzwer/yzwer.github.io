# -*- coding: utf-8 -*-
"""OCR-based hardcoded subtitle extractor for video files.

Uses ffmpeg to extract frames at regular intervals, crops the subtitle region,
and applies cnocr (Chinese OCR) to recognize text. Outputs SRT subtitle file.
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def get_video_duration(video_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def format_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def deduplicate_subtitles(subtitles):
    if not subtitles:
        return []
    result = [subtitles[0]]
    for sub in subtitles[1:]:
        if sub["text"].strip() != result[-1]["text"].strip():
            result.append(sub)
        else:
            result[-1]["end"] = sub["end"]
    return result


def write_srt(subtitles, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, sub in enumerate(subtitles, 1):
            f.write(f"{i}\n")
            f.write(f"{format_srt_time(sub['start'])} --> {format_srt_time(sub['end'])}\n")
            f.write(f"{sub['text'].strip()}\n\n")


def main():
    parser = argparse.ArgumentParser(description="Extract hardcoded subtitles via OCR")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--output", required=True, help="Output SRT file")
    parser.add_argument("--interval", type=float, default=2.0, help="Frame interval seconds")
    parser.add_argument("--crop-top", type=float, default=0.85)
    parser.add_argument("--crop-bottom", type=float, default=1.0)
    parser.add_argument("--crop-left", type=float, default=0.05)
    parser.add_argument("--crop-right", type=float, default=0.95)
    args = parser.parse_args()

    print("Loading cnocr model...")
    from cnocr import CnOcr
    ocr = CnOcr(rec_model_name="densenet_lite_136-gru")
    print("Model loaded.")

    duration = get_video_duration(args.video)
    print(f"Video duration: {duration:.1f}s")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract frames
        cmd = [
            "ffmpeg", "-i", args.video,
            "-vf", f"fps=1/{args.interval}",
            "-q:v", "2",
            os.path.join(tmpdir, "frame_%06d.png")
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        frames = sorted(Path(tmpdir).glob("frame_*.png"))
        print(f"Extracted {len(frames)} frames at {args.interval}s interval")

        if not frames:
            print("No frames extracted!")
            sys.exit(1)

        # OCR each frame
        subtitles = []
        crop_w = args.crop_right - args.crop_left
        crop_h = args.crop_bottom - args.crop_top
        crop_filter = f"crop=iw*{crop_w}:ih*{crop_h}:iw*{args.crop_left}:ih*{args.crop_top}"

        for i, frame_path in enumerate(frames):
            timestamp = i * args.interval
            cropped_path = os.path.join(tmpdir, f"cropped_{i:06d}.png")
            # Crop subtitle region
            cmd = ["ffmpeg", "-i", str(frame_path), "-vf", crop_filter, "-y", cropped_path]
            subprocess.run(cmd, capture_output=True, text=True)
            # OCR
            try:
                results = ocr.ocr(cropped_path)
                text = " ".join([r["text"] for r in results if r.get("text", "").strip()])
            except Exception as e:
                print(f"  OCR error at {timestamp:.1f}s: {e}")
                text = ""

            if text.strip():
                subtitles.append({"start": timestamp, "end": timestamp + args.interval, "text": text.strip()})
                print(f"  [{format_srt_time(timestamp)}] {text.strip()}")

            if (i + 1) % 50 == 0:
                print(f"  Progress: {i+1}/{len(frames)} frames")

    subtitles = deduplicate_subtitles(subtitles)
    write_srt(subtitles, args.output)
    print(f"\nDone! {len(subtitles)} subtitle entries written to {args.output}")


if __name__ == "__main__":
    main()
