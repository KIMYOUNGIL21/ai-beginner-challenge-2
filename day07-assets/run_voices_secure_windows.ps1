param(
  [string]$Text = "오늘부터 작은 기록을 시작합니다.",
  [string]$Query = "차분하고 또렷한 한국어 내레이션",
  [string]$OutDir = "voices"
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
  & (Join-Path $skill ".venv\Scripts\python.exe") (Join-Path $skill "scripts\voices.py") $Text --out $OutDir --query $Query --n 5
} finally {
  [Environment]::SetEnvironmentVariable("TYPECAST_API_KEY", $null, "Process")
}
