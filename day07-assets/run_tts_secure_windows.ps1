param(
  [Parameter(Mandatory=$true)][string]$ScriptFile,
  [Parameter(Mandatory=$true)][string]$WorkDir,
  [string]$VoiceId = ""
)
$ErrorActionPreference = "Stop"
$secrets = Join-Path $HOME ".config\ai-shorts\secrets.env"
if (-not (Test-Path $secrets)) { throw "Typecast 연결 정보가 없습니다. TYPECAST_SETUP.md를 먼저 보세요." }
foreach ($line in Get-Content $secrets) {
  if ($line -match '^([^#=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process") }
}
if (-not $VoiceId) { $VoiceId = if ($env:TYPECAST_VOICE) { $env:TYPECAST_VOICE } else { "tc_69fc0cff784968297fb45daa" } }
$skill = Join-Path $HOME ".claude\skills\ai-shorts"
& (Join-Path $skill ".venv\Scripts\python.exe") (Join-Path $skill "scripts\tts.py") $ScriptFile $WorkDir --voice $VoiceId
[Environment]::SetEnvironmentVariable("TYPECAST_API_KEY", $null, "Process")
