from threading import Thread
from multiprocessing import Process, Pipe
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
from utils import fibonacci, integrate_parallel, main_get, main_send, A_process, B_process
import math
from os import cpu_count
import sys

if __name__ == '__main__':
    # 4.1
    n_runs = 10
    N = 300_000

    start = time.time()
    for _ in range(n_runs):
        fibonacci(N)
    elapsed_sync = round(time.time() - start, 4)
    with open('artifacts/sync.txt', 'w') as f:
        f.write(f'Sync run finished in {elapsed_sync} s')
    
    threads = [Thread(target=fibonacci, args=(N, )) for _ in range(n_runs)]
    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed_thread = round(time.time() - start, 4)
    with open('artifacts/thread.txt', 'w') as f:
        f.write(f'Threaded run finished in {elapsed_thread} s')
    
    processes = [Process(target=fibonacci, args=(N, )) for _ in range(n_runs)]
    start = time.time()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    elapsed_processes = round(time.time() - start, 4)
    with open('artifacts/multiprocessing.txt', 'w') as f:
        f.write(f'Multiprocessing run finished in {elapsed_processes} s')
    
    # 4.2
    thread_file = open('artifacts/integrate_thread_file.txt', 'w')
    process_file =  open('artifacts/integrate_multiprocessing_file.txt', 'w')
    for num_workers in range(1, cpu_count()*2):
        start = time.time()
        integrate_parallel(math.cos, 0, math.pi / 2, ThreadPoolExecutor, n_jobs=num_workers)
        elapsed = round(time.time() - start, 4)
        thread_file.write(f'Threaded call with {num_workers} cpu cores finished in {elapsed} sec \n')

        start = time.time()
        integrate_parallel(math.cos, 0, math.pi / 2, ProcessPoolExecutor, n_jobs=num_workers)
        elapsed = round(time.time() - start, 4)
        process_file.write(f'Multiprocessing call with {num_workers} cpu cores finished in {elapsed} sec \n')
    
    thread_file.close()
    process_file.close()

    # 4.3
    recv_A, send_M = Pipe()
    recv_B, send_A = Pipe()
    recv_M, send_B = Pipe()

    A_proc = Process(target=A_process, args=(recv_A, send_A))
    B_proc = Process(target=B_process, args=(recv_B, send_B))
    
    log_file = open('artifacts/4_3_logs.txt', 'w')
    getter = Thread(target=main_get, args=(recv_M, log_file), daemon=True)
    sender = Thread(target=main_send, args=(send_M, log_file), daemon=True)

    A_proc.start()
    B_proc.start()

    print('Input:')
    sender.start()
    getter.start()

    try:
        sender.join()
        getter.join()
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        log_file.close()
        A_proc.terminate()
        B_proc.terminate()
        sys.exit()