#!/usr/bin/env python3
"""Preflight the clips folder against scenes.json.

Flow generation is the one manual step, so the question "what still needs
making?" comes up repeatedly. This answers it all at once instead of failing
on the first missing file the way build.py would.

Usage:
  python3 check.py scenes.json
"""
import argparse
import json
import os
import subprocess
import sys


def probe(path):
    """Return (duration, width, height) or None if unreadable."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True)
    if r.returncode != 0:
        return None
    vals = r.stdout.split()
    if len(vals) < 3:
        return None
    return float(vals[2]), int(vals[0]), int(vals[1])


def contact_sheet(scenes, out):
    """One image with a frame from every clip, side by side.

    Flow defaults to 16:9 and generates each clip with no memory of the last,
    so the two failures that matter -- a landscape clip, and twin shots that do
    not match -- are both visible at a glance and invisible in a table of
    numbers. Credits are spent by this point; seeing it now still beats seeing
    it in the finished video.
    """
    tiles = []
    for i, sc in enumerate(scenes):
        if not os.path.exists(sc["file"]):
            continue
        t = f"/tmp/.cs{i:02d}.png"
        r = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", str(float(sc["use"]) / 2),
             "-i", sc["file"], "-frames:v", "1",
             # Fixed box so hstack works whatever the source aspect is, and a
             # landscape clip shows up letterboxed instead of breaking the stack.
             "-vf", ("scale=240:360:force_original_aspect_ratio=decrease,"
                     "pad=240:360:(ow-iw)/2:(oh-ih)/2:color=0x15181A"),
             t], capture_output=True)
        if r.returncode == 0:
            tiles.append(t)
    if not tiles:
        return None
    args = []
    for t in tiles:
        args += ["-i", t]
    n = len(tiles)
    try:
        subprocess.run(["ffmpeg", "-y", "-v", "error", *args,
                        "-filter_complex", f"hstack=inputs={n}" if n > 1 else "null",
                        out], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        return None          # the sheet is a convenience; never fail the check
    finally:
        for t in tiles:
            try:
                os.remove(t)
            except OSError:
                pass
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenes")
    ap.add_argument("--sheet", default="clips-미리보기.png",
                    help="컷마다 한 프레임씩 뽑아 이어 붙인 확인용 이미지")
    args = ap.parse_args()
    scenes = json.load(open(args.scenes, encoding="utf-8"))

    ready, missing, short, landscape = 0, [], [], []
    print(f"{'씬':<5}{'상태':<6}{'필요':>6}{'실제':>8}  파일")
    print("-" * 62)
    for i, sc in enumerate(scenes, 1):
        want, path = float(sc["use"]), sc["file"]
        info = probe(path) if os.path.exists(path) else None
        if info is None:
            missing.append(i)
            print(f"C{i:<4}{'없음':<6}{want:>5.1f}s{'-':>8}  {path}")
            continue
        dur, w, h = info
        state, note = "OK", ""
        if dur + 0.05 < want:
            short.append(i)
            state = "짧음"
        elif w > h:
            # Flow's default is 16:9. A landscape clip crops to a narrow strip
            # of the original frame, so it is a redo, not a warning.
            landscape.append(i)
            state = "가로!"
            note = "  ← 9:16으로 다시 생성해야 합니다"
        else:
            ready += 1
        print(f"C{i:<4}{state:<6}{want:>5.1f}s{dur:>7.1f}s  {os.path.basename(path)}"
              f"  {w}x{h}{note}")

    total = len(scenes)
    print("-" * 62)
    print(f"{ready}/{total} 준비됨")
    if missing:
        print(f"생성 필요: {', '.join('C%d' % i for i in missing)}")
    if short:
        print(f"다시 생성(길이 부족): {', '.join('C%d' % i for i in short)}")
    if landscape:
        print(f"다시 생성(가로로 나옴): {', '.join('C%d' % i for i in landscape)}")
        print("  Flow 설정에서 화면 비율을 9:16으로 바꾸고 다시 뽑으세요.")

    sheet = contact_sheet(scenes, args.sheet)
    if sheet:
        print(f"\n미리보기: {os.path.abspath(sheet)}")
        print("  컷마다 한 장면씩 이어 붙였습니다. 조립 전에 한 번 보세요 —")
        print("  가로로 나온 컷, 엉뚱한 장면, 안 맞는 쌍둥이 컷이 여기서 보입니다.")

    if ready == total:
        print("\n→ build.py 실행 가능")
    sys.exit(0 if ready == total else 1)


if __name__ == "__main__":
    main()
