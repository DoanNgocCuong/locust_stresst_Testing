# Cài đặt dependencies
cd 6_SmallAPI/src
pip install -r requirements.txt

# Chạy với Web UI
locust

# Hoặc chạy headless
locust --headless -u 10 -r 2 -t 60s --host http://103.253.20.30:30030
locust -f locustfile.py --host http://103.253.20.30:30030


# Hoặc dùng PowerShell script
cd 6_SmallAPI/src
.\run_test.ps1 10 2 60s headless