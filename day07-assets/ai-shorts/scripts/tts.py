#!/usr/bin/env python3
"""Typecast Timestamp TTS -> narration.wav + words.json

Synthesizes a script sentence by sentence so Smart Emotion gets surrounding
context, then concatenates the parts and rebases every word timestamp onto the
concatenated timeline. Those timings are what build.py turns into subtitles, so
they must describe the exact audio we ship -- never a re-recorded take.

Usage:
  TYPECAST_API_KEY=... python3 tts.py script.txt out/ --voice tc_xxx
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

API = "https://api.typecast.ai/v1/text-to-speech/with-timestamps?granularity=word"
UA = ("typecast-direct/1 python-urllib typecast-integration/1 "
      "(source=api-docs; generated_by=claude-code)")
MAX_CHARS = 2000
GAP = 0.25  # seconds of silence between sentences


def split_sentences(text):
    """Split Korean narration into sentences, keeping terminal punctuation."""
    parts = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        for s in re.split(r'(?<=[.!?])\s+', line):
            s = s.strip()
            if not s:
                continue
            if len(s) > MAX_CHARS:
                sys.exit(f"sentence exceeds {MAX_CHARS} chars: {s[:60]}...")
            parts.append(s)
    if not parts:
        sys.exit("script is empty")
    return parts


def synth(text, prev, nxt, voice, key, lang):
    """Synthesize one sentence and return audio + word timings.

    This is the only provider-specific function. Everything downstream —
    sentence splitting, concatenation, timestamp rebasing — works off the
    {audio, words:[{text,start,end}]} shape, so swapping TTS providers means
    rewriting this and nothing else. Fish Audio was evaluated and parked:
    its timestamps exist only on an SSE endpoint, which would move stream
    reassembly into the one place a mistake silently desyncs every subtitle.
    """
    body = {
        "voice_id": voice,
        "text": text,
        "model": "ssfm-v30",
        "language": lang,
        # Smart Emotion reads tone from the neighbouring lines instead of us
        # faking delivery with pitch/tempo.
        "prompt": {"emotion_type": "smart", "previous_text": prev, "next_text": nxt},
        "output": {"audio_format": "wav"},
    }
    req = urllib.request.Request(
        API,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "X-API-KEY": key, "User-Agent": UA},
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:400]
        hint = {
            401: "check TYPECAST_API_KEY",
            402: "out of API credits",
            403: "legacy Starter key? regenerate at studio.typecast.ai/developers/api",
            404: f"voice_id {voice} not found",
            429: "rate limited, retry slower",
        }.get(e.code, "")
        sys.exit(f"typecast {e.code}: {hint}\n{detail}")


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("outdir")
    ap.add_argument("--voice", required=True, help="tc_ or uc_ voice id")
    ap.add_argument("--lang", default="kor")
    args = ap.parse_args()

    key = os.environ.get("TYPECAST_API_KEY")
    if not key:
        sys.exit("set TYPECAST_API_KEY (create one at studio.typecast.ai/developers/api)")

    sentences = split_sentences(open(args.script, encoding="utf-8").read())
    parts_dir = os.path.join(args.outdir, "tts_parts")
    os.makedirs(parts_dir, exist_ok=True)

    wavs, words, offset = [], [], 0.0
    for i, s in enumerate(sentences):
        prev = sentences[i - 1] if i else ""
        nxt = sentences[i + 1] if i + 1 < len(sentences) else ""
        print(f"  [{i+1}/{len(sentences)}] {s[:40]}...", file=sys.stderr)
        res = synth(s, prev, nxt, args.voice, key, args.lang)

        wav = os.path.join(parts_dir, f"{i:03d}.wav")
        with open(wav, "wb") as f:
            f.write(base64.b64decode(res["audio"]))
        wavs.append(wav)

        for w in res.get("words") or []:
            words.append({"text": w["text"],
                          "start": w["start"] + offset,
                          "end": w["end"] + offset,
                          "sentence": i})
        # Measure the file we actually wrote; audio_duration is advisory.
        offset += duration(wav) + GAP

    # Concat with GAP of silence between parts.
    listing = os.path.join(parts_dir, "concat.txt")
    silence = os.path.join(parts_dir, "gap.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
                    "-i", f"anullsrc=r=44100:cl=mono", "-t", str(GAP), silence], check=True)
    with open(listing, "w") as f:
        for j, w in enumerate(wavs):
            if j:
                f.write(f"file '{os.path.abspath(silence)}'\n")
            f.write(f"file '{os.path.abspath(w)}'\n")

    narration = os.path.join(args.outdir, "narration.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", listing, "-ar", "44100", "-ac", "1", narration], check=True)

    with open(os.path.join(args.outdir, "words.json"), "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=1)

    print(f"narration.wav  {duration(narration):.2f}s")
    print(f"words.json     {len(words)} words")


if __name__ == "__main__":
    main()
