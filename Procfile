web: flask db upgrade; flask translate compile; gunicorn -k eventlet -w 1 blogeek:app
worker: rq worker blogeek-tasks
