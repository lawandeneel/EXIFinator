source venv/bin/activate
mrq-worker download write > logs/worker1.log 2>&1 &
mrq-worker write > logs/worker2.log 2>&1 &
mrq-dashboard > logs/dashboard.log 2>&1 & 
