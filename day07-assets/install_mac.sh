#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo "Python 3가 없습니다. 운영자에게 알려 주세요."; exit 1; }
command -v ffmpeg >/dev/null || { echo "ffmpeg가 없습니다. 먼저 운영자 설치 안내를 받으세요."; exit 1; }
install_root="${AI_SHORTS_INSTALL_ROOT:-$HOME/.claude/skills}"
mkdir -p "$install_root"
target="$install_root/ai-shorts"
if [ -e "$target" ]; then
  stamp="$(date +%Y%m%d-%H%M%S)"
  backup="$install_root/ai-shorts.backup-$stamp"
  mv "$target" "$backup"
  echo "기존 Skill 백업: $backup"
fi
cp -R ai-shorts "$target"
python3 -m venv "$target/.venv"
"$target/.venv/bin/pip" install -q pillow
echo "설치 완료: $target"
echo "Claude Code 새 세션에서 /ai-shorts 를 확인하세요."
