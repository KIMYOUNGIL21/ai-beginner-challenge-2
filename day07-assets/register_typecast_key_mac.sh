#!/usr/bin/env bash
set -euo pipefail
config_dir="$HOME/.config/ai-shorts"
config_file="$config_dir/secrets.env"
mkdir -p "$config_dir"
chmod 700 "$config_dir"
printf 'Typecast API 키 입력(화면에 보이지 않음): '
IFS= read -r -s typecast_key
printf '\n'
if [ -z "$typecast_key" ]; then
  echo '입력된 키가 없습니다.'
  exit 1
fi
umask 077
printf 'TYPECAST_API_KEY=%q\nTYPECAST_VOICE=%q\n' "$typecast_key" 'tc_69fc0cff784968297fb45daa' > "$config_file"
chmod 600 "$config_file"
unset typecast_key
echo 'Typecast 연결 정보를 사용자 전용 설정에 저장했습니다. 키 값은 출력하지 않습니다.'
