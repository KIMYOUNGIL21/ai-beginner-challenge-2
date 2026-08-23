#!/usr/bin/env python3
"""words.json -> scenes.json. Cut lengths come from the measured narration.

The whole premise of this pipeline is that cut lengths cannot be eyeballed --
guessing was 23% off on the first script we tried. Until this script existed,
that arithmetic was done by hand in chat, i.e. by exactly the faculty that was
wrong the first time. This does it from the data.

Cuts land on sentence starts so a picture change coincides with a new line.

Usage:
  python3 plan.py work/ --out scenes.json [--max-use 5.0] [--gen 6]
"""
import argparse
import json
import os
import subprocess
import sys


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir")
    ap.add_argument("--out", default="scenes.json")
    ap.add_argument("--max-use", type=float, default=5.0,
                    help="한 컷 상한. Flow 생성 길이보다 1초 이상 짧아야 한다")
    ap.add_argument("--gen", type=int, default=6, help="Flow 생성 길이(초)")
    args = ap.parse_args()

    words_path = os.path.join(args.workdir, "words.json")
    narration = os.path.join(args.workdir, "narration.wav")
    for p in (words_path, narration):
        if not os.path.exists(p):
            sys.exit(f"missing {p} — tts.py 를 먼저 도세요")

    words = json.load(open(words_path, encoding="utf-8"))
    if not words:
        sys.exit("words.json 이 비어 있습니다")
    total = duration(narration)

    starts = {}
    for w in words:
        starts.setdefault(w["sentence"], w["start"])
    order = sorted(starts)

    # One cut per sentence. The leading silence belongs to the first cut --
    # otherwise the opening frame freezes for that long before the voice starts.
    bounds = [0.0] + [starts[s] for s in order[1:]] + [total]
    uses = [round(bounds[i + 1] - bounds[i], 1) for i in range(len(order))]

    over = [(i + 1, u) for i, u in enumerate(uses) if u > args.max_use]
    if over:
        print(f"컷이 {args.max_use}초를 넘습니다 — {args.gen}초로 생성해도 못 덮습니다.\n",
              file=sys.stderr)
        for n, u in over:
            print(f"  C{n}  {u}초  {' '.join(x['text'] for x in words if x['sentence']==order[n-1])}",
                  file=sys.stderr)
        sys.exit("\n해당 문장을 줄이고 tts.py 를 다시 도세요. 컷을 늘리면 크레딧이 모자랍니다.")

    scenes = [{"file": f"clips/c{i+1:02d}.mp4", "use": u} for i, u in enumerate(uses)]
    drift = abs(sum(uses) - total)
    if drift > 0.05:
        # Rounding to 0.1s can leave a sliver; put it on the last cut so the
        # video and the narration end together.
        scenes[-1]["use"] = round(scenes[-1]["use"] + (total - sum(uses)), 2)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(scenes, f, indent=1)

    print(f"{'컷':<5}{'생성':>6}{'사용':>7}   첫 문장")
    for i, s in enumerate(scenes):
        first = next(x['text'] for x in words if x['sentence'] == order[i])
        print(f"C{i+1:<4}{str(args.gen)+'초':>6}{s['use']:>6.1f}s   {first}…")
    print(f"{'':11}{sum(s['use'] for s in scenes):>6.1f}s   (내레이션 {total:.2f}s)")
    print(f"\n{args.out} · 생성 {len(scenes)}회 × {args.gen}초")


if __name__ == "__main__":
    main()
