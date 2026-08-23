# Day 6 시작 폴더

압축을 푼 이 폴더 이름을 `day06-닉네임`으로 바꾸고, Day 5의 `index.html`, `내정보.txt`, `CLAUDE.md` 세 파일을 안에 복사한 뒤 Claude Code Desktop의 Local 세션에서 연다.

Mac Finder에서는 `.claude` 폴더가 숨겨져 보이지 않을 수 있지만 ZIP 안에 이미 들어 있다. 삭제하거나 새로 만들지 않는다.

```text
day06-assets/
├── .claude/skills/openchat-proof/SKILL.md
├── input/result.json
├── scripts/build_card.py
├── output/
└── README.md
```

실행 명령은 운영체제에 따라 하나만 쓴다.

- Mac: `python3 scripts/build_card.py`
- Windows: `py scripts/build_card.py`

성공하면 `output/proof-card.html`이 생긴다. 외부 패키지와 API 키는 필요 없다.
