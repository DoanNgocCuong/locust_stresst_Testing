# Script để fix lỗi cài đặt packages trên Windows
# Lỗi: [WinError 32] The process cannot access the file because it is being used by another process

Write-Host "=== Fix Locust Installation Issue ===" -ForegroundColor Cyan

# Bước 1: Kill tất cả Python processes
Write-Host "`n[1/4] Đang dừng tất cả Python processes..." -ForegroundColor Yellow
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    $pythonProcesses | Stop-Process -Force
    Write-Host "   Đã dừng $($pythonProcesses.Count) Python process(es)" -ForegroundColor Green
} else {
    Write-Host "   Không có Python process nào đang chạy" -ForegroundColor Green
}

# Bước 2: Đợi một chút để file được release
Write-Host "`n[2/4] Đợi 2 giây để file được release..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

# Bước 3: Cài đặt lại với --no-cache-dir
Write-Host "`n[3/4] Cài đặt lại packages với --no-cache-dir..." -ForegroundColor Yellow
Write-Host "   Chạy: pip install --no-cache-dir -r requirements.txt" -ForegroundColor Cyan

# Bước 4: Hướng dẫn
Write-Host "`n[4/4] Hướng dẫn:" -ForegroundColor Yellow
Write-Host "   1. Đóng tất cả IDE/Editor (VS Code, PyCharm, etc.)" -ForegroundColor White
Write-Host "   2. Đóng tất cả terminal windows khác" -ForegroundColor White
Write-Host "   3. Chạy lệnh sau:" -ForegroundColor White
Write-Host "      pip install --no-cache-dir -r requirements.txt" -ForegroundColor Cyan
Write-Host "`n   HOẶC nếu vẫn lỗi, xóa và tạo lại virtual environment:" -ForegroundColor White
Write-Host "      deactivate" -ForegroundColor Cyan
Write-Host "      Remove-Item -Recurse -Force ..\..\.locust_env" -ForegroundColor Cyan
Write-Host "      python -m venv ..\..\.locust_env" -ForegroundColor Cyan
Write-Host "      ..\..\.locust_env\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "      pip install --upgrade pip" -ForegroundColor Cyan
Write-Host "      pip install -r requirements.txt" -ForegroundColor Cyan

Write-Host "`n=== Hoàn thành ===" -ForegroundColor Green








