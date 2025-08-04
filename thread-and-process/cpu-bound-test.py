import time
import threading
import multiprocessing

TASK_COUNT = 10
WORKLOAD = 10_000_000

def cpu_task():
    total = 0
    for i in range(WORKLOAD):
        total += i*i

def run_threads():
    threads = []
    start = time.time()
    for _ in range(TASK_COUNT):
        t = threading.Thread(target=cpu_task)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print(f"Threading (CPU-bound): {time.time() - start:.2f} seconds")

def run_processes():
    processes = []
    start = time.time()
    for _ in range(TASK_COUNT):
        p = multiprocessing.Process(target=cpu_task)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print(f"Multiprocessing (CPU-bound): {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    run_threads()
    run_processes()

