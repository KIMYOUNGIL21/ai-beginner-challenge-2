#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 3 ]; then
  echo '사용법: run_tts_secure_mac.sh script.txt work폴더 voice_id'
  exit 1
fi
secrets="${AI_SHORTS_SECRETS_FILE:-$HOME/.config/ai-shorts/secrets.env}"
if [ ! -f "$secrets" ]; then
  echo 'Typecast 연결 정보가 없습니다. TYPECAST_SETUP.md를 먼저 보세요.'
  exit 1
fi
set -a
source "$secrets"
set +a
trap 'unset TYPECAST_API_KEY' EXIT
voice="$3"
skill="${AI_SHORTS_SKILL_ROOT:-$HOME/.claude/skills/ai-shorts}"
runner="$skill/.venv/bin/python"
tts="$skill/scripts/tts.py"
"$runner" "$tts" "$1" "$2" --voice "$voice"
