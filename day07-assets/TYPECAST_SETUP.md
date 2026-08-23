# Typecast API 키 안전 등록

## 절대 하지 않을 것

- Claude 채팅이나 카카오톡에 실제 키 붙여넣기
- 키가 보이는 터미널 화면 캡처
- 프로젝트 폴더나 GitHub에 키 저장

## 1. 키 준비

Typecast 개발자 페이지에서 현재 API 플랜·크레딧·사용 조건을 먼저 확인합니다. 키를 새로 만들거나 기존 키의 복사 버튼을 누릅니다. 키의 발급 화면과 상업 이용 조건은 바뀔 수 있으므로 개강 당일 운영자 안내를 따릅니다.

## 2. 화면에 보이지 않게 로컬 등록

Claude에게 다음처럼 요청합니다.

```text
실제 API 키를 채팅으로 받지 마세요.
Mac이면 register_typecast_key_mac.sh, Windows면 register_typecast_key_windows.ps1의 내용을 설명하고,
내 승인 뒤 통합 Terminal에서 실행해 키를 보이지 않게 직접 입력하도록 안내해 주세요.
등록 뒤 키 값은 출력하지 말고 설정 파일 존재와 권한만 확인하세요.
```

Mac은 실행 중 `Typecast API 키 입력`이 나오면 키를 붙이고 Enter를 누릅니다. 글자가 안 보이는 것이 정상입니다. Windows는 별도 보안 입력창에 붙입니다.

저장 위치:

- Mac: `~/.config/ai-shorts/secrets.env`, 권한 600
- Windows: `%USERPROFILE%\.config\ai-shorts\secrets.env`

목소리 후보를 들을 때는 `run_voices_secure_mac.sh` 또는
`run_voices_secure_windows.ps1`, 전체 음성을 만들 때는
`run_tts_secure_mac.sh` 또는 `run_tts_secure_windows.ps1`이 이 파일을 현재
프로세스에만 불러옵니다. 값을 대화나 로그에 다시 출력하지 않습니다.

## 3. 목소리 선택은 키 파일과 분리

후보를 들은 뒤 고른 번호의 `voice_id`는 프로젝트의 `my-short/voice.txt`에 저장합니다. `voice_id`는 비밀키가 아닙니다. Claude는 `secrets.env`를 열거나 수정하지 않고, 안전 실행기에 아래처럼 선택 ID만 인자로 넘깁니다.

```text
Mac:     run_tts_secure_mac.sh my-short/script.txt my-short/work [voice_id]
Windows: run_tts_secure_windows.ps1 -ScriptFile my-short/script.txt -WorkDir my-short/work -VoiceId [voice_id]
```

이 방식이면 목소리를 바꿔도 API 키 파일을 읽거나 다시 저장할 필요가 없습니다.

노출되었다면 Typecast에서 해당 키를 폐기하고 새로 발급합니다.
