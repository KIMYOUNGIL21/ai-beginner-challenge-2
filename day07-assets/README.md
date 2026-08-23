# Day 7 배포 패키지

`ai-shorts/`는 운영 중인 `/ai-shorts` Skill 패키지를 그대로 복사한 기준본이다. 수강 중 코드를 새로 설계하지 않는다.

동기화 시각과 체크섬은 [`AI_SHORTS_VERSION.md`](AI_SHORTS_VERSION.md)에 기록했다.

`demo-project/`는 API 키와 유료 계정 없이 조립을 연습하는 시작 폴더다. 샘플 클립, 음성, 타임스탬프가 들어 있다.

## 설치 위치

이 폴더에서 Claude Code Desktop을 열고 다음 프롬프트를 보낸다.

```text
내 운영체제를 확인하고 install_mac.sh 또는 install_windows.ps1 중 맞는 것 하나만 실행해 주세요. 설치할 파일과 위치를 먼저 보여 주고 내 확인을 기다리세요.
```

설치 뒤 새 세션에서 `/ai-shorts`가 보이면 성공이다.

## 데모 실행

Mac:

```bash
cd demo-project
AI_SHORTS_DIR="$HOME/.claude/skills/ai-shorts"
"$AI_SHORTS_DIR/.venv/bin/python" "$AI_SHORTS_DIR/scripts/check.py" scenes.json
"$AI_SHORTS_DIR/.venv/bin/python" "$AI_SHORTS_DIR/scripts/build.py" scenes.json work/ --out D7_demo_쇼츠.mp4
```

Windows PowerShell:

```powershell
Set-Location demo-project
$aiShortsDir = Join-Path $HOME ".claude\skills\ai-shorts"
& (Join-Path $aiShortsDir ".venv\Scripts\python.exe") (Join-Path $aiShortsDir "scripts\check.py") scenes.json
& (Join-Path $aiShortsDir ".venv\Scripts\python.exe") (Join-Path $aiShortsDir "scripts\build.py") scenes.json work --out D7_demo_쇼츠.mp4
```

데모에는 Typecast 키가 필요 없다. `tts.py`를 실행하지 않고 제공 음성과 `words.json`을 사용한다.

장면 그래픽은 교재용으로 직접 만든 HTML/CSS 원본을 FFmpeg 모션 영상으로 바꾼 것이다. 외부 사진·영상·음악은 사용하지 않았다. 자세한 기록은 [`demo-project/licenses/SOURCES.md`](demo-project/licenses/SOURCES.md)에서 확인한다.
