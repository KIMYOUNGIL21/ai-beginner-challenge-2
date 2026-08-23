# Mac 사전점검

## 필요한 것

- 최신 Claude Desktop과 유료 Claude 요금제
- Python 3
- FFmpeg와 FFprobe
- 인터넷 연결 — 최초 Pillow 설치에 필요

## 확인 순서

Claude에게 `명령을 실행하기 전에 읽기 전용 확인만 하고 결과를 쉬운 말로 보여 주세요.`라고 한 뒤 다음을 확인하게 합니다.

```bash
python3 --version
ffmpeg -version
ffprobe -version
```

세 명령이 버전 번호를 보여 주면 `bash install_mac.sh`의 작업 내용을 먼저 설명하게 하고 승인 뒤 실행합니다. 설치 파일은 기존 Skill을 날짜가 붙은 백업으로 옮긴 뒤 새 사본과 전용 Python 환경을 만듭니다.

## 성공 문장

```text
영상 자르기 준비 완료
영상 정보 읽기 준비 완료
자막 그리기 준비 완료
Skill 설치 완료
```

Python 또는 FFmpeg가 없다면 임의 웹사이트의 설치 파일을 받지 말고 운영자에게 `Day 7 사전점검 / Mac / 없는 항목`을 보냅니다. 운영자와 [`INSTALL_CLINIC.md`](INSTALL_CLINIC.md)의 Mac 절차를 완료한 뒤 다시 확인합니다.
