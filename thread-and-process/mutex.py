import threading
import time

# Shared counter (global variable across threads)
shared_counter = 0

# Create a Lock
mutex = threading.Lock()

# Race condition version
def increment_without_lock():
    global shared_counter

    # Each thread increments 100,000 times
    for _ in range(100_000):
        tmp = shared_counter
        time.sleep(0.000001) # Force a context switch opportunity
        # No lock, race condition possible
        shared_counter = tmp + 1

# Safe synchronized version
def increment_with_lock():
    global shared_counter
    for _ in range(100_000):
        # Acquire the lock before modifying shared data
        #mutex.acquire()
        #shared_counter += 1
        #mutex.release()
        with mutex:
            tmp = shared_counter
            time.sleep(0.000001)
            shared_counter = tmp + 1

def main():
    global shared_counter

    print("Demonstrating Race condition:")
    shared_counter = 0

    threads = [threading.Thread(target=increment_without_lock) for _ in range(2)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    print(f"Final Counter (unsafe): {shared_counter}")

    print("\nDemonstrating safe synchronization:")
    shared_counter = 0

    threads = [threading.Thread(target=increment_with_lock) for _ in range(2)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    print(f"Final counter (Safe): {shared_counter}")

if __name__ == "__main__":
    main()
