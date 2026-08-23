---
name: ai-shorts
description: Produce a 1-2 minute Korean YouTube Short end to end, and handle its setup - pick a topic, write the reversal-structure script, generate per-scene Google Flow prompts, synthesize narration with Typecast Timestamp TTS, and assemble the final 1080x1920 MP4 with burned-in subtitles via ffmpeg. Everything is automated except generating the clips in Flow, which the user does by hand. Use when the user asks for a 쇼츠/short, a video script with scene prompts, or wants to turn a topic into a finished vertical video. Also use for setup phrased in plain language - "쇼츠 만들 준비됐는지 확인해줘", "타임캐스트 키 등록해줘", "쇼츠 스킬을 어디서든 쓸 수 있게 설치해줘".
---

# AI 쇼츠 제작

주제 하나에서 완성된 9:16 MP4까지.

```
1 주제·대본 ─ 2 TTS ─ 3 씬 프롬프트 ─┤ 4 Flow 클립 생성 ├─ 5 배치 ─ 6 조립
              자동                       현재 수동          자동
```

**TTS를 씬 프롬프트보다 먼저 돌린다.** 씬 길이는 낭독 길이에서 나오지,
대본을 눈으로 읽고 추정할 수 있는 값이 아니다 — 예시 대본으로 실측했을 때
감으로 잡은 씬 길이가 실제 낭독보다 30% 가까이 짧았다. 순서를 뒤집으면 Flow 크레딧을
쓴 뒤에 길이가 안 맞는 걸 알게 된다.

**현재 손이 가는 건 4번뿐이다.** 그 앞은 전부 생성해 주고, 그 뒤는 전부
스크립트가 처리한다. 경계 양쪽을 매끄럽게 만드는 데 집중한다: **넘겨줄 땐
프롬프트를 붙여넣기 좋게, 받을 땐 파일 이름을 사람이 안 만지게.**

4번은 고정된 제약이 아니다. 사용자가 자동화를 원하면 **Veo API**(Gemini API로
같은 모델을 직접 호출)를 권한다 — 길이 지정, 파일명 직접 지정, 실패한 컷만
재시도가 되고, 앞 컷 마지막 프레임을 물려 연속성도 잡을 수 있다. `tts.py`,
`build.py`와 같은 결로 `flow.py`를 추가하면 된다. 단 Flow 크레딧과 API 청구는
별개다. 브라우저로 Flow UI를 직접 모는 방식도 가능하지만, 컷당 수 분에 재개가
안 되고 실패 시 크레딧을 날리므로 완전 자동보다 반자동을 권한다.
**어느 쪽이든 5·6번은 클립 출처와 무관하게 그대로 동작한다.**

## 0. 준비 요청 처리

설명서가 초보자에게 셸 명령 대신 평문으로 부탁하도록 안내한다.
아래 요청이 오면 **사용자에게 명령을 치게 하지 말고 직접 실행한다.**

### "쇼츠 만들 준비됐는지 확인해줘"

`scripts/setup.sh`를 실행하고 결과를 **평문으로** 옮긴다.
"ffmpeg", "Pillow" 같은 이름을 그대로 던지지 말고 무엇을 위한 것인지 붙인다.

빠진 게 있으면 **설치 명령을 사용자에게 넘기지 말고 직접 실행한다.**
Homebrew 설치처럼 사용자 확인이 필요한 것만 물어본다.
전부 통과하면 다음에 뭘 하면 되는지 한 줄로 알려준다.

### "타임캐스트 키 등록해줘: <키>"

`~/.zshrc`에 `TYPECAST_API_KEY`와 `TYPECAST_VOICE`를 추가한다
(보이스 기본값 `tc_69fc0cff784968297fb45daa`). 이미 있으면 값만 교체한다.
현재 세션에서도 쓰도록 환경변수를 설정하고, `setup.sh`로 확인한다.

**키를 대화에 다시 출력하지 않는다.** 등록됐다는 사실만 알린다.

### "쇼츠 스킬을 어디서든 쓸 수 있게 설치해줘"

`~/.claude/skills/`를 만들고 이 스킬 폴더를 복사한 뒤 `setup.sh`를 돌린다.
기본은 프로젝트 폴더 안에서 그냥 동작하므로 **이 요청이 오기 전에 먼저
권하지 않는다.**

## 1. 주제와 대본

`references/prompt-formula.md`의 **반전 구조**를 따른다. 요약하면:

1. 현재 방식의 실패를 단언한다 (훅)
2. 흔한 해결책 두세 개를 차례로 무너뜨린다
3. "그런데 X는, 애초에 ~할 생각이 없었습니다" 로 뒤집는다
4. 진짜 메커니즘을 보여준다 (영상의 핵심)
5. 대구로 닫는다 — "우리는 A를 원했고, X는 B를 만들었습니다"

한 문장 = 한 호흡으로 쓴다. 그 문장 경계가 그대로 자막 단위가 된다.
`script.txt`로 저장한다.

## 2. 내레이션 — Typecast Timestamp TTS

```bash
export TYPECAST_API_KEY=...        # studio.typecast.ai/developers/api
python3 scripts/tts.py script.txt work/ --voice tc_xxxxxxxx
```

`work/narration.wav` + `work/words.json`(단어별 start/end)이 나온다.

타임스탬프는 **합성 과정에서 나온 값**이므로 STT/Whisper 정렬은 쓰지 않는다.
목소리를 직접 녹음한 경우에만 별도 정렬이 필요하다.

보이스 고르기: 원하는 톤을 문장으로 설명해
`GET /v1/voices/recommendations?query=...`로 후보를 받는다. 응답은
`voice_id`/`voice_name`/`score`만 주므로, 고르기 전에 `GET /v2/voices/{id}`로
모델·감정 지원 여부를 확인한다. 전체 탐색은 `GET /v2/voices`.

