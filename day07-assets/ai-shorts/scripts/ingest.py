#!/usr/bin/env python3
"""Rename Flow downloads into the clips/ layout build.py expects.

Flow drops files into ~/Downloads under generated names, so mapping eleven of
them onto C1..C11 by hand is where this pipeline actually breaks. Flow is
worked scene by scene, so download order matches scene order -- that is the
default mapping, shown for confirmation before anything moves.

Usage:
  python3 ingest.py scenes.json                    # preview mtime-order mapping
  python3 ingest.py scenes.json --apply
  python3 ingest.py scenes.json --map 7=~/Downloads/x.mp4 --apply   # redo one
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

EXTS = {".mp4", ".mov", ".webm", ".m4v"}


def state_path(scenes_file):
    return os.path.join(os.path.dirname(os.path.abspath(scenes_file)), ".ingest.json")


def load_state(scenes_file):
    try:
        return json.load(open(state_path(scenes_file), encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def candidates(src_dir, since, consumed):
    """Downloads newer than `since`, oldest first, skipping ones already placed.

    Without the consumed set, a partial run would re-offer files it already
    used and silently shift every later scene by one.

    Returns (paths, ambiguous). Ambiguous is True when the timestamps do not
    separate the files: a Shift-select batch download writes them all in the
    same instant, so arrival order is gone and sorted() falls back to the
    filename, which for Flow is a hash. Guessing there scrambles every cut.
    """
    out = []
    for name in os.listdir(src_dir):
        p = os.path.join(src_dir, name)
        if os.path.isfile(p) and os.path.splitext(name)[1].lower() in EXTS:
            if os.path.abspath(p) in consumed:
                continue
            st = os.stat(p)
            if st.st_mtime >= since:
                out.append((st.st_mtime, p))
    out.sort()
    times = [t for t, _ in out]
    ambiguous = len(times) > 1 and (max(times) - min(times)) < 2.0
    return [p for _, p in out], ambiguous


def order_sheet(paths, out):
    """Numbered thumbnail strip of the candidate files, in the offered order.

    When timestamps cannot tell us the order, the user has to. Asking them
    about hash filenames is unanswerable; asking them about pictures is a
    five-second look.
    """
    tiles = []
    for i, src in enumerate(paths, 1):
        t = f"/tmp/.ord{i:02d}.png"
        r = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", src, "-frames:v", "1",
             "-vf", ("scale=240:360:force_original_aspect_ratio=decrease,"
                     "pad=240:360:(ow-iw)/2:(oh-ih)/2:color=0x15181A,"
                     f"drawbox=x=0:y=0:w=54:h=54:color=0x15181A@0.85:t=fill"),
             t], capture_output=True)
        if r.returncode == 0:
            tiles.append(t)
    if not tiles:
        return None
    args = []
    for t in tiles:
        args += ["-i", t]
    try:
        subprocess.run(["ffmpeg", "-y", "-v", "error", *args,
                        "-filter_complex", f"hstack=inputs={len(tiles)}"
                        if len(tiles) > 1 else "null", out],
                       check=True, capture_output=True)
    except subprocess.CalledProcessError:
        return None
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
    ap.add_argument("--from", dest="src", default=os.path.expanduser("~/Downloads"))
    ap.add_argument("--map", action="append", default=[],
                    help="N=path, to place one scene explicitly")
    ap.add_argument("--since-hours", type=float, default=24.0)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    scenes = json.load(open(args.scenes, encoding="utf-8"))

    explicit = {}
    for m in args.map:
        n, _, path = m.partition("=")
        if not path:
            sys.exit(f"--map needs N=path, got {m!r}")
        idx = int(n)
        if not 1 <= idx <= len(scenes):
            sys.exit(f"--map {idx}: scenes.json only has {len(scenes)} scenes")
        explicit[idx] = os.path.expanduser(path)

    plan = []
    if explicit:
        for idx, src in sorted(explicit.items()):
            if not os.path.exists(src):
                sys.exit(f"--map {idx}: missing {src}")
            plan.append((idx, src))
    else:
        if not os.path.isdir(args.src):
            sys.exit(f"no such directory: {args.src}")
        since = time.time() - args.since_hours * 3600
        found, ambiguous = candidates(args.src, since, set(load_state(args.scenes)))
        # Only fill scenes that have no clip yet, in download order.
        todo = [i for i, sc in enumerate(scenes, 1) if not os.path.exists(sc["file"])]
        if not todo:
            print("모든 씬에 이미 클립이 있습니다. 교체하려면 --map 을 쓰세요.")
            return
        if not found:
            sys.exit(f"{args.src} 에서 최근 {args.since_hours:g}시간 내 영상 파일을 "
                     f"못 찾았습니다 (--since-hours 로 범위를 넓히세요)")
        if len(found) != len(todo):
            print(f"주의: 받은 파일 {len(found)}개 / 빈 씬 {len(todo)}개 — "
                  f"앞에서부터 {min(len(found), len(todo))}개만 배치합니다.\n",
                  file=sys.stderr)
        plan = list(zip(todo, found))

        if ambiguous and not args.apply:
            sheet = order_sheet(found, os.path.join(
                os.path.dirname(os.path.abspath(args.scenes)), "받은순서-확인.png"))
            print("⚠ 파일들이 같은 시각에 저장돼 있어 순서를 알 수 없습니다.")
            print("  한꺼번에 다운로드하면 이렇게 됩니다 — 아래 순서는 추측입니다.\n")
            if sheet:
                print(f"  미리보기: {sheet}")
                print("  왼쪽부터 1번입니다. 실제 컷 순서와 다르면 --map 으로 지정하세요.\n")

    print(f"{'씬':<5}{'길이':>7}{'필요':>7}  ←  파일")
    print("-" * 66)
    good, bad = [], []
    for idx, src in plan:
        want = float(scenes[idx - 1]["use"])
        dur = probe(src)
        if dur is None:
            flag, note = "  ✗ 읽을 수 없음", None
        elif dur + 0.05 < want:
            flag, note = "  ✗ 너무 짧음", None
        else:
            flag, note = "", (idx, src)
        (good if note else bad).append((idx, src))
        print(f"C{idx:<4}{(f'{dur:.1f}s' if dur else '?'):>7}{want:>6.1f}s  ←  "
              f"{os.path.basename(src)}{flag}")
    print("-" * 66)

    if not args.apply:
        print("미리보기입니다. 맞으면 --apply 를 붙여 실행하세요.")
        print("순서가 틀렸으면 --map 7=경로 형식으로 개별 지정하세요.")
        sys.exit(0 if not bad else 1)

    # Place what is usable and leave the rest for a redo. Holding the good
    # clips back would only mean regenerating them alongside the bad one.
    state = load_state(args.scenes)
    for idx, src in good:
        dst = scenes[idx - 1]["file"]
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
        shutil.copy2(src, dst)   # copy, so a bad mapping never eats the download
        state[os.path.abspath(src)] = idx
        print(f"C{idx} → {dst}")
    # Remember rejects too: a clip that is too short stays too short, and
    # leaving it in the pool would block the regenerated file behind it.
    for _, src in bad:
        state.setdefault(os.path.abspath(src), "rejected")
    with open(state_path(args.scenes), "w", encoding="utf-8") as f:
        json.dump(state, f, indent=1)

    print(f"\n{len(good)}개 배치 완료.")
    if bad:
        print(f"다시 생성 필요: {', '.join('C%d' % i for i, _ in bad)}")
        print("Flow에서 다시 받은 뒤 같은 명령을 그대로 실행하면 됩니다 "
              "(거부된 파일은 자동으로 건너뜁니다).")
    print(f"다음: check.py {args.scenes}")
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
