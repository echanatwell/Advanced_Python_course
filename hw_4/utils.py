import math
from concurrent.futures import as_completed
import time
from multiprocessing import Queue
from threading import Thread, Lock
import codecs
from datetime import datetime


def fibonacci(n):
    f1 = f2 = 1
    for _ in range(2, n):
        f1, f2 = f2, f1 + f2
    
    return f2


def integrate(f, a, b, n_iter=10000000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

def integrate_parallel(f, a, b, executor, n_jobs=1, n_iter=10000000, ):
    step = (b - a) / n_iter
    batch = math.ceil(n_iter // n_jobs)

    ranges = [(a + i*batch*step, a + min((i+1)*batch, n_iter)*step) for i in range(n_jobs)]
    
    remain_iters = n_iter
    futures = []
    with executor(max_workers=n_jobs) as exc:
        for r in ranges:
            range_iters = remain_iters if batch > remain_iters else batch
            futures.append(exc.submit(integrate, f, r[0], r[1], range_iters))
        acc = sum(future.result() for future in as_completed(futures))
    return acc
        

def A_process(recv_conn, send_conn):
    def get():
        while True:
            if recv_conn.poll():
                queue.put(recv_conn.recv().lower())
            time.sleep(0.1)
    
    def send():
        while True:
            if not queue.empty():
                send_conn.send(queue.get_nowait())
                time.sleep(5)
    
    queue = Queue()

    getter = Thread(target=get)
    sender = Thread(target=send)

    getter.start()
    sender.start()


def B_process(recv_conn, send_conn):
    def send_encoded():
        while True:
            if recv_conn.poll():
                send_conn.send(codecs.encode(recv_conn.recv(), 'rot13'))
            time.sleep(0.1)
    
    sender = Thread(target=send_encoded)

    sender.start()


def main_get(recv_conn, log_file):
    lock = Lock()
    while True:
        if recv_conn.poll():
            with lock:
                log_file.write(f'Got: {recv_conn.recv()}, timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \n')


def main_send(send_conn, log_file):
    lock = Lock()
    while True:
        inp = input()
        send_conn.send(inp)
        with lock:
            log_file.write(f'Sent: {inp}, timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \n')
        time.sleep(0.1)

