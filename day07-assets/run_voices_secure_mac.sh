#!/usr/bin/env bash
set -euo pipefail

text="${1:-오늘부터 작은 기록을 시작합니다.}"
query="${2:-차분하고 또렷한 한국어 내레이션}"
out="${3:-voices}"
secrets="${AI_SHORTS_SECRETS_FILE:-$HOME/.config/ai-shorts/secrets.env}"

if [ ! -f "$secrets" ]; then
  echo 'Typecast 연결 정보가 없습니다. TYPECAST_SETUP.md를 먼저 보세요.'
  exit 1
fi

set -a
source "$secrets"
set +a
trap 'unset TYPECAST_API_KEY' EXIT

skill="${AI_SHORTS_SKILL_ROOT:-$HOME/.claude/skills/ai-shorts}"
"$skill/.venv/bin/python" "$skill/scripts/voices.py" "$text" \
  --out "$out" --query "$query" --n 5
