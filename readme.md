# Tìm hiểu Celery
---

Task queue là kỹ thuật phân phối task trên các thread và worker

Đầu vào task queue là có đơn vị task. Các worker sẽ liên tục theo dõi, thực hiện task.

Celery kết nối thông qua message, sử dụng broker (Người trung gian) giữa client và worker. Để khởi tạo task, client sẽ đẩy message vào queue, broker sẽ đen message tới worker.

Celery bao gồm nhiều worker và broker, đảm bảo tính HA, mở rộng

---

# Brokers
> Người trung gian

Broker hỗ trợ các công nghệ:
- RabbitMQ
- Redis
- Amazon SQS

```
Name	    Status	        Monitoring	Remote Control
RabbitMQ	Stable	        Yes	        Yes
Redis	    Stable	        Yes	        Yes
Amazon      SQS	Stable	    No	        No
Zookeeper	Experimental	No	        No
```

---

# App
Đầu tiên, celery yêu cầu khởi tạo instance riêng. Gọi chúng là celery application, hoặc app.
- Mỗi instance là nơi thực hiện các tác vụ đồi hỏi sử dụng celery hay khái niệm task queue.

---
Giải thích giao diện khi khởi tạo worker

```
-------------- celery@ubuntu v4.2.1 (windowlicker)
---- **** ----- 
--- * ***  * -- Linux-4.15.0-34-generic-x86_64-with-Ubuntu-18.04-bionic 2018-09-21 09:06:29
-- * - **** --- 
- ** ---------- [config]
- ** ---------- .> app:         proj:0x7f7d97f3e1d0
- ** ---------- .> transport:   amqp://guest:**@localhost:5672//
- ** ---------- .> results:     amqp://
- *** --- * --- .> concurrency: 4 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery

```

http://docs.celeryproject.org/en/latest/getting-started/next-steps.html#starting-the-worker


# Chạy celery ngầm

http://docs.celeryproject.org/en/latest/getting-started/next-steps.html#in-the-background

# Run
Truy cập: `celery-note/src/project`

Chạy
```
celery -A proj worker -l info
```

Test:
```
res1 = sleep_test.delay(10)

res1.state (trạng thái)

res1.get() (lấy kết quả)
```

---

# Signatures
Đóng gói task thành 1 gói, truyền biến độc lập. Việc này cho phép truyền nhiều hơn giá trị hiện có của hàm

```
from celery import signature

signature('tasks.add', args=(2, 2), countdown=10)
```

```
>>> add.apply_async(args, kwargs, **options)
>>> add.signature(args, kwargs, **options).apply_async()

>>> add.apply_async((2, 2), countdown=1)
>>> add.signature((2, 2), countdown=1).apply_async()
```

```
>>> s = add.signature((2, 2), {'debug': True}, countdown=10)
>>> s.args
(2, 2)
>>> s.kwargs
{'debug': True}
>>> s.options
{'countdown': 10}
```

---

# Partials

Với signature, ta có thể thực hiện task trong worker theo dạng:
```
>>> add.s(2, 2).delay()
>>> add.s(2, 2).apply_async(countdown=1)
```

Hoặc có thể thực hiện trực tiếp
```
add.s(2, 2)()
```

trick:
```
>>> # is the same as
>>> sig.delay().get()
```

---

# Immutability

Partials thường được sử dụng với hàm callbacks, any tasks linked, hoặc chord callbacks với

---

# Callbacks

Callbacks có thể áp dụng với bất kỳ task với trường link trong `apply_async`

```
add.apply_async((2, 2), link=other_task.s())
```

---
## Simple chain
```
>>> from celery import chain

>>> # 2 + 2 + 4 + 8
>>> res = chain(add.s(2, 2), add.s(4), add.s(8))()
>>> res.get()
16
```

## Immutable signatures
> Hạn chế, không cho truyền đối số liền kề
```
>>> add.signature((2, 2), immutable=True)

>>> res = (add.si(2, 2) | add.si(4, 4) | add.si(8, 8))()
>>> res.get()
16

>>> res.parent.get()
8

>>> res.parent.parent.get()
4
```

```
>>> from celery import group
>>> res = group(add.s(i, i) for i in [1,2,3,4,5,6,7,8])()
>>> res.get(timeout=1)
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

## Simple chord
```
from celery import chord
res = chord((add.s(i, i) for i in [1,2,3,4,5,6,7,8]), xsum.s())()
```

```
>>> c1 = (add.s(4) | mul.s(8))

# (16 + 4) * 8
>>> res = c1(16)
>>> res.get()
160
```

---
# Chains
```
>>> res = add.apply_async((2, 2), link=mul.s(16))
>>> res.get()
64

>>> res.children
[<AsyncResult: 8c350acf-519d-4553-8a53-4ad3a5c5aeb4>]

>>> res.children[0].get()
64

>>> list(res.collect())
[(<AsyncResult: 7b720856-dc5f-4415-9134-5c89def5664e>, 4),
 (<AsyncResult: 8c350acf-519d-4553-8a53-4ad3a5c5aeb4>, 64)]
```

```
>>> s = add.s(2, 2)
>>> s.link(mul.s(4))
>>> s.link(log_result.s())
```

You can also add error callbacks using the on_error method:
```
>>> add.s(2, 2).on_error(log_error.s()).delay()
```
```
add.apply_async((2, 2), link_error=log_error.s())
```

---
# Groups

```
>>> from celery import group
>>> from proj.tasks import add

>>> group(add.s(2, 2), add.s(4, 4))
(proj.tasks.add(2, 2), proj.tasks.add(4, 4))

>>> g = group(add.s(2, 2), add.s(4, 4))
>>> res = g()
>>> res.get()
[4, 8]
```

```
>>> from celery import group
>>> from tasks import add

>>> job = group([
...             add.s(2, 2),
...             add.s(4, 4),
...             add.s(8, 8),
...             add.s(16, 16),
...             add.s(32, 32),
... ])

>>> result = job.apply_async()

>>> result.ready()  # have all subtasks completed?
True
>>> result.successful() # were all subtasks successful?
True
>>> result.get()
[4, 8, 16, 32, 64]
```

---

# Routing 
- Hỗ trợ routing, tức task nào sẽ đi qua queue nào. 
- Định tuyến hỗ trợ việc giám sát.
