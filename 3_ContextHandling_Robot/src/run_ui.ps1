# Script chạy Locust với Web UI
# Sử dụng: .\run_ui.ps1

param(
    [string]$Host = "",
    [int]$Port = 8089,
    [string]$WebHost = "0.0.0.0"
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

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Locust Stress Test - Web UI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Target Host: $targetHost" -ForegroundColor White
Write-Host "  Web UI Port: $Port" -ForegroundColor White
Write-Host "  Web UI URL: http://localhost:$Port" -ForegroundColor White
Write-Host ""
Write-Host "Starting Locust Web UI..." -ForegroundColor Green
Write-Host "  Open browser at: http://localhost:$Port" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Chạy Locust với Web UI
locust -f locustfile.py `
    --host=$targetHost `
    --web-host=$WebHost `
    --web-port=$Port

