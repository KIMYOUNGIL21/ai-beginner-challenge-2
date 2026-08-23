param(
  [string]$Text = "오늘부터 작은 기록을 시작합니다.",
  [string]$Query = "차분하고 또렷한 한국어 내레이션",
  [string]$OutDir = "voices"
)

$ErrorActionPreference = "Stop"
$secrets = if ($env:AI_SHORTS_SECRETS_FILE) { $env:AI_SHORTS_SECRETS_FILE } else { Join-Path $HOME ".config\ai-shorts\secrets.env" }
if (-not (Test-Path $secrets)) {
  throw "Typecast 연결 정보가 없습니다. TYPECAST_SETUP.md를 먼저 보세요."
}

foreach ($line in Get-Content $secrets) {
  if ($line -match '^([^#=]+)=(.*)$') {
    [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
  }
}

$skill = if ($env:AI_SHORTS_SKILL_ROOT) { $env:AI_SHORTS_SKILL_ROOT } else { Join-Path $HOME ".claude\skills\ai-shorts" }
try {
  & (Join-Path $skill ".venv\Scripts\python.exe") (Join-Path $skill "scripts\voices.py") $Text --out $OutDir --query $Query --n 5
} finally {
  [Environment]::SetEnvironmentVariable("TYPECAST_API_KEY", $null, "Process")
}
