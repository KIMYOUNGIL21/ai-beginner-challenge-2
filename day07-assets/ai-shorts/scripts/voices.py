#!/usr/bin/env python3
"""Synthesize the same line with several Typecast voices so it can be heard.

Voice metadata (name, gender, age, tags) does not tell you what a voice sounds
like, and picking wrong is expensive later: narration length drives every cut
length, so changing voice after the clips exist invalidates them. This renders
candidates up front, using a line from the actual script, and writes both
individual files and one concatenated preview.

Usage:
  TYPECAST_API_KEY=... python3 voices.py "여름에 통유리 건물 안은 40도까지 오릅니다." \
      --out voices/ --query "차분한 중년 남성 다큐멘터리 내레이션"
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.typecast.ai"
UA = ("typecast-direct/1 python-urllib typecast-integration/1 "
      "(source=api-docs; generated_by=claude-code)")


def call(path, key, body=None):
    req = urllib.request.Request(
        API + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Content-Type": "application/json", "X-API-KEY": key, "User-Agent": UA},
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        hint = {401: "check TYPECAST_API_KEY", 402: "out of API credits",
                403: "old key? regenerate at studio.typecast.ai/developers/api",
                429: "rate limited"}.get(e.code, "")
        sys.exit(f"typecast {e.code}: {hint}\n{detail}")


def candidates(key, query, gender, n):
    """Recommendations when a description is given, otherwise browse and filter."""
    if query:
        q = urllib.parse.urlencode({"query": query})
        rec = call(f"/v1/voices/recommendations?{q}", key)
        ids = [r["voice_id"] for r in rec]
    else:
        ids = None

    allv = {v["voice_id"]: v for v in call("/v2/voices", key)}
    picked = []
    for vid in (ids or allv):
        v = allv.get(vid)
        if not v:
            continue
        # ssfm-v30 is what tts.py synthesizes with; anything else would preview
        # a voice the pipeline cannot actually use.
        if not any(m["version"] == "ssfm-v30" for m in v.get("models", [])):
            continue
        if gender and v.get("gender") != gender:
            continue
        picked.append(v)
        if len(picked) >= n:
            break
    if not picked:
        sys.exit("조건에 맞는 보이스를 못 찾았습니다. --query 나 --gender 를 바꿔보세요.")
    return picked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sample", help="들어볼 문장 — 실제 대본의 첫 문장을 쓰는 게 좋다")
    ap.add_argument("--out", default="voices")
    ap.add_argument("--query", default="", help="원하는 톤을 문장으로")
    ap.add_argument("--gender", choices=["male", "female"])
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--lang", default="kor")
    args = ap.parse_args()

    key = os.environ.get("TYPECAST_API_KEY")
    if not key:
        sys.exit("set TYPECAST_API_KEY (studio.typecast.ai/developers/api)")

    picked = candidates(key, args.query, args.gender, args.n)
    os.makedirs(args.out, exist_ok=True)

    rows, files = [], []
    for i, v in enumerate(picked, 1):
        print(f"  [{i}/{len(picked)}] {v['voice_name']}", file=sys.stderr)
        # The plain TTS endpoint streams raw audio bytes; the timestamps one
        # wraps it in JSON, which is easier to handle uniformly here.
        # The voice announces its own number. Listening to the combined file,
        # there is otherwise no way to tell which candidate is speaking, and
        # "pick a number" becomes a guess.
        res = call("/v1/text-to-speech/with-timestamps?granularity=word", key, {
            "voice_id": v["voice_id"], "text": f"{i}번. {args.sample}",
            "model": "ssfm-v30", "language": args.lang,
            "output": {"audio_format": "wav"},
        })
        wav = os.path.join(args.out, f"{i:02d}-{v['voice_name']}.wav")
        with open(wav, "wb") as f:
            f.write(base64.b64decode(res["audio"]))
        files.append(wav)
        rows.append({"n": i, "voice_id": v["voice_id"], "voice_name": v["voice_name"],
                     "gender": v.get("gender", ""), "age": v.get("age", ""),
                     "use_cases": v.get("use_cases", []), "file": wav})

    # One file that plays every candidate in order, for quick comparison.
    gap = os.path.join(args.out, ".gap.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
                    "-i", "anullsrc=r=44100:cl=mono", "-t", "0.7", gap], check=True)
    listing = os.path.join(args.out, ".all.txt")
    with open(listing, "w") as f:
        for j, w in enumerate(files):
            if j:
                f.write(f"file '{os.path.abspath(gap)}'\n")
            f.write(f"file '{os.path.abspath(w)}'\n")
    allwav = os.path.join(args.out, "00-전체듣기.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", listing, "-ar", "44100", "-ac", "1", allwav], check=True)

    with open(os.path.join(args.out, "voices.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)

    print()
    print(f"{'번호':<5}{'이름':<14}{'성별':<8}{'나이':<13}용도")
    for r in rows:
        print(f"{r['n']:<5}{r['voice_name']:<14}{r['gender']:<8}{r['age']:<13}"
              f"{', '.join(r['use_cases'][:2])}")
    print(f"\n전체 듣기: {os.path.abspath(allwav)}")
    print(f"  → 각 후보가 자기 번호를 먼저 말한 뒤 문장을 읽습니다.")
    print(f"개별 파일: {os.path.abspath(args.out)}/01-*.wav …")


if __name__ == "__main__":
    main()
