#!/usr/bin/env bash
# One-time setup. Run once per machine, then never again.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== 쇼츠 제작 환경 확인 =="
fail=0

# Homebrew is how the other two get installed, so check it first — otherwise
# "brew install ffmpeg" just fails with command not found.
if command -v brew >/dev/null 2>&1; then
  echo "  Homebrew    OK"
  BREW=1
else
  echo "  Homebrew    없음  ← 먼저 이것부터"
  echo "              아래 한 줄을 터미널에 붙여넣고 실행하세요:"
  echo ""
  echo '              /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  echo ""
  echo "              설치가 끝나면 화면에 나오는 안내(PATH 추가)를 따라 하고,"
  echo "              터미널을 새로 연 뒤 이 스크립트를 다시 실행하세요."
  BREW=0
  fail=1
fi

if command -v ffmpeg >/dev/null 2>&1; then
  echo "  ffmpeg      OK  ($(ffmpeg -version | head -1 | cut -d' ' -f3))"
else
  echo "  ffmpeg      없음"
  [ "$BREW" = "1" ] && echo "              설치: brew install ffmpeg"
  fail=1
fi

if command -v python3 >/dev/null 2>&1; then
  echo "  python3     OK  ($(python3 -V | cut -d' ' -f2))"
else
  echo "  python3     없음"
  echo "              설치: brew install python"
  fail=1
fi

[ "$fail" -eq 0 ] || { echo; echo "위 항목을 설치한 뒤 다시 실행하세요."; exit 1; }

# Subtitles need libass, or Pillow as the fallback renderer.
if ffmpeg -hide_banner -filters 2>/dev/null | awk '{print $2}' | grep -qx ass; then
  echo "  자막        ffmpeg libass 사용"
else
  echo "  자막        libass 없음 → Pillow 준비 중..."
  [ -d .venv ] || python3 -m venv .venv
  ./.venv/bin/pip install -q --disable-pip-version-check pillow
  echo "              OK  (Pillow $(./.venv/bin/python -c 'import PIL;print(PIL.__version__)'))"
fi

echo
if [ -n "${TYPECAST_API_KEY:-}" ] && [ -n "${TYPECAST_VOICE:-}" ]; then
  echo "  타임캐스트  키·보이스 설정됨"
  echo
  echo "준비 완료. 영상 폴더를 만들고 거기서 클로드를 여세요."
else
  echo "  타임캐스트  아직 설정 안 됨"
  echo
  echo "마지막 한 단계 — ~/.zshrc 맨 아래에 이 두 줄을 넣으세요."
  echo "  (텍스트 편집기로 열려면:  open -e ~/.zshrc )"
  echo
  echo "    export TYPECAST_API_KEY=여기에_발급받은_키"
  echo "    export TYPECAST_VOICE=tc_69fc0cff784968297fb45daa"
  echo
  echo "  키 발급: https://studio.typecast.ai/developers/api"
  echo "  저장한 뒤 터미널을 새로 열면 적용됩니다."
fi
