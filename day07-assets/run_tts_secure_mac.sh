#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 2 ]; then
  echo '사용법: run_tts_secure_mac.sh script.txt work폴더 [voice_id]'
  exit 1
fi
secrets="$HOME/.config/ai-shorts/secrets.env"
if [ ! -f "$secrets" ]; then
  echo 'Typecast 연결 정보가 없습니다. TYPECAST_SETUP.md를 먼저 보세요.'
  exit 1
fi
set -a
source "$secrets"
set +a
voice="${3:-${TYPECAST_VOICE:-tc_69fc0cff784968297fb45daa}}"
runner="$HOME/.claude/skills/ai-shorts/.venv/bin/python"
tts="$HOME/.claude/skills/ai-shorts/scripts/tts.py"
"$runner" "$tts" "$1" "$2" --voice "$voice"
unset TYPECAST_API_KEY
