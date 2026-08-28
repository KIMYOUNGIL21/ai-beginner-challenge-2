param(
  [Parameter(Mandatory=$true)][string]$ScriptFile,
  [Parameter(Mandatory=$true)][string]$WorkDir,
  [Parameter(Mandatory=$true)][string]$VoiceId
)

$ErrorActionPreference = "Stop"

$key = $null
$keyFile = Join-Path (Get-Location) "typecast-key.txt"
if (Test-Path $keyFile) {
  $raw = Get-Content $keyFile -Raw -ErrorAction SilentlyContinue
  if ($raw) { $key = $raw.Trim() }
}
if ($key) {
  [Environment]::SetEnvironmentVariable("TYPECAST_API_KEY", $key, "Process")
} else {
  $secrets = if ($env:AI_SHORTS_SECRETS_FILE) { $env:AI_SHORTS_SECRETS_FILE } else { Join-Path $HOME ".config\ai-shorts\secrets.env" }
  if (Test-Path $secrets) {
    foreach ($line in Get-Content $secrets) {
      if ($line -match '^([^#=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
      }
    }
  }
}
if (-not $env:TYPECAST_API_KEY) {
  throw "Typecast 키가 없습니다. typecast-key.txt를 두 번 눌러 열고, 복사한 키를 붙여넣어 저장한 뒤 다시 실행하세요."
}

$skill = if ($env:AI_SHORTS_SKILL_ROOT) { $env:AI_SHORTS_SKILL_ROOT } else { Join-Path $HOME ".claude\skills\ai-shorts" }
try {
  & (Join-Path $skill ".venv\Scripts\python.exe") (Join-Path $skill "scripts\tts.py") $ScriptFile $WorkDir --voice $VoiceId
} finally {
  [Environment]::SetEnvironmentVariable("TYPECAST_API_KEY", $null, "Process")
}
