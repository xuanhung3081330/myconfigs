import threading
import multiprocessing
import time

N = 100 # Number of threads/processes to create

def dummy_function():
    pass

def measure_thread_creation():
    threads = []
    start = time.perf_counter()
    for _ in range(N):
        t = threading.Thread(target=dummy_function)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    end = time.perf_counter()
    print(f"[Threading] created and joined {N} threads in {end - start:.4f} seconds")

def measure_process_creation():
    processes = []
    start = time.perf_counter()
    for _ in range(N):
        p = multiprocessing.Process(target=dummy_function)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    end = time.perf_counter()
    print(f"[Multiprocessing] created and joined {N} processes in {end - start:.4f} seconds")

if __name__ == "__main__":
    print("Starting thread creation test...")
    measure_thread_creation()

    print("\nStarting process creation test...")
    measure_process_creation()
