# Windows 사전점검

## 필요한 것

- 최신 Claude Desktop과 유료 Claude 요금제
- Python Launcher(`py`)
- FFmpeg와 FFprobe가 PATH에서 실행되는 상태
- 인터넷 연결 — 최초 Pillow 설치에 필요

## 확인 순서

Claude에게 PowerShell에서 읽기 전용 확인만 하게 합니다.

```powershell
py --version
ffmpeg -version
ffprobe -version
```

모두 버전 번호를 보여 주면 `install_windows.ps1`의 작업 내용을 먼저 설명하게 하고 승인 뒤 실행합니다. 기존 Skill은 날짜가 붙은 백업으로 옮겨집니다.

## 성공 문장

```text
영상 자르기 준비 완료
영상 정보 읽기 준비 완료
자막 그리기 준비 완료
Skill 설치 완료
```

`py` 또는 `ffmpeg`를 찾을 수 없으면 PowerShell의 임의 설치 명령을 실행하지 않습니다. 운영자에게 `Day 7 사전점검 / Windows / 화면에 보이는 오류`를 보냅니다. 운영자가 Windows 교육용 컴퓨터에서 먼저 검증한 [`INSTALL_CLINIC.md`](INSTALL_CLINIC.md)의 Windows 절차를 함께 진행합니다.
