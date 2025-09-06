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

def measure_thread_context_switch(num_threads=NUM_THREADS, switch_count=1000):
    counter = [0]

    def switch_task(n):
        for _ in range(n):
            counter[0] += 1

    # Create num_threads threads running the switch_task task
    threads = [threading.Thread(target=switch_task, args=(switch_count, )) for _ in range(num_threads)]
    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = time.time()
    return end - start

def measure_thread_memory_overhead(num_threads=NUM_THREADS):
    # Begin tracking memory allocations
    tracemalloc.start()
    threads = [threading.Thread(target=dummy_task, args=(1000,)) for _ in range(num_threads)]

    # Record peak memory so far
    start_mem = tracemalloc.get_traced_memory()[1]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Get peak memory after creation and execution
    end_mem = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    # memory overhead
    return end_mem - start_mem


def measure_green_thread_creation(num_threads=NUM_THREADS):
    start = time.time()
    
    # Creates a greenlet (user-level thread)
    jobs = [gevent.spawn(dummy_task, 1000) for _ in range(num_threads)]

    # Waits for all greenlets to finish.
    gevent.joinall(jobs)
    end = time.time()
    return end - start

def measure_green_context_switch(num_threads=NUM_THREADS, switch_count=1000):
    counter = [0]

    def switch_task(n):
        for _ in range(n):
            counter[0] += 1
            gevent.sleep(0) # yield control so another greenlet can run

    jobs = [gevent.spawn(switch_task, switch_count) for _ in range(num_threads)]
    start = time.time()
    gevent.joinall(jobs)
    end = time.time()
    return end - start

def measure_green_memory_overhead(num_threads=NUM_THREADS):
    tracemalloc.start()
    jobs = [gevent.spawn(dummy_task, 1000) for _ in range(num_threads)]
    start_mem = tracemalloc.get_traced_memory()[1]
    gevent.joinall(jobs)
    end_mem = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return end_mem - start_mem

if __name__ == "__main__":
    print("=== Thread creation time ===")
    print("Kernel threads:", measure_thread_creation())
    print("Green threads:", measure_green_thread_creation())

    print("=== Context switch time ===")
    print("Kernel threads:", measure_thread_context_switch())
    print("Green threads:", measure_green_thread_creation())

    print("=== Memory Overhead (bytes) ===")
    print("Kernel threads:", measure_thread_memory_overhead())
    print("Green threads:", measure_green_memory_overhead())
