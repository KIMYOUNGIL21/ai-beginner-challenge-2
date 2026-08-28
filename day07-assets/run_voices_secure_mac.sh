#!/usr/bin/env bash
set -euo pipefail

text="${1:-오늘부터 작은 기록을 시작합니다.}"
query="${2:-차분하고 또렷한 한국어 내레이션}"
out="${3:-voices}"

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

skill="${AI_SHORTS_SKILL_ROOT:-$HOME/.claude/skills/ai-shorts}"
"$skill/.venv/bin/python" "$skill/scripts/voices.py" "$text" \
  --out "$out" --query "$query" --n 5
