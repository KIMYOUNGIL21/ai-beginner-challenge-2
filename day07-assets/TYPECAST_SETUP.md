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

Skill은 Typecast를 호출할 때 `run_tts_secure_mac.sh` 또는
`run_tts_secure_windows.ps1`로 이 파일을 현재 프로세스에만 불러옵니다. 값을
대화나 로그에 다시 출력하지 않습니다.

노출되었다면 Typecast에서 해당 키를 폐기하고 새로 발급합니다.
