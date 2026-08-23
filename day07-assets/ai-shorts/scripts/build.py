#!/usr/bin/env python3
"""Assemble Flow scene clips + Typecast narration into a finished 9:16 short.

Replaces the manual CapCut pass: trims each scene to its "use" length, pads to
1080x1920, concatenates, lays the narration underneath, and burns in subtitles
timed from words.json.

Subtitle timings come from Typecast's Timestamp TTS, i.e. from the synthesis
that produced this exact audio -- there is no STT step and nothing to hand-sync.

Usage:
  python3 build.py scenes.json out/ --out short.mp4
"""
import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subs  # noqa: E402

W, H = 1080, 1920
FONT_SIZE = 96
MARGIN_V = 320   # keeps captions clear of the Shorts UI at the bottom
FPS = 30


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def normalise_scenes(scenes, workdir):
    """Trim each clip to its 'use' length and letterbox-crop it to 9:16.

    Flow clips are generated a beat longer than they are used, because motion
    degrades near the tail; that surplus is dropped here.
    """
    norm_dir = os.path.join(workdir, "scenes_norm")
    os.makedirs(norm_dir, exist_ok=True)
    out = []
    for i, sc in enumerate(scenes):
        src = sc["file"]
        if not os.path.exists(src):
            sys.exit(f"scene {i+1}: missing {src}")
        have, want = probe(src), float(sc["use"])
        if want > have + 0.05:
            sys.exit(f"scene {i+1} ({src}): asked for {want}s but clip is {have:.2f}s")
        dst = os.path.join(norm_dir, f"{i:02d}.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-i", src, "-t", str(want),
            "-vf", (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                    f"crop={W}:{H},fps={FPS},setsar=1"),
            "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", dst], check=True)
        out.append(dst)
        print(f"  scene {i+1:2d}  {want:>4.1f}s  {os.path.basename(src)}", file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenes", help="JSON list of {file, use}")
    ap.add_argument("workdir", help="dir holding narration.wav + words.json")
    ap.add_argument("--out", default="short.mp4")
    ap.add_argument("--no-subs", action="store_true")
    args = ap.parse_args()

    scenes = json.load(open(args.scenes, encoding="utf-8"))
    narration = os.path.join(args.workdir, "narration.wav")
    words_path = os.path.join(args.workdir, "words.json")
    for p in (narration, words_path):
        if not os.path.exists(p):
            sys.exit(f"missing {p} -- run tts.py first")
    words = json.load(open(words_path, encoding="utf-8"))

    norm = normalise_scenes(scenes, args.workdir)

    listing = os.path.join(args.workdir, "scenes_norm", "concat.txt")
    with open(listing, "w") as f:
        for p in norm:
            f.write(f"file '{os.path.abspath(p)}'\n")
    silent = os.path.join(args.workdir, "video_silent.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", listing, "-c", "copy", silent], check=True)

    vlen, alen = probe(silent), probe(narration)
    print(f"video {vlen:.2f}s / narration {alen:.2f}s", file=sys.stderr)
    # Under a second of drift used to pass silently, and the overlay then
    # froze the last frame to cover it. plan.py makes the numbers exact, so
    # any real gap here means scenes.json was edited by hand and is wrong.
    if abs(vlen - alen) > 0.15:
        sys.exit(f"영상 {vlen:.2f}s / 내레이션 {alen:.2f}s — {abs(vlen-alen):.2f}s 어긋납니다.\n"
                 f"  plan.py 로 scenes.json 을 다시 만드세요:\n"
                 f"    python3 <스킬>/scripts/plan.py {args.workdir} --out {args.scenes}")

    if args.no_subs or not words:
        chain, extra = ["[0:v]null[vout]"], []
    else:
        cues = subs.group_captions(words)
        backend = subs.build_ass if subs.have_libass() else subs.build_png
        print(f"subtitles: {len(cues)} cues via {backend.__name__[6:]}", file=sys.stderr)
        chain, extra = backend(cues, args.workdir, W, H, FONT_SIZE, MARGIN_V)

    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", silent, "-i", narration, *extra,
        "-filter_complex", ";".join(chain),
        "-map", "[vout]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", args.out], check=True)

    print(f"{args.out}  {probe(args.out):.2f}s  {W}x{H}")


if __name__ == "__main__":
    main()
