# Names

Every task must have a unique name.

If no explicit name is provided the task decorator will generate one for you, and this name will be based on 1) the module the task is defined in, and 2) the name of the task function.

```python
>>> @app.task(name='sum-of-two-numbers')
>>> def add(x, y):
...     return x + y

>>> add.name
'sum-of-two-numbers'
```

A best practice is to use the module name as a name-space, this way names won’t collide if there’s already a task with that name defined in another module.

```python
>>> @app.task(name='tasks.add')
>>> def add(x, y):
...     return x + y
```

---

# Task Request
```python
@app.task(bind=True)
def dump_context(self, x, y):
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
            self.request))
```

http://docs.celeryproject.org/en/latest/userguide/tasks.html#task-request


# Retrying

app.Task.retry() can be used to re-execute the task, for example in the event of recoverable errors.

When you call retry it’ll send a new message, using the same task-id, and it’ll take care to make sure the message is delivered to the same queue as the originating task.

When a task is retried this is also recorded as a task state, so that you can track the progress of the task using the result instance (see States).

```python
@app.task(bind=True)
def send_twitter_status(self, oauth, tweet):
    try:
        twitter = Twitter(oauth)
        twitter.update_status(tweet)
    except (Twitter.FailWhaleError, Twitter.LoginError) as exc:
        raise self.retry(exc=exc)
```