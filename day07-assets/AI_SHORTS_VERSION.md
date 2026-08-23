# ai-shorts 교재 배포 기준

- 원본 위치: `/Users/kim/orca/projects/ai/.claude/skills/ai-shorts`
- 마지막 동기화·교육용 보안 수정: 2026-08-23 KST
- 구조 기준: 최신 6컷 / 실측 TTS 31.95초 예시
- 교재 기본 실습: API 없는 3장면 14초 조립 데모

## 운영 원본과의 관계

스크립트와 6컷 공식은 운영 원본 기준이다. 교육용 `SKILL.md`는 실제 API 키를
Claude 채팅으로 받지 않고 로컬 보안 등록 파일만 사용하도록 의도적으로 수정했다.
따라서 전체 폴더 diff는 `SKILL.md` 차이를 보여 주는 것이 정상이다.

```bash
diff -qr --exclude=.venv --exclude=__pycache__ \
  /Users/kim/orca/projects/ai/.claude/skills/ai-shorts \
  day07-assets/ai-shorts
```

## SHA-256

```text
36cf8b08cd1de8d81f9ff5fd3adb23f0718e5164a032cf312a3e072c4d15e096  SKILL.md
3eebbf6eddbf719f2fc3c9186a72e211da16d14d34d2675dd4c47b88682671ae  references/prompt-formula.md
dc4a7c6ca7e97c3368d14fd6d5edb3561c9ee3f404e87c9b903a2092caf1bc90  scripts/build.py
f10277ef78b86a7a95c1c5dbc053425b8213f6026eaaff780c1b53227e9e37be  scripts/check.py
2fb68d8c3e85cbeea6c6ad61a2584408f3d3b9032255f9887d89e02c9d4c91b1  scripts/ingest.py
ca0641e44421785b5c1abbebc83ee9caf624d408985538aec008b477b2f5c032  scripts/make-short.sh
40cc40bedc3196b10671aeed4e91c32ac8427d600ca2b16cb049f294a2008d17  scripts/setup.sh
145d3b7c4a036b56d785b0008787594435cd381cad9e2624e8496818504c0065  scripts/subs.py
31fe8d9fc4581601c3eae1b4d031b18e47e940d96f0359b21edf2f8a7dc52765  scripts/tts.py
018f5201f78b9de530241abc08cd138def3e0cdeb3484f116ab3b28bbfaf4105  install_mac.sh
18c58945dc956fc0f8bc800a7934071e33c552bebcfcb444adae0291eae5a355  install_windows.ps1
d31c9d2bd8591627101f203f39c4698ba4e5d323aa2b676730448a17919f2cdb  register_typecast_key_mac.sh
059f5d2c614f8d23fdcce8af4c37b3301e4f3a6a1204795c1450cefd0767833a  register_typecast_key_windows.ps1
7bbbe7ddf6ad68b077d92bdecca0b73f9bd8623ae75ea5ecf8c5756197ccb946  run_tts_secure_mac.sh
a947797754d4ed281ba05eb1cd1dede5f0da5d7ec382bf42d43f228c6d2a5e66  run_tts_secure_windows.ps1
```

운영 원본이 바뀌면 먼저 전체 실습을 재검증한 뒤 이 파일과 ZIP을 함께 갱신한다.
