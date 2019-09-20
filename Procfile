release:  flask db upgrade && python3 $PWD/api/inserts.py
web: gunicorn -w 4 -b $HOST:$PORT "api:create_app()"