# Day 6 한 장 실행표 — `/shorts-brief`

Skill은 완성 파일을 넣어 두는 상자가 아니라 **Claude가 새 채팅에서도 반복할 작업 순서**입니다.

## 네 단계

1. **기능 공부:** `CLAUDE.md`·Skill·커넥터를 구분합니다.
2. **작은 성공:** `shorts-brief-maker.html`에서 주제 한 줄을 바꿔 5컷을 움직입니다.
3. **완성 결과:** `/shorts-brief`로 훅 3안과 20~23초·5컷 주문서를 만듭니다.
4. **연결:** `shorts-brief-v1` JSON을 검사해 Day 7로 넘깁니다.

## Skill 호출에 필요한 다섯 가지

```text
/shorts-brief
주제: __________
대상: __________
눈으로 보여 줄 대비: __________
마지막 한마디: __________
말투: __________
```

## Skill 파일에서 확인할 것

- 위치: `.claude/skills/shorts-brief/SKILL.md`
- 빠진 입력을 추측하지 않고 질문한다.
- 훅 3안과 C1~C5를 먼저 제안하고 승인을 기다린다.
- 컷마다 내레이션은 한 문장, 계획상 5초 이하이다.
- `input/brief.json`과 `output/shorts-brief.html`만 만든다.
- JSON은 `shorts-brief-v1`, C1~C5, 계획 합계 20~23초이다.
- 외부 설치와 API를 요구하지 않는다.

## 결과물

- 훅 3개와 5컷이 한 화면에 보이는 `shorts-brief.html`
- Day 7이 읽을 `brief.json`
- 두 파일을 복사한 `day06-handoff` 폴더
- 캡처 `D06_닉네임_숏츠주문서.png`

## 30초 안에 찍는 인증 동선

1. `/shorts-brief`와 내 다섯 입력을 보여 줍니다.
2. Skill이 만든 훅 3안을 보여 줍니다.
3. 완성 HTML의 C1~C5를 보여 줍니다.
4. JSON 검사 결과 `shorts-brief-v1 / 5컷 / 20~23초`를 보여 줍니다.

전체 버튼 위치·프롬프트·복구법은 [Day06 Skills 실행서](Day06_Skills_Connectors_실행서_v2.md)를 따릅니다.
