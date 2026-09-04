# Day 6 — `/shorts-brief` 한 번으로 숏츠 주문서 만들기

오늘은 **Skill**을 사용해 숏츠 주문서를 만들어요. Skill은 같은 일을 같은 순서로 처리하도록 저장한 작업 순서표예요. `/shorts-brief`를 입력하면 첫 문장 3개와 장면 5개의 계획이 나옵니다. 만든 파일 두 개는 Day 7에서 사용해요.

예상 시간은 약 1시간이에요.

## 오늘 만드는 것

![Skill이 만든 5컷 숏츠 주문서 완성 예시](day06-assets/expected/shorts-brief-example.png)

[완성 주문서 크게 보기](day06-assets/output/shorts-brief.html)

[먼저 한 장으로 전체 순서 보기](Day06_나만의스킬.md)

- 첫 1~2초에 시선을 끌 문장(`훅`) 3개
- 장면(`컷`) 5개의 주문서 — 장면마다 한 문장, 전체 20~23초
- Day 7에 쓸 파일 2개: `input/brief.json`, `output/shorts-brief.html`

`brief.json`은 Claude가 다음 작업에서 읽을 정보 파일이에요. `shorts-brief.html`은 브라우저로 열어 보는 주문서 화면이에요.

> 오늘 적는 초는 **계획**이에요. 실제 낭독 시간은 Day 7에서 목소리를 만든 뒤 자동으로 다시 재요.

## 1단계 — 시작 폴더 열기

`ZIP`은 여러 파일을 한 묶음으로 줄여 놓은 압축 파일이에요.

![Code 로컬, 폴더 선택 위치](day06-assets/screenshots/01-local-manual.png)

1. [Day 6 시작 자료 ZIP](downloads/day06-start.zip)을 받으세요.
2. Windows는 받은 ZIP 파일을 마우스 오른쪽으로 누르고 **모두 압축 풀기**를 누르세요. Mac은 ZIP 파일을 두 번 누르세요.
3. 압축을 풀면 생기는 `day06-assets` 폴더의 이름을 `Day06_Skill_닉네임`으로 바꾸세요. 새 폴더를 만들지 마세요.
4. 이름을 바꾼 폴더를 여세요.
5. `shorts-brief-maker.html`이 바로 보이는지 확인하세요.
6. 파일이 또 다른 폴더 안에 있으면 그 안쪽 폴더를 바탕 화면으로 옮기세요. 안쪽 폴더의 이름을 `Day06_Skill_닉네임`으로 바꾸세요.
7. Claude Desktop에서 **Code → 로컬 → 폴더 선택…**을 누르세요.
8. `shorts-brief-maker.html`이 바로 보였던 `Day06_Skill_닉네임` 폴더를 고르세요.

아래 문장을 보내세요.

```text
파일은 바꾸지 말고, 지금 열린 폴더 이름과 /shorts-brief Skill이 있는지만 알려 주세요.
```

**이렇게 되면 성공:** 폴더 이름과 함께 "shorts-brief Skill이 있습니다"라는 답이 와요.

## 2단계 — 완성 모양 미리 구경하기 (1분)

먼저 완성 화면을 확인하세요.

1. Finder 또는 파일 탐색기에서 `shorts-brief-maker.html`을 두 번 누르세요.
2. 화면 왼쪽의 **작은 연습 · 얼음 예시 한 번에 넣기**를 누르세요.
3. 오른쪽 5컷이 얼음 이야기로 바뀌는지 보세요.

**이렇게 되면 성공:** 오른쪽 장면 5개가 얼음 이야기로 바뀌어요. 다른 버튼은 누르지 말고 창을 닫으세요.

## 3단계 — `/shorts-brief` 실행하기

Code 입력창에 아래를 그대로 붙여 넣고 보내세요. 첫 줄의 `/shorts-brief`가 Skill을 부르는 말이에요.

```text
/shorts-brief
주제: 한옥 처마가 여름빛은 막고 겨울빛은 들이는 이유
대상: 생활 속 설계 원리가 궁금한 사람
눈으로 보여 줄 대비: 같은 처마에서 여름의 높은 햇빛은 막히고 겨울의 낮은 햇빛은 안으로 들어온다
마지막 한마디: 긴 처마는 햇빛을 전부 막는 지붕이 아니라 계절에 따라 빛을 고르는 장치다
말투: 짧고 또렷한 다큐멘터리 톤
```

> **내 주제로 만들기(선택):** 각 줄에서 `:` 뒤의 내용만 바꾸세요. 예시를 그대로 보내도 돼요.

