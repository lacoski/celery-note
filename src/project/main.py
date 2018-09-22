from celery import chain
from proj.tasks import add
res = chain(add.s(2, 2), add.s(4), add.s(8))()
res.get()