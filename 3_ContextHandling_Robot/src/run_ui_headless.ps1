# Script chạy Locust headless (không có UI) và export kết quả
# Sử dụng: .\run_ui_headless.ps1 -Users 10 -SpawnRate 2 -Time 60s

param(
    [string]$Host = "",
    [int]$Users = 10,
    [int]$SpawnRate = 2,
    [string]$Time = "60s",
    [string]$OutputDir = "results"
)

# Đọc .env file nếu có
$envFile = Join-Path (Split-Path $PSScriptRoot -Parent) ".env"
$targetHost = "http://103.253.20.30:30020"  # Default

if (Test-Path $envFile) {
    $envContent = Get-Content $envFile
    foreach ($line in $envContent) {
        if ($line -match "^3_ContextHandling_Robot_URL=(.+)$") {
            $targetHost = $matches[1].Trim()
            break
        }
    }
    Write-Host "Loaded URL from .env: $targetHost" -ForegroundColor Green
} else {
    Write-Host "Warning: .env file not found, using default URL" -ForegroundColor Yellow
}

# Override với parameter nếu được cung cấp
if ($Host -ne "") {
    $targetHost = $Host
}

# Tạo thư mục results nếu chưa có
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$HtmlReport = "$OutputDir\report_$Timestamp.html"
$CsvReport = "$OutputDir\stats_$Timestamp.csv"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Locust Stress Test - Headless Mode" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Target Host: $targetHost" -ForegroundColor White
Write-Host "  Users: $Users" -ForegroundColor White
Write-Host "  Spawn Rate: $SpawnRate users/second" -ForegroundColor White
Write-Host "  Duration: $Time" -ForegroundColor White
Write-Host "  HTML Report: $HtmlReport" -ForegroundColor White
Write-Host "  CSV Report: $CsvReport" -ForegroundColor White
Write-Host ""
Write-Host "Starting test..." -ForegroundColor Green
Write-Host ""

# Chạy Locust headless
locust -f locustfile.py `
    --host=$targetHost `
    --headless `
    -u $Users `
    -r $SpawnRate `
    -t $Time `
    --html=$HtmlReport `
    --csv=$OutputDir\stats_$Timestamp

Write-Host ""
Write-Host "Test completed!" -ForegroundColor Green
Write-Host "  View report: $HtmlReport" -ForegroundColor Cyan

