$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not (Get-Command py -ErrorAction SilentlyContinue)) { throw "Python 3가 없습니다. 운영자에게 알려 주세요." }
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { throw "ffmpeg가 없습니다. 먼저 운영자 설치 안내를 받으세요." }
$installRoot = if ($env:AI_SHORTS_INSTALL_ROOT) { $env:AI_SHORTS_INSTALL_ROOT } else { Join-Path $HOME ".claude\skills" }
$target = Join-Path $installRoot "ai-shorts"
New-Item -ItemType Directory -Force (Split-Path $target) | Out-Null
if (Test-Path $target) {
  $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
  $backup = Join-Path (Split-Path $target) "ai-shorts.backup-$stamp"
  Move-Item $target $backup
  Write-Host "기존 Skill 백업: $backup"
}
Copy-Item -Recurse "ai-shorts" $target
py -m venv (Join-Path $target ".venv")
& (Join-Path $target ".venv\Scripts\python.exe") -m pip install -q pillow
Write-Host "설치 완료: $target"
Write-Host "Claude Code 새 세션에서 /ai-shorts 를 확인하세요."
