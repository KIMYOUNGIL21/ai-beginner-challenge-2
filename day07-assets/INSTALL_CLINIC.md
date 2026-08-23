# Day 7 사전 설치 클리닉

이 문서는 **수강생 혼자 하는 숙제**가 아닙니다. 운영자가 화면을 함께 보면서 Day 7 전날까지 끝냅니다. 목표는 설치 방법을 외우는 것이 아니라 아래 네 줄을 확인하는 것입니다.

```text
Python 준비 완료
FFmpeg 준비 완료
FFprobe 준비 완료
Skill 설치 완료
```

## 1. 먼저 읽기 전용으로 확인

Claude Desktop에서 `day07-start` 폴더를 **Code → 로컬 → 폴더 선택… → 수동**으로 열고 다음 문장을 보냅니다.

```text
파일을 바꾸거나 설치하지 말고 PRECHECK_MAC.md 또는 PRECHECK_WINDOWS.md를 읽어 주세요.
내 운영체제에서 Python, FFmpeg, FFprobe가 준비됐는지만 확인하고
'준비됨' 또는 '없음'으로 표를 보여 주세요.
```

세 항목이 모두 준비됐으면 4번으로 갑니다. 하나라도 없으면 운영자와 아래 OS별 경로를 진행합니다.

## 2. Mac — 운영자와 함께

1. Safari/Chrome에서 [Homebrew 공식 홈페이지](https://brew.sh/)를 엽니다.
2. 홈페이지의 **Install Homebrew** 명령을 복사합니다. 다른 블로그의 명령은 쓰지 않습니다.
3. Mac의 **Terminal**을 열고 붙여넣은 뒤 Return을 누릅니다.
4. Mac 로그인 암호를 묻는다면 수강생이 직접 입력합니다. 입력 중 글자가 안 보여도 정상이며, 암호를 운영자에게 보내지 않습니다.
5. 설치 마지막에 `Next steps`가 나오면 화면의 PATH 명령을 그대로 실행합니다.
6. Terminal을 닫았다가 다시 열고 `brew --version`을 실행합니다.
7. 버전 번호가 보이면 `brew install python ffmpeg`를 실행합니다.
8. 설치 뒤 Terminal을 닫았다가 다시 열고 `python3 --version`, `ffmpeg -version`, `ffprobe -version`을 차례로 확인합니다.

오류가 나면 같은 설치를 반복하지 말고 화면 전체를 운영자에게 보여 줍니다.

## 3. Windows — 운영자와 함께

Windows 설치 경로는 운영자가 **실제 Windows 교육용 컴퓨터에서 먼저 리허설한 뒤** 사용합니다.

1. 시작 메뉴에서 **PowerShell**을 엽니다.
2. `winget --version`을 실행해 Windows 패키지 관리자가 있는지 확인합니다.
3. 준비돼 있다면 운영자가 아래 두 패키지 이름과 게시자를 화면에서 다시 확인한 뒤 한 줄씩 실행합니다.

```powershell
winget install --exact --id Python.Python.3.12
winget install --exact --id Gyan.FFmpeg
```

4. PowerShell을 완전히 닫았다가 다시 엽니다.
5. `py --version`, `ffmpeg -version`, `ffprobe -version`을 차례로 확인합니다.

`winget`이 없거나 설치 뒤 명령을 찾지 못하면 임의 사이트에서 ZIP을 받거나 PATH를 추측해 고치지 않습니다. 운영자가 [Python 공식 Windows 다운로드](https://www.python.org/downloads/windows/)와 [FFmpeg 공식 다운로드 안내](https://ffmpeg.org/download.html)에서 현재 권장 경로를 다시 확인합니다.

## 4. Skill 설치와 마지막 확인

세 도구가 준비된 뒤 Claude에게 다음 문장을 보냅니다.

```text
내 운영체제용 install 파일이 하는 일을 먼저 세 줄로 설명해 주세요.
기존 ai-shorts는 삭제하지 않고 날짜가 붙은 백업으로 옮기는지 확인해 주세요.
내 확인을 기다린 뒤 설치하고, 새 Code 세션에서 /ai-shorts가 보이는지 확인해 주세요.
```

새 세션에서 `/`를 입력했을 때 `ai-shorts`가 보이고, `demo-project` 점검에서 `3/3 준비됨`이 나오면 클리닉 완료입니다.

## 운영자 체크

- [ ] Mac 한 대에서 ZIP 압축 해제부터 14초 MP4 완성까지 다시 실행했다.
- [ ] Windows 한 대에서 ZIP 압축 해제부터 14초 MP4 완성까지 다시 실행했다.
- [ ] 설치 화면에 API 키·암호·개인 경로가 보이지 않는지 확인했다.
- [ ] 설치 실패자는 Day 7 전에 별도 보충 시간을 배정했다.
