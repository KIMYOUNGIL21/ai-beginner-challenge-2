# ai-shorts 교재 배포 기준

- 원본 위치: `/Users/kim/orca/projects/ai/.claude/skills/ai-shorts`
- 마지막 동기화: 2026-08-23 11:12 KST
- 구조 기준: 최신 6컷 / 실측 TTS 31.95초 예시
- 교재 기본 실습: API 없는 3장면 14초 조립 데모

## 원본 동일성 확인

아래 명령의 출력이 없으면 운영 원본과 교재 배포본이 같다.

```bash
diff -qr --exclude=.venv --exclude=__pycache__ \
  /Users/kim/orca/projects/ai/.claude/skills/ai-shorts \
  day07-assets/ai-shorts
```

## SHA-256

```text
1598670f84b2154a3f4647f1ca4fa77005bb2046232c50ce81c42e3b55c271b8  SKILL.md
609c723b062f97816c562ae869bb528277bda6dc6ad1d5f5fbfff1ecea3b5f8b  references/prompt-formula.md
dc4a7c6ca7e97c3368d14fd6d5edb3561c9ee3f404e87c9b903a2092caf1bc90  scripts/build.py
f10277ef78b86a7a95c1c5dbc053425b8213f6026eaaff780c1b53227e9e37be  scripts/check.py
2fb68d8c3e85cbeea6c6ad61a2584408f3d3b9032255f9887d89e02c9d4c91b1  scripts/ingest.py
ca0641e44421785b5c1abbebc83ee9caf624d408985538aec008b477b2f5c032  scripts/make-short.sh
40cc40bedc3196b10671aeed4e91c32ac8427d600ca2b16cb049f294a2008d17  scripts/setup.sh
145d3b7c4a036b56d785b0008787594435cd381cad9e2624e8496818504c0065  scripts/subs.py
31fe8d9fc4581601c3eae1b4d031b18e47e940d96f0359b21edf2f8a7dc52765  scripts/tts.py
```

운영 원본이 바뀌면 먼저 전체 실습을 재검증한 뒤 이 파일과 ZIP을 함께 갱신한다.
