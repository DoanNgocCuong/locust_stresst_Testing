# Cài đặt dependencies
cd 3_ContextHandling_Robot/src
pip install -r requirements.txt

# Chạy với Web UI
locust -f locustfile.py --host=http://103.253.20.30:30020

# Chạy headless
locust -f locustfile.py --host=http://103.253.20.30:30020 --headless -u 10 -r 2 -t 60s