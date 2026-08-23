# Day 6 — 내 일을 기억하는 Skill + 자료를 가져오는 Connector

오늘은 긴 프롬프트를 외우지 않는다. 제공된 **Skill을 한 번 실행해 눈에 보이는 인증 카드**를 만들고, Connector로 내 자료 하나를 읽어 그 카드의 근거로 연결한다.

> Skill은 반복 작업 설명서이고, Connector는 Google Drive·Notion 같은 외부 서비스와 Claude를 연결하는 통로다. Skill에 비밀번호나 API 키를 쓰지 않는다.

## 기능과 정확한 위치

| 기능 | 쉬운 뜻 | Claude Desktop에서 찾는 곳 |
|---|---|---|
| Skill | 다시 부를 수 있는 작업 설명서 | Code 입력창에서 `/`, 또는 입력창 옆 **`+ → Slash commands`** |
| Connector | Drive·Notion 같은 외부 서비스 연결 | **Local Code 세션** 입력창 옆 **`+ → Connectors`** |
| Manual 권한 | 파일 변경·명령 전에 내가 확인 | 입력창 옆 권한 모드 메뉴의 **Manual(구 Ask permissions)** |
| Browser pane | HTML 결과를 실제로 누르고 보는 창 | 채팅의 HTML 경로 클릭, 또는 **Views → Browser** |
| 새 세션 | 이전 대화 없이 Skill이 작동하는지 시험 | Mac `Cmd+N`, Windows `Ctrl+N`, 또는 새 세션 버튼 |

## 교재에 넣을 화면 캡처 목록

아래 이미지는 현재 실제 Claude Desktop 화면이다. `① Code`, `② Local`, `③ 프로젝트 폴더`, `④ Manual` 순서로 찾는다.

![Local 프로젝트 폴더와 Manual 권한 위치](day06-assets/screenshots/01-local-manual.png)

그다음 클릭 순서는 다음과 같다.

1. Skill: 입력창 옆 `+` → **Slash commands** → `openchat-proof`.
2. Connector: 입력창 옆 `+` → **Connectors** → Google Drive 또는 Notion.
3. 변경 확인: 변경 대상이 `input/result.json`인지 확인 → 승인 또는 거절.
4. 결과 확인: 채팅의 `output/proof-card.html` 경로 클릭 → Browser pane.

Skill·Connector·승인·결과 화면의 추가 캡처는 운영자가 개강 직전 실제 수강생 계정으로 찍는다. 촬영 전까지 존재하지 않는 이미지를 교재에서 불러오지 않는다.

## 오늘 끝나면 남는 것

![Day 6 Skill이 반복해서 만들어 주는 인증 카드의 실제 완성 예시](day06-assets/expected/proof-card-example.png)

[완성 예시 인증 카드를 큰 화면으로 열기](day06-assets/output/proof-card.html)

- `output/proof-card.html`과 휴대폰 캡처 1장
- 내 프로젝트의 `.claude/skills/openchat-proof/SKILL.md`
- Connector에서 읽은 자료의 `제목 + 서비스 이름 + 내가 쓸 점 1줄`
- `/openchat-proof` 실행부터 결과 확인까지 30초 영상

Connector 연결이 계정 정책 때문에 안 되면 **Skill 결과물까지가 기본 완주**다. 연결 성공은 별도 배지로 표시한다. 연결 실패 때문에 결과물을 못 내는 수업으로 만들지 않는다.

## 3시간 시간표

| 순서 | 시간 | 하는 일 | 눈에 보이는 성공 |
|---|---:|---|---|
| 기능 이해 | 20분 | Skill과 Connector 차이 보기 | 어느 쪽이 절차이고 어느 쪽이 연결인지 말한다 |
| 작은 결과 | 30분 | 기준 입력으로 카드 만들기 | Browser pane에 샘플 카드가 열린다 |
| 메인 결과 | 60분 | `/openchat-proof`로 내 카드 만들기 | 내 내용의 HTML이 생긴다 |
| Connector | 35분 | 내 자료 하나를 읽어 출처 메모 만들기 | 제목·서비스·활용점이 기록된다 |
| 자기 응용 | 20분 | Skill의 질문/완료 조건 하나 바꾸기 | 새 세션에서도 바뀐 순서를 따른다 |
| 검수·인증 | 15분 | 개인정보 확인 후 캡처·영상 | 오픈카톡에 바로 올릴 수 있다 |

## 시작 전 확인

