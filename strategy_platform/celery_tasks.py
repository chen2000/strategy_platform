from __future__ import absolute_import

from celery import Celery

broker = 'redis://127.0.0.1:6379/1'
# 6379 is port number, 1 is database name, New connections always use the database 0 so designated connections better start from 1, to avoid conflict
# broker is used to store task queue
backend = 'redis://127.0.0.1:6379/2'
# backend is used to store result

app = Celery('celery_tasks', broker=broker, backend=backend)

@app.task
def add(x, y):
    return x + y
