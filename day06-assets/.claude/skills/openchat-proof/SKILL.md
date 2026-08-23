---
name: openchat-proof
description: 오늘 만든 결과와 배운 점을 받아 공개 가능한 오픈카톡 인증 카드로 만들 때 사용한다.
disable-model-invocation: true
---

# 오픈카톡 인증 카드 만들기

1. 프로젝트 루트의 `CLAUDE.md`를 먼저 읽고 Day 5에서 정한 대상·말투·금지 사항을 확인한다. 파일이 없으면 작업을 멈추고 사용자에게 알린다.
2. 사용자에게 `오늘 만든 것`, `오늘 배운 것`, `다음에 할 것`을 확인한다. 없는 내용을 추측하지 않는다.
3. `input/result.json`의 값만 바꿀 계획을 먼저 보여 주고 확인을 기다린다.
4. 확인 후 JSON을 수정한다. 전화번호, 이메일, API 키, 고객명은 넣지 않는다.
5. 운영체제를 확인해 Mac은 `python3 scripts/build_card.py`, Windows는 `py scripts/build_card.py`를 실행한다.
6. `output/proof-card.html`이 존재하는지 확인하고 Browser pane에서 연다.
7. 제목, 닉네임, 세 내용이 실제 입력과 같은지, `CLAUDE.md`의 말투를 어기지 않았는지 확인한다.
8. 성공하면 결과 위치와 오픈카톡에 올릴 짧은 문구를 알려 준다.
9. 실패하면 파일을 삭제하거나 패키지를 설치하지 말고 오류 한 가지와 다음 확인 한 단계만 알려 준다.
