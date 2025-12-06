# Cài đặt dependencies
cd 6_SmallAPI/src
pip install -r requirements.txt

# Chạy với Web UI
locust

# Hoặc chạy headless
locust --headless -u 10 -r 2 -t 60s --host http://124.197.20.86:7862
locust -f locustfile.py --host http://124.197.20.86:7862


# Hoặc dùng PowerShell script
cd 6_SmallAPI/src
.\run_test.ps1 10 2 60s headless