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

