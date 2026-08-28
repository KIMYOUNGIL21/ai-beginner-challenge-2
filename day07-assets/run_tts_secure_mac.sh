#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 3 ]; then
  echo '사용법: run_tts_secure_mac.sh script.txt work폴더 voice_id'
  exit 1
fi

keyfile="./typecast-key.txt"
secrets="${AI_SHORTS_SECRETS_FILE:-$HOME/.config/ai-shorts/secrets.env}"

TYPECAST_API_KEY="${TYPECAST_API_KEY:-}"
if [ -f "$keyfile" ]; then
  TYPECAST_API_KEY="$(LC_ALL=C tr -d '[:space:]' < "$keyfile" | sed $'s/\xef\xbb\xbf//g')"
fi
if [ -z "$TYPECAST_API_KEY" ] && [ -f "$secrets" ]; then
  set -a
  source "$secrets"
  set +a
fi
if [ -z "${TYPECAST_API_KEY:-}" ]; then
  echo 'Typecast 키가 없습니다. typecast-key.txt를 두 번 눌러 열고, 복사한 키를 붙여넣어 저장한 뒤 다시 실행하세요.'
  exit 1
fi
export TYPECAST_API_KEY
trap 'unset TYPECAST_API_KEY' EXIT

voice="$3"
skill="${AI_SHORTS_SKILL_ROOT:-$HOME/.claude/skills/ai-shorts}"
runner="$skill/.venv/bin/python"
tts="$skill/scripts/tts.py"
"$runner" "$tts" "$1" "$2" --voice "$voice"
