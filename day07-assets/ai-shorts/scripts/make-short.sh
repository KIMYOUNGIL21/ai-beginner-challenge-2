#!/usr/bin/env bash
# Everything after the Flow step, in one command.
# Claude Desktop Code can run this through its integrated terminal after the
# user has reviewed and approved the command.
#
#   ./make-short.sh [프로젝트폴더] [결과파일명]
#
# 프로젝트 폴더에 있어야 할 것:
#   script.txt   대본
#   scenes.json  씬 목록
set -euo pipefail

SKILL="$(cd "$(dirname "$0")/.." && pwd)"
PROJ="$(cd "${1:-.}" && pwd)"
OUT="${2:-D07_쇼츠.mp4}"
cd "$PROJ"

# Prefer the package venv (it carries Pillow for subtitles). Windows puts it
# under Scripts/ and installs "py"/"python" rather than "python3", and the
# Store stubs named python/python3 only open the Microsoft Store, so every
# candidate has to actually run.
PY=""
for candidate in "$SKILL/.venv/bin/python" "$SKILL/.venv/Scripts/python.exe" \
                 "$SKILL/.venv/Scripts/python" python3 python py; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c "import sys" >/dev/null 2>&1; then
    PY="$candidate"
    break
  fi
done
[ -n "$PY" ] || { echo "✗ python 을 찾지 못했습니다. 시작 패키지의 설치 문서를 먼저 진행하세요." >&2; exit 1; }

die() { echo; echo "✗ $*" >&2; exit 1; }
step() { echo; echo "── $* ──"; }

[ -f script.txt ]  || die "script.txt 가 없습니다 (대본). 클로드가 만들어준 파일을 여기에 두세요: $PROJ"
[ -f scenes.json ] || die "scenes.json 이 없습니다 (씬 목록). 클로드가 만들어준 파일을 여기에 두세요: $PROJ"

step "1/4  내레이션 (타임캐스트)"
mkdir -p work
# TTS uses a secret, so the education package creates it only through the
# secure OS wrapper before this script runs. Never ask for or export the key.
if [ -f work/narration.wav ] && [ -f work/words.json ] \
   && ! [ script.txt -nt work/narration.wav ] \
   && ! [ script.txt -nt work/words.json ] \
   && [ "${FORCE_TTS:-}" != "1" ]; then
  echo "  이미 생성된 내레이션을 재사용합니다 (다시 만들려면 FORCE_TTS=1)"
else
  die "안전하게 만든 narration.wav와 words.json이 필요합니다.
   시작 패키지의 TYPECAST_SETUP.html을 읽고 run_tts_secure_mac.sh 또는
   run_tts_secure_windows.ps1로 먼저 음성을 만드세요. 키를 export하지 마세요."
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
$PY "$SKILL/scripts/build.py" scenes.json work/ --out "$OUT"

echo
echo "완성: $PROJ/$OUT"
