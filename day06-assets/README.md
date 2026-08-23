# Day 6 시작 폴더

압축을 푼 이 폴더 이름을 `day06-닉네임`으로 바꾸고, Day 5의 `index.html`, `my-info.txt`, `CLAUDE.md` 세 파일을 안에 복사한 뒤 Claude Code Desktop의 로컬 세션에서 연다.

Mac Finder에서는 `.claude` 폴더가 숨겨져 보이지 않을 수 있지만 ZIP 안에 이미 들어 있다. 삭제하거나 새로 만들지 않는다.

```text
day06-assets/
├── .claude/skills/openchat-proof/SKILL.md
├── card-maker.html
├── input/result.json
├── scripts/build_card.py
├── output/
└── README.md
```

기본 완주는 `card-maker.html`을 두 번 눌러 브라우저에서 연다. 다섯 칸을 입력하고 미리보기와 다운로드를 누르면 Python 없이 `proof-card.html`이 생긴다.

아래 Python 실행은 설치된 사람의 선택 심화다.

- Mac: `python3 scripts/build_card.py`
- Windows: `py scripts/build_card.py`

성공하면 `output/proof-card.html`이 생긴다. 외부 패키지와 API 키는 필요 없다.