`words.json`의 문장 시작 시각이 다음 단계의 컷 경계가 된다.

```bash
python3 -c "
import json
w=json.load(open('work/words.json')); seen=set()
for x in w:
    if x['sentence'] not in seen:
        seen.add(x['sentence']); print(f\"{x['start']:6.2f}s  {x['text']}\")"
```

## 3. 씬 프롬프트 — 넘겨주는 쪽

`references/prompt-formula.md`의 프롬프트 문법과 씬 배치표를 적용한다.

**기본은 6컷이다.** 사용자가 더 길게 요청하지 않는 한 6컷으로 잡는다 —
11컷이면 Flow 대기만 30분이 넘어 첫 편을 완주하지 못한다. 6컷이어도
훅 / 전환 / 핵심 쌍 / 대구 엔딩이라는 뼈대는 그대로 산다.

늘려 달라고 하면 새 아이디어를 넣지 말고 **기존 컷을 쪼갠다**
(`prompt-formula.md`의 "늘리려면").

두 개를 만든다.

**`prompts.md`** — 사람이 Flow에 붙여넣을 것. 씬마다 이 형식으로:

````
### C4 · 8초 생성 → 6.8초 사용 · 연쇄 4단
```
(프롬프트 전문 — 코드블록에 넣어 복사가 한 번에 되게)
```
````

씬 번호와 **생성 길이**를 제목에 적는다. Flow에서 길이를 그걸로 맞춘다.

**`scenes.json`** — 생성 길이가 아니라 **사용 길이**를 적는다. 값은 2번에서
나온 문장 시작 시각의 차이로 정한다 (컷을 문장 중간이 아니라 시작점에 맞춰야
전환과 말이 같이 떨어진다):

```json
[{"file": "clips/c01.mp4", "use": 4.2},
 {"file": "clips/c08.mp4", "use": 7.1}]
```

합계가 내레이션 길이와 맞는지 확인한다. 안 맞으면 Flow에서 다시 뽑아야 한다.

그리고 사용자에게 안내한다: [Flow](https://labs.google/fx/ko/tools/flow)에서
**C1부터 순서대로** 생성하고 받은 파일은 이름 그대로 두라고. 순서만 지키면
다음 단계가 알아서 맞춘다.

## 4. Flow 클립 생성

여기서 멈추고 기다린다. 사용자가 다 받았다고 하면 5번으로 간다.

사용자가 이 단계를 자동화하고 싶어 하면 위의 Veo API 경로를 제안한다 —
막아서지 말 것.

## 5. 배치 — 받는 쪽

```bash
python3 scripts/ingest.py scenes.json          # 미리보기
python3 scripts/ingest.py scenes.json --apply
```

`~/Downloads`의 최근 영상 파일을 받은 순서대로 빈 씬에 채운다. 옮기기 전에
씬별 길이와 필요 길이를 표로 보여주고, 짧은 클립은 배치하지 않는다.

- 쓸 만한 것만 배치하고 나머지는 "다시 생성 필요"로 알린다
- 배치한 파일과 거부한 파일을 `.ingest.json`에 기록하므로, Flow에서 다시 받아
  같은 명령을 실행하면 순서가 밀리지 않고 재생성분이 제자리에 들어간다
- 순서가 꼬였으면 `--map 7=~/Downloads/foo.mp4`로 개별 지정
- 원본은 복사만 하고 지우지 않는다

```bash
python3 scripts/check.py scenes.json
```

무엇이 남았는지 한 번에 보여준다. `4/4 준비됨`이 나오면 다음으로 간다.

## 6. 조립

```bash
.venv/bin/python scripts/build.py scenes.json work/ --out short.mp4
```

각 클립을 사용 길이로 자르고 → 1080x1920으로 크롭 → 이어붙이고 →
내레이션을 깔고 → `words.json` 타이밍으로 자막을 태워 넣는다.

영상 길이와 내레이션 길이가 1초 넘게 어긋나면 경고가 뜬다. 그때
`scenes.json`의 `use` 값을 조정한다.

## 한 번에 돌리기

4~6번을 순서대로 실행하는 래퍼가 있다. 사용자가 클립을 다 받았다고 하면
개별 스크립트 대신 이걸 써도 된다.

```bash
scripts/make-short.sh [프로젝트폴더]
```

폴더에 `script.txt`와 `scenes.json`만 있으면 된다. 중간에 멈추면 무엇이
부족한지 알려주고, 고친 뒤 같은 명령을 다시 실행하면 이어서 간다.
이미 만든 내레이션은 재사용한다 — TTS는 크레딧이 나가므로 다시 만들려면
`FORCE_TTS=1`. 다운로드 폴더가 `~/Downloads`가 아니면 `DOWNLOADS=경로`.

처음 쓰는 환경이면 `scripts/setup.sh`를 먼저 한 번 실행한다.

## 전제 조건

- `ffmpeg` / `ffprobe`
- 자막용: libass 빌드 ffmpeg **또는** Pillow. Homebrew ffmpeg 9는 libass가 없어
  Pillow 경로로 떨어진다 — `python3 -m venv .venv && .venv/bin/pip install pillow`
  후 `build.py`를 `.venv/bin/python`으로 실행한다.
- `TYPECAST_API_KEY` (웹 플랜과 별도인 **API 플랜** 필요)

## 주의

- Typecast 무료 다운로드는 상업적 이용 불가. 수익 창출 채널이면 유료 플랜을 쓴다.
- 씬 프롬프트 끝에 "한글이나 한국어 문자는 넣지 않는다"를 항상 붙인다.
  Flow가 화면에 글자를 그려 넣으면 자막과 충돌한다.
