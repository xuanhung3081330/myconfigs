import threading
import multiprocessing
import time

# Shared variable for threading example (Shared memory)
shared_counter = 0

# Function for thread to increment shared_counter
def thread_increment():
    global shared_counter
    for _ in range(100):
        shared_counter += 1
        print(f"===Counter value in threads: {shared_counter}===")

# Function for process to increment a local copy (no shared memory)
def process_increment(counter):

    # Set to small number to check if each process is really calculating their own 'counter' variable
    for _ in range(10):
        #Case 2: counter.value += 1
        #Case 1: 
        counter += 1
        print(f"=== Counter value in child process: {counter}===")

if __name__ == "__main__":
    print("=== Thread example (shared memory) ===")
    threads = []
    shared_counter = 0

    for _ in range(4):
        t = threading.Thread(target=thread_increment)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"=== Final shared_counter value (threads): {shared_counter} ===")
    # Expect: 4 * 10000 = 40000 (but race condition may occur)

    print("\n=== Process example (separate memory) ===")
    # multiprocessing.Value to create shared memory for int
    # Case 1: counter = multiprocessing.Value('i', 0) --> This simulates processes share memory with each other
    #counter = multiprocessing.Value('i', 0)

    # This variable is used to test if processes share memory with each other
    # Case 2: 
    counter = 0

    processes = []
    for _ in range(4):
        p = multiprocessing.Process(target=process_increment, args=(counter,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print(f"=== Final counter value (processes): {counter} ===")
