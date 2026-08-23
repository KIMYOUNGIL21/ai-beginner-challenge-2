---
name: openchat-proof
description: 오늘 만든 결과와 배운 점을 받아 공개 가능한 오픈카톡 인증 카드로 만들 때 사용한다.
disable-model-invocation: true
---

# 오픈카톡 인증 카드 만들기

1. 프로젝트 루트의 `CLAUDE.md`를 먼저 읽고 Day 5에서 정한 대상·말투·금지 사항을 확인한다. 파일이 없으면 작업을 멈추고 사용자에게 알린다.
2. 사용자에게 다음 다섯 입력을 모두 확인한다: `닉네임`, `카드 제목`, `오늘 만든 것`, `오늘 배운 것`, `다음에 할 것`. 하나라도 없으면 추측하지 말고 빠진 항목만 질문한다.
3. 다섯 입력과 변경할 두 파일 `input/result.json`, `output/proof-card.html`을 표로 보여 주고 확인을 기다린다.
4. 확인 후 JSON의 `nickname`, `title`, `result`, `learned`, `next`를 모두 수정한다. `day`는 `Day 6`으로 유지한다. 전화번호, 이메일, API 키, 고객명은 넣지 않는다.
5. Python이나 Terminal을 사용하지 않는다. `output/proof-card.html`의 제목, 세 내용, 닉네임을 같은 다섯 입력으로 직접 바꾼다. HTML 구조와 스타일은 유지한다.
6. `output/proof-card.html`을 Browser pane에서 열고 다섯 입력이 모두 같은지 확인한다.
7. 샘플 값 `내닉네임`이나 다른 사람의 닉네임이 남지 않았는지, `CLAUDE.md`의 말투를 어기지 않았는지 확인한다.
8. 성공하면 결과 위치와 오픈카톡에 올릴 짧은 문구를 알려 준다.
9. 실패하면 파일을 삭제하거나 패키지를 설치하지 말고 오류 한 가지와 다음 확인 한 단계만 알려 준다.
