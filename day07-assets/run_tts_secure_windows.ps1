param(
  [Parameter(Mandatory=$true)][string]$ScriptFile,
  [Parameter(Mandatory=$true)][string]$WorkDir,
  [Parameter(Mandatory=$true)][string]$VoiceId
)
$ErrorActionPreference = "Stop"
$secrets = if ($env:AI_SHORTS_SECRETS_FILE) { $env:AI_SHORTS_SECRETS_FILE } else { Join-Path $HOME ".config\ai-shorts\secrets.env" }
if (-not (Test-Path $secrets)) { throw "Typecast 연결 정보가 없습니다. TYPECAST_SETUP.md를 먼저 보세요." }
foreach ($line in Get-Content $secrets) {
  if ($line -match '^([^#=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process") }
}
$skill = if ($env:AI_SHORTS_SKILL_ROOT) { $env:AI_SHORTS_SKILL_ROOT } else { Join-Path $HOME ".claude\skills\ai-shorts" }
try {
  & (Join-Path $skill ".venv\Scripts\python.exe") (Join-Path $skill "scripts\tts.py") $ScriptFile $WorkDir --voice $VoiceId
} finally {
  [Environment]::SetEnvironmentVariable("TYPECAST_API_KEY", $null, "Process")
}
