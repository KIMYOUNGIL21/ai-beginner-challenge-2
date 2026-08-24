#!/usr/bin/env bash
# Read-only environment check for the education package.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== 쇼츠 제작 환경 읽기 전용 확인 =="
missing=0

check_command() {
  local command_name="$1"
  local label="$2"
  if command -v "$command_name" >/dev/null 2>&1; then
    echo "  $label  OK"
  else
    echo "  $label  없음"
    missing=1
  fi
}

# Windows installs "py"/"python"; macOS and Linux install "python3".
python_bin=""
for candidate in python3 python py; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c "import sys" >/dev/null 2>&1; then
    python_bin="$candidate"
    break
  fi
done
if [ -n "$python_bin" ]; then
  echo "  Python 3  OK"
else
  echo "  Python 3  없음"
  missing=1
fi

check_command ffmpeg "FFmpeg "
check_command ffprobe "FFprobe "

# Windows venvs put the interpreter under Scripts/, unix under bin/.
venv_python=""
for candidate in .venv/bin/python .venv/Scripts/python.exe .venv/Scripts/python; do
  if [ -x "$candidate" ]; then
    venv_python="$candidate"
    break
  fi
done
if [ -n "$venv_python" ] && "$venv_python" -c 'import PIL' >/dev/null 2>&1; then
  echo "  자막 도구  OK"
else
  echo "  자막 도구  없음"
  missing=1
fi

secret_file="$HOME/.config/ai-shorts/secrets.env"
if [ -f "$secret_file" ]; then
  echo "  Typecast  로컬 보안 파일 있음 (값은 읽지 않음)"
else
  echo "  Typecast  아직 연결 안 됨 — API 없는 데모는 실행 가능"
fi

if [ "$missing" -ne 0 ]; then
  echo
  echo "준비 중단: 없는 프로그램이 있습니다. 임의 설치 명령을 실행하지 마세요."
  echo "시작 패키지의 PRECHECK 문서와 INSTALL_CLINIC.md를 운영자와 진행하세요."
  exit 1
fi

echo
echo "준비 완료: API 없는 데모를 조립할 수 있습니다."
echo "실제 목소리는 TYPECAST_SETUP.md의 가려진 입력 방식으로 별도 연결하세요."
