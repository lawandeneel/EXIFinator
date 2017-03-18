virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
redis-server > logs/redis_server.log 2>&1 &
mongod > logs/mongo_server.log 2>&1 &
