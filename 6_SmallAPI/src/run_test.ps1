# PowerShell script để chạy Locust test cho Qwen3-1.7B API

# Màu sắc cho output
$Host.UI.RawUI.ForegroundColor = "Green"
Write-Host "========================================"
Write-Host "  Qwen3-1.7B API Locust Stress Test"
Write-Host "========================================"
$Host.UI.RawUI.ForegroundColor = "White"

# Kiểm tra xem đã cài đặt Locust chưa
try {
    $locustVersion = locust --version 2>&1
    Write-Host "Locust version: $locustVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Locust chưa được cài đặt!" -ForegroundColor Red
    Write-Host "Hãy chạy: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Tham số mặc định
$users = 10
$spawnRate = 2
$duration = "60s"
$hostUrl = "http://124.197.20.86:7862"
$headless = $false

# Đọc tham số từ command line (nếu có)
if ($args.Count -gt 0) {
    $users = if ($args[0]) { [int]$args[0] } else { 10 }
    $spawnRate = if ($args[1]) { [int]$args[1] } else { 2 }
    $duration = if ($args[2]) { $args[2] } else { "60s" }
    $headless = if ($args[3] -eq "headless") { $true } else { $false }
}

Write-Host ""
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  Users: $users"
Write-Host "  Spawn Rate: $spawnRate users/second"
Write-Host "  Duration: $duration"
Write-Host "  Host: $hostUrl"
Write-Host "  Mode: $(if ($headless) { 'Headless' } else { 'Web UI' })"
Write-Host ""

# Tạo thư mục results nếu chưa có
if (-not (Test-Path "../results")) {
    New-Item -ItemType Directory -Path "../results" | Out-Null
}

if ($headless) {
    Write-Host "Starting Locust in headless mode..." -ForegroundColor Yellow
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $htmlReport = "../results/report_$timestamp.html"
    $csvPrefix = "../results/results_$timestamp"
    
    locust --headless `
        -u $users `
        -r $spawnRate `
        -t $duration `
        --host $hostUrl `
        --html $htmlReport `
        --csv $csvPrefix
    
    Write-Host ""
    Write-Host "Test completed! Report saved to: $htmlReport" -ForegroundColor Green
} else {
    Write-Host "Starting Locust Web UI..." -ForegroundColor Yellow
    Write-Host "Open browser at: http://localhost:8089" -ForegroundColor Cyan
    Write-Host ""
    locust --host $hostUrl
}

