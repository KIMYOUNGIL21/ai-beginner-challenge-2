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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenes")
    args = ap.parse_args()
    scenes = json.load(open(args.scenes, encoding="utf-8"))

    ready, missing, short = 0, [], []
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
        if dur + 0.05 < want:
            short.append(i)
            state = "짧음"
        else:
            ready += 1
            state = "OK"
        note = "" if w * 16 == h * 9 or w >= h else "  (세로 소스 — 크롭 확인)"
        print(f"C{i:<4}{state:<6}{want:>5.1f}s{dur:>7.1f}s  {os.path.basename(path)}"
              f"  {w}x{h}{note}")

    total = len(scenes)
    print("-" * 62)
    print(f"{ready}/{total} 준비됨")
    if missing:
        print(f"생성 필요: {', '.join('C%d' % i for i in missing)}")
    if short:
        print(f"다시 생성(길이 부족): {', '.join('C%d' % i for i in short)}")
    if ready == total:
        print("→ build.py 실행 가능")
    sys.exit(0 if ready == total else 1)


if __name__ == "__main__":
    main()
