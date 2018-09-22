from __future__ import absolute_import, unicode_literals
from proj.celery import app
from celery.task import Task
from celery.registry import tasks
from celery.task import task
import time
import os



@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

class Hello(Task):
    queue = 'hipri'

    def run(self, to):
        return 'hello {0}'.format(to)

@app.task
def hello(to):
    return 'hello {0}'.format(to)

@app.task
def sleep_test(time_count):
    print ("Start : %s" % time.ctime())
    time.sleep( time_count )
    print ("End : %s" % time.ctime())
    return True

tasks.register(Hello)

@app.task
def log_error(request, exc, traceback):
    with open(os.path.join('/var/errors', request.id), 'a') as fh:
        print('--\n\n{0} {1} {2}'.format(
            task_id, exc, traceback), file=fh)

@app.task
def on_chord_error(request, exc, traceback):
    print('Task {0!r} raised error: {1!r}'.format(request.id, exc))
    