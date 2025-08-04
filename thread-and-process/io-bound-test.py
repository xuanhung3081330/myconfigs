import time
import threading
import multiprocessing

TASK_COUNT = 10
SLEEP_DURATION = 1

def io_task():
    time.sleep(SLEEP_DURATION)

def run_threads():
    threads = []
    start = time.time()
    for _ in range(TASK_COUNT):
        t = threading.Thread(target=io_task)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print(f"Threading (I/O-bound): {time.time() - start:.2f} seconds")

def run_processes():
    processes = []
    start = time.time()
    for _ in range(TASK_COUNT):
        p = multiprocessing.Process(target=io_task)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print(f"Multiprocessing (I/O-bound): {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    run_threads()
    run_processes()