Claude가 첫 문장 3개와 장면 5개의 계획을 보여 줘요. 내용을 확인한 뒤 아래 문장을 보내세요.

```text
추천 훅으로 진행해 주세요. input/brief.json과 output/shorts-brief.html 두 파일만 만들어 주세요.
```

**이렇게 되면 성공:** "두 파일을 만들었습니다"라는 답이 와요.

## 4단계 — 결과 확인하기

1. 폴더의 `output` 안에 있는 `shorts-brief.html`을 두 번 눌러 브라우저로 여세요.
2. **제목, 훅 3개, 장면 번호 C1부터 C5까지**가 보이는지 확인하세요.
3. 마지막으로 Claude에게 검사를 맡기세요.

```text
input/brief.json을 바꾸지 말고 검사만 해 주세요.
컷이 C1부터 C5까지 5개 있는지, 계획한 초를 모두 더하면 20~23초인지 알려 주세요.
```

**이렇게 되면 성공:** "5컷, 20~23초 맞습니다"라는 답이 와요.

틀렸다는 답이 오면 이렇게 보내세요.

```text
틀린 부분만 고치고, 같은 검사를 다시 해 주세요.
```

## 5단계 — Day 7에 쓸 폴더 만들기

`handoff`는 다음 날 작업으로 넘긴다는 뜻이에요.

1. Finder 또는 파일 탐색기에서 `Day06_Skill_닉네임` 폴더를 여세요.
2. 빈 곳에서 마우스 오른쪽 버튼을 누르세요.
3. Windows는 **새로 만들기 → 폴더**, Mac은 **새로운 폴더**를 누르세요.
4. 폴더 이름을 `day06-handoff`로 적으세요.
5. `input` 폴더를 열고 `brief.json`을 한 번 누르세요.
6. Windows는 `Ctrl+C`, Mac은 `Command+C`를 누르세요.
7. `day06-handoff` 폴더를 열고 Windows는 `Ctrl+V`, Mac은 `Command+V`를 누르세요.
8. 같은 방법으로 `output` 폴더의 `shorts-brief.html`도 복사해 `day06-handoff` 안에 붙여넣으세요.

Day 7 시작 자료를 받은 뒤 이 `day06-handoff` 폴더를 `day07-start` 폴더 안으로 옮기세요. 같은 이름의 폴더가 있다는 창이 뜨면 `대체` 또는 `병합`을 누르세요.

> Day 7에서는 `brief.json`의 내용을 사용해 대본을 만들어요.

**이렇게 되면 성공:** `day06-handoff` 폴더 안에 `brief.json`과 `shorts-brief.html` 두 파일이 보여요.

## 오픈카톡 인증 — 30초

📸 **인증 캡처:** 완성된 숏츠 주문서 화면 1장

```text
[왕초보3기 Day 6 / 닉네임]
✅ 20~23초·5컷 숏츠 주문서 완성
💬 소감:
```

## 끝났는지 확인해요

- [ ] `/shorts-brief`를 실행해 훅 3안과 5컷을 받았다.
- [ ] `shorts-brief.html`을 브라우저로 열어 봤다.
- [ ] 검사에서 "5컷, 20~23초"를 확인했다.
- [ ] `day06-handoff` 폴더에 두 파일을 넣었다.

## 막혔을 때

| 보이는 상황 | 바로 할 일 |
|---|---|
| "shorts-brief Skill이 없습니다"라는 답 | 지금 연 폴더 안에 `shorts-brief-maker.html`이 **바로** 보이는지 Finder/탐색기에서 확인하세요. 또 다른 폴더 속에 있으면 1단계 6번대로 꺼낸 뒤, Code에서 그 폴더를 다시 여세요. |
| Skill이 설명만 하고 파일을 안 만듦 | `설명은 됐으니 input/brief.json과 output/shorts-brief.html 두 파일을 실제로 만들어 주세요` 보내기 |
| 검사에서 컷 수나 초가 틀림 | `틀린 부분만 고치고 같은 검사를 다시 해 주세요` 보내기 |
| 브라우저 화면과 채팅 결과가 다름 | `output/shorts-brief.html을 input/brief.json과 같은 내용으로 맞춰 주세요` 보내기 |
| 폴더 복사가 어려움 | Claude에게 `day06-handoff 폴더를 만들고 input/brief.json과 output/shorts-brief.html을 그 안에 복사해 주세요` 보내기 |

## 공식 참고

- [Claude Code Desktop 공식 문서](https://code.claude.com/docs/en/desktop)
- [Claude Code Skills 공식 문서](https://code.claude.com/docs/en/slash-commands)
