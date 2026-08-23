#!/usr/bin/env bash
# Everything after the Flow step, in one command.
#
# Deliberately a shell script and not a Claude tool call: the person receiving
# this may be using the Claude Desktop app, which cannot run ffmpeg on their
# machine. Claude writes script.txt / prompts.md / scenes.json; this turns them
# into the finished MP4 without Claude needing to touch the filesystem.
#
#   ./make-short.sh [프로젝트폴더]
#
# 프로젝트 폴더에 있어야 할 것:
#   script.txt   대본
#   scenes.json  씬 목록
set -euo pipefail

SKILL="$(cd "$(dirname "$0")/.." && pwd)"
PROJ="$(cd "${1:-.}" && pwd)"
cd "$PROJ"

PY=python3
[ -x "$SKILL/.venv/bin/python" ] && PY="$SKILL/.venv/bin/python"

die() { echo; echo "✗ $*" >&2; exit 1; }
step() { echo; echo "── $* ──"; }

[ -f script.txt ]  || die "script.txt 가 없습니다 (대본). 클로드가 만들어준 파일을 여기에 두세요: $PROJ"
[ -f scenes.json ] || die "scenes.json 이 없습니다 (씬 목록). 클로드가 만들어준 파일을 여기에 두세요: $PROJ"

[ -n "${TYPECAST_API_KEY:-}" ] || die "TYPECAST_API_KEY 를 설정하세요.
   발급: https://studio.typecast.ai/developers/api
   설정: export TYPECAST_API_KEY=..."
[ -n "${TYPECAST_VOICE:-}" ] || die "TYPECAST_VOICE 를 설정하세요.
   설정: export TYPECAST_VOICE=tc_xxxxxxxx"

step "1/4  내레이션 (타임캐스트)"
mkdir -p work
# TTS costs credits, so a re-run after fixing one scene must not re-synthesize.
if [ -f work/narration.wav ] && [ -f work/words.json ] \
   && [ work/narration.wav -nt script.txt ] && [ "${FORCE_TTS:-}" != "1" ]; then
  echo "  이미 생성된 내레이션을 재사용합니다 (다시 만들려면 FORCE_TTS=1)"
else
  $PY "$SKILL/scripts/tts.py" script.txt work/ --voice "$TYPECAST_VOICE"
fi

step "2/4  Flow 다운로드 배치"
# DOWNLOADS lets the caller point at somewhere other than ~/Downloads.
INGEST=("$PY" "$SKILL/scripts/ingest.py" scenes.json --apply)
[ -n "${DOWNLOADS:-}" ] && INGEST+=(--from "$DOWNLOADS")
if "${INGEST[@]}"; then :; else
  die "배치가 끝나지 않았습니다. 위 메시지를 확인하고, Flow에서 필요한 컷을 받은 뒤
   같은 명령을 그대로 다시 실행하세요."
fi

step "3/4  클립 확인"
$PY "$SKILL/scripts/check.py" scenes.json || die "빠진 씬이 있습니다. 위 목록을 Flow에서 생성한 뒤 다시 실행하세요."

step "4/4  영상 조립"
$PY "$SKILL/scripts/build.py" scenes.json work/ --out short.mp4

echo
echo "완성: $PROJ/short.mp4"
