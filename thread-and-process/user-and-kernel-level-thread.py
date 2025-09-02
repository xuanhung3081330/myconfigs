import threading
import time

# Allows us to measure Python memory allocations
import tracemalloc

# Provides user-level threads managed in user space
import gevent

# Used to patch Python's standard library so that blocking calls (like sleep, socket) co-operate with greenlets.
from gevent import monkey

# This line replaces some standard blocking functions (like time.sleep) with gevent-aware versions
monkey.patch_all()

NUM_THREADS = 1000

# CPU-bound dummy task
def dummy_task(n):
    for _ in range(n):
        pass

def measure_thread_creation(num_threads=NUM_THREADS):
    start = time.time()
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=dummy_task, args=(1000,))
        t.start()
        threads.append(t)

    for t in threads:
        # Wait for all threads to finish before continuing
        t.join()
    end = time.time()
    return end - start

def measure_green_thread_creation(num_threads=NUM_THREADS):
    start = time.time()
    
    # Creates a greenlet (user-level thread)
    jobs = [gevent.spawn(dummy_task, 1000) for _ in range(num_threads)]

    # Waits for all greenlets to finish.
    gevent.joinall(jobs)
    end = time.time()
    return end - start

if __name__ == "__main__":
    print("=== Thread creation time ===")
    print("Kernel threads:", measure_thread_creation())
    print("Green threads:", measure_green_thread_creation())
