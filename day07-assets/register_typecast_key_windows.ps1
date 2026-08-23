$ErrorActionPreference = "Stop"
$configDir = Join-Path $HOME ".config\ai-shorts"
$configFile = Join-Path $configDir "secrets.env"
New-Item -ItemType Directory -Force $configDir | Out-Null
$secure = Read-Host "Typecast API 키 입력(화면에 보이지 않음)" -AsSecureString
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
try {
  $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
  if ([string]::IsNullOrWhiteSpace($plain)) { throw "입력된 키가 없습니다." }
  "TYPECAST_API_KEY=$plain" | Set-Content -Encoding ascii $configFile
} finally {
  if ($ptr -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
  $plain = $null
}
Write-Host "Typecast 연결 정보를 사용자 전용 설정에 저장했습니다. 키 값은 출력하지 않습니다."