1. [Day 6 시작 자료 ZIP을 받는다](downloads/day06-start.zip). 압축을 풀고 `day06-assets` 폴더 이름을 `day06-닉네임`으로 바꾼다.
2. Claude Desktop을 최신 버전으로 업데이트한다. Mac은 **Claude → Check for Updates**, Windows는 **Help → Check for Updates**다.
3. Day 5 폴더에서 `index.html`, `내정보.txt`, `CLAUDE.md` 세 파일만 `day06-닉네임` 안으로 복사한다. 같은 이름이 있으면 덮어쓰기 전에 운영자에게 확인한다.
4. Mac Finder에서는 이름이 점으로 시작하는 `.claude` 폴더가 숨겨져 보이지 않을 수 있다. ZIP 안에 이미 들어 있으므로 새로 만들거나 옮길 필요가 없다.
5. Claude Desktop의 **Code → Local → 폴더 선택**에서 복사본을 연다.
6. 권한은 **Manual(구 Ask permissions)**을 고른다.
6. Windows에서 Code가 처음 열리지 않으면 [Git for Windows](https://git-scm.com/download/win)를 설치하고 Claude 앱을 완전히 종료한 뒤 다시 연다.

`CLAUDE.md`에는 Day 5 웹 도구의 이름, 대상, 말투, 금지 사항이 들어 있어야 한다. 없으면 Day 5가 끝난 것이 아니므로 운영자에게 Day 5 보충 안내를 받고 먼저 만든다. Day 6 Skill은 이 파일을 읽어 전날 기준을 유지한다.

## 1. 기능 이해 — 20분

| 기능 | 쉬운 뜻 | 오늘 하는 행동 |
|---|---|---|
| `CLAUDE.md` | Day 5 웹 도구의 대상·말투·금지 사항 | 전날 만든 기준을 Skill 결과에도 유지한다 |
| Skill | 필요할 때 부르는 작업 순서 | `/openchat-proof`로 카드를 만든다 |
| Connector | 외부 자료를 읽거나 작업하는 연결 | Drive/Notion에서 공개 가능한 자료 하나를 읽는다 |

공식 문서가 말하는 프로젝트 Skill 위치는 `.claude/skills/<이름>/SKILL.md`다. 채팅 입력창에서 `/`를 입력하거나 `+ → Slash commands`에서 실행한다.

## 2. 작은 결과 — 기준 카드 1장

파일을 바꾸기 전에 통합 Terminal을 연다. 메뉴에서 **Views → Terminal**, 또는 Mac·Windows 모두 `Ctrl`+`` ` ``를 누른다.

Mac:

```bash
python3 scripts/build_card.py
```

Windows:

```powershell
py scripts/build_card.py
```

`완성: output/proof-card.html`이 보이면 채팅의 파일 경로를 누르거나 파일 목록에서 열어 Browser pane으로 본다.

**성공 화면:** 검은 카드에 `Day 6 COMPLETE`, 오늘 만든 것, 배운 것, 다음 할 것이 보인다.

Python을 찾을 수 없으면 임의 설치하지 말고 운영자에게 `Day 6 / Python 없음 / Mac 또는 Windows`라고 알린다. 운영자는 설치된 기준 컴퓨터와 시작 폴더를 개강 전에 확인해야 한다.

## 3. 메인 결과 — Skill을 직접 실행

1. 입력창에 `/`를 쓴다.
2. `openchat-proof`를 선택한다. 안 보이면 같은 프로젝트 폴더인지 확인하고 새 Code 세션을 연다.
3. 아래 한 줄에서 대괄호 세 곳만 바꾼다.

```text
/openchat-proof 오늘 만든 것: [AI 초보자용 카드뉴스 5장], 오늘 배운 것: [입력 파일을 바꾸고 같은 명령으로 다시 만드는 법], 다음에 할 것: [내 강의 주제로 한 번 더 실행]
```

4. Skill이 `input/result.json` 변경 계획을 보여 주면 실제 내 말과 같은지 본다.
5. 허용 화면에는 오늘 폴더 안의 `input/result.json`만 있는지 확인한다.
6. 실행 명령을 허용한다.
7. `output/proof-card.html`을 Browser pane에서 연다.
8. Claude에게 다음을 보낸다.

```text
Browser pane에서 proof-card.html을 직접 확인해 주세요. 제목, 닉네임, 세 내용이 input/result.json과 같은지 검사하고, 화면이 휴대폰 폭에서도 읽히는지 확인해 주세요. 문제가 있으면 최소 변경으로 고친 뒤 다시 확인해 주세요.
```

이 단계의 핵심은 Claude가 파일만 만들고 “됐습니다”라고 말하는 데서 끝내지 않고, Browser pane에서 실제 화면을 검사하는 것이다.

## 4. Connector — 내 자료 하나만 안전하게 읽기

### 연결

1. **Local 세션**인지 확인한다. Cloud/Remote 세션에서는 `+` Connector 메뉴가 보이지 않을 수 있다.
2. 입력창 옆 `+` → **Connectors**를 누른다.
3. 자신이 이미 쓰는 서비스 하나만 고른다. 권장 순서는 Google Drive 또는 Notion이다.
4. 로그인 화면에서 요청 권한을 읽는다. 수업용이 아닌 회사·고객 계정은 연결하지 않는다.
5. 연결 뒤 채팅에 `현재 이 세션에서 사용 가능한 Connector 이름만 알려 줘. 아무 파일도 수정하지 마.`라고 보낸다.

### 읽기 전용 미션

공개해도 되는 본인 자료 하나를 정하고 아래를 보낸다.

```text
연결된 [Google Drive 또는 Notion]에서 제목에 [검색어]가 들어간 내 자료를 찾아 주세요.
읽기 전용으로만 작업하고 수정·공유·삭제하지 마세요.
후보가 여러 개면 제목만 보여 주고 내 선택을 기다리세요.
선택한 자료에서 다음 세 가지만 connector-note.md에 저장하세요.
1. 자료 제목
2. 서비스 이름
3. Day 6 인증 카드에 활용할 수 있는 점 한 줄
개인정보와 원문 본문은 복사하지 마세요.
```

**성공 화면:** 프로젝트 파일 목록에 `connector-note.md`가 있고, 외부 자료 전체가 아닌 세 줄만 있다.

Connector가 없거나 연결을 원치 않으면 다음 대체 과제를 한다.

```text
공식 Claude Code Desktop 문서를 Browser pane에서 열고 Skills와 Connectors 부분만 읽어 주세요.
문서 제목, 공식 URL, 내가 오늘 사용한 기능 한 줄을 connector-note.md에 적어 주세요.
```

대체 과제는 Connector 사용 배지가 아니지만 Day 6 기본 완주에는 포함된다.

## 5. 자기 주제 응용

`SKILL.md`를 직접 열어 아래 중 하나만 바꾼다.

- 마지막에 질문할 항목 하나 추가
- 공개 전 확인할 개인정보 항목 하나 추가
- 내 업종에 맞는 결과 파일명 규칙 추가

바꾼 뒤 새 세션에서 `/openchat-proof`를 다시 실행한다. 이전 대화가 아니라 Skill 파일의 새 규칙을 따르는지 본다.

## 완료 판정

- [ ] 기준 입력으로 `proof-card.html`이 만들어졌다.
- [ ] `/openchat-proof`를 직접 골라 내 내용으로 다시 만들었다.
- [ ] Browser pane에서 Claude가 화면을 실제 검사했다.
- [ ] Skill 파일의 위치와 역할을 내 말로 설명할 수 있다.
- [ ] Connector 또는 공식문서 대체 경로로 `connector-note.md`를 만들었다.
- [ ] 새 세션에서도 Skill이 수정한 순서를 따른다.
- [ ] 카드·녹화에 이메일, 파일 경로, API 키, 고객 정보가 없다.

첫 세 항목 중 하나라도 빠지면 다시 한다. Connector 연결 자체는 계정 상태에 따라 선택이지만, 어떤 자료를 읽었는지 출처 메모는 반드시 남긴다.

## 막혔을 때

| 증상 | 한 번만 할 조치 |
|---|---|
| Skill이 목록에 없음 | 프로젝트 루트에 `.claude/skills/openchat-proof/SKILL.md`가 있는지 확인하고 새 세션 |
| `python3`/`py` 없음 | 다른 명령을 추측하지 말고 OS와 화면을 운영자에게 전달 |
| Connector 메뉴 없음 | Local 세션과 앱 업데이트 확인; 계속 없으면 공식문서 대체 과제 |
| 외부 자료 후보가 너무 많음 | 날짜나 제목 단어 하나를 더 주고, 제목만 보게 한다 |
| Claude가 자료를 수정하려 함 | 거절하고 `읽기 전용, 제목과 활용점만`으로 다시 요청 |
| 카드가 이전 내용임 | `input/result.json` 저장 여부와 출력 파일 수정 시간을 확인 |

## 오픈카톡 인증

```text
[왕초보2기 Day 6 / 닉네임]
오늘 만든 것: /openchat-proof로 만든 내 인증 카드
Skill이 반복한 순서: 입력 확인 → 카드 생성 → 화면 검수
Connector: Google Drive 연결 성공 / Notion 연결 성공 / 공식문서 대체
읽은 자료: 제목만 적기
결과물: 카드 캡처 + 30초 Skill 실행 영상
내일 넘길 주제: __________
```

## 공식 레퍼런스와 실제 활용 예

- [Claude Code Desktop 공식 문서](https://code.claude.com/docs/en/desktop): `+` 메뉴의 Skills·Connectors, Local 세션, Browser pane, 권한 모드.
- [Claude Code Skills 공식 문서](https://code.claude.com/docs/en/slash-commands): 프로젝트 Skill 구조와 `/skill-name` 실행.
- [Claude Code 확장 기능 개요](https://code.claude.com/docs/en/features-overview): CLAUDE.md는 항상 적용되는 규칙, Skill은 필요할 때 불러오는 절차, MCP/Connector는 외부 연결이라는 구분.
- [Anthropic 공식 활용 예—반복 프롬프트를 Skill로](https://code.claude.com/docs/en/communications-kit): Git 기록을 매일 요약하는 `/standup` 같은 반복 작업이 Skill에 적합한 사례.
