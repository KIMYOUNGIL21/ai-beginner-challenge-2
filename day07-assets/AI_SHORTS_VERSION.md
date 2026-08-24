# ai-shorts 교재 배포 기준

- 운영 원본: 운영자의 `ai-shorts` Skill 저장소
- 채택 커밋: `f23d0a4` — 2026-08-23 14:39:46 KST
- 구조 기준: 5문장 · 5컷 · 전부 6초 생성 · 완성 약 20~23초
- 교재 작은 성공: 외부 호출 없는 3장면 14초 조립 데모

## 이번 동기화에서 들어온 기능

- `voices.py`: 같은 첫 문장을 읽는 음성 후보 5개 미리듣기
- `plan.py`: Typecast 실제 낭독 시간에서 컷 길이 자동 계산
- `ingest.py`: 다운로드 순서가 모호하면 확인 시트를 열고 추측 금지
- `check.py`: 가로 영상·짧은 영상·빠진 컷과 미리보기 시트 확인
- Flow 크레딧 부족 시 받은 클립만으로 시간을 다시 맞추는 복구 흐름
- 긴 Flow 프롬프트를 컷별로 클립보드에 복사하는 평문 요청

## 운영 원본과 다른 교육용 조정

핵심 생성·측정·배치·검사·조립 스크립트는 원본과 같습니다. 교육 패키지에서는
다음 네 파일만 조정했습니다.

- `SKILL.md`: Day 6 `shorts-brief-v1` 이어받기, Mac/Windows 승인 설치, 키와 voice ID 분리
- `references/prompt-formula.md`: 고정 가격 단정을 없애고 현재 Flow 화면 우선
- `scripts/setup.sh`: 설치·zshrc 안내를 없앤 읽기 전용 상태 검사 (Windows의 `py`·`.venv\Scripts`도 함께 인식)
- `scripts/make-short.sh`: 안전 실행기로 만든 음성만 재사용하고 키 export 금지

키를 채팅이나 명령어에 직접 넣지 않고 시작 패키지의 마스킹 입력과 안전 실행기를
사용합니다. 안전 실행기로 이미 만든 `narration.wav`·`words.json`은
`make-short.sh`가 키 없이 재사용할 수 있습니다.

```bash
diff -qr --exclude=.venv --exclude=__pycache__ \
  "<운영 원본 경로>/ai-shorts" \
  day07-assets/ai-shorts
```

정상 결과는 위 네 파일만 다르다고 나옵니다.

## 핵심 SHA-256

```text
a1d75410b45fa58133f7d85b6d5d8faec599aadc4b56d0a3a79957ffaaaff819  SKILL.md
56994e450dd2cf3aac54bceb6b44ae77dc9992a82ad0bf90e29fd58397d18b6a  references/prompt-formula.md
1ec5a7dd8c99a11fad39a8e6ca2840d90c307787b165178a5b53b70bb275b3c0  scripts/build.py
664adec44eb987bee943f1e557a742cecbe8b6c841df1119100381b58cc4d6b2  scripts/check.py
67744b66f1d27c2be53dde6387d9e1b1fa8673dafee865ae5b8c2a9c176f136e  scripts/ingest.py
69157cfc0d04af3616806094fdaf18c5b76b19d42b804be18572968ac12625d3  scripts/plan.py
75556b33efc8cfa64baf1c0a7dc9b2f605a195a1770a39e355e2623e76695a2d  scripts/setup.sh
81eff7efc7bc80ef96dd6e630afe1e70cd7700e1ca7cf6d02fab5a9c0b43781e  scripts/subs.py
31fe8d9fc4581601c3eae1b4d031b18e47e940d96f0359b21edf2f8a7dc52765  scripts/tts.py
2e0d00ef25825859198bc8446ffee47081644a27c0661b60799466f9ce160cfd  scripts/voices.py
0c37b935cbb51b590df5632795ea68abdfd7ad54fb7b05afb4dae6251f8399fe  scripts/make-short.sh
```

## 검증 기록

- Python 스크립트 전체 문법 검사 통과
- Mac 셸 스크립트 전체 문법 검사 통과
- 제공 데모: `3/3 준비됨`
- 제공 데모 최종 MP4: 14.00초 · 1080×1920 · 영상+음성 · 자막 8개
- Day 6 전달: `shorts-brief-v1` · C1~C5 · 계획 21초 → `script.txt` 5줄 생성
- 목소리 전달: 비밀키 출력 없이 선택한 `voice_id`가 안전 실행기 `--voice` 인자로 전달됨
- 민감한 키 문자열 미포함
