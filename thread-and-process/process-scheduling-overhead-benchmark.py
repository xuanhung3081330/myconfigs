import os
import time
import threading
import queue

# Number of iterations between parent and child processes
# Each iteration includes 2 context switches (parent -> child, child -> parent)
NUM_ITERATIONS = 1_000_000

def measure_process_context_switch_overhead():
    # Create a pipe: returns (read_fd, write_fd)
    # Unidirectional communication channel
    pipe_fd = os.pipe() # --> This returns 2 file descriptors: pipe_fd[0]: read end, pipe_fd[1]: write end

    # A one-byte message that will be passed back and forth. Used to trigger context switch
    buffer = b"x"

    start = time.time()
    
    pid = os.fork()
    if pid == 0:
        # Child process
        for _ in range(NUM_ITERATIONS):
            os.read(pipe_fd[0], 1) # Child blocks until it reads 1 byte from the pipe (sent by the parent)
            os.write(pipe_fd[1], buffer) # After receiving, it responds.
        os._exit(0)
    else:
        # Parent process
        for _ in range(NUM_ITERATIONS):
            os.write(pipe_fd[1], buffer) # Writes 1 byte -> Signals child to run
            os.read(pipe_fd[0], 1) # Waits until child responds

    end = time.time()
    elapsed = end - start
    print(f"[Process] The total seconds to run the switching process: {elapsed:.6f} seconds")

    avg_us = (elapsed * 1_000_000) / (NUM_ITERATIONS * 2)
    print(f"[Process] Average context switch time: {avg_us:.6f} microseconds")

def measure_thread_context_switch_overhead():
    pipe1 = os.pipe() # main -> worker
    pipe2 = os.pipe() # worker -> main
    buffer = b"x"

    #buffer = object() # dummy token, acts as a message between threads
    #q1 = queue.Queue(maxsize=1) # Used by parent to signal child
    #q2 = queue.Queue(maxsize=1) # Used by child to signal parent

    def worker(): # Thread function to simulate the child thread
        for _ in range(NUM_ITERATIONS):
            os.read(pipe1[0], 1) # Blocks until main thread writes
            os.write(pipe2[1], buffer) # Responds back

            #q1.get() # Wait until parent signals
            #q2.put(buffer) # Reply to parent
    
    t = threading.Thread(target=worker)
    t.start() # --> Thread becomes runnable

    start = time.time()
    for _ in range(NUM_ITERATIONS):
        os.write(pipe1[1], buffer) # Signal worker
        os.read(pipe2[0], 1) # Wait for reply

        #q1.put(buffer) # Signal worker
        #q2.get() # Wait for reply

    end = time.time()
    t.join()
    elapsed = end - start
    print(f"[Thread-Kernel] Total seconds: {elapsed:.6f} s")

    avg_us = (elapsed * 1_000_000) / (NUM_ITERATIONS * 2)
    print(f"[Thread-Kernel] Average context switch time: {avg_us:.6f} microseconds")



if __name__ == "__main__":
    measure_process_context_switch_overhead()
    measure_thread_context_switch_overhead()


## Every time:
### - Parent writes, then blocks on read() --> Kernel puts parent to sleep (not runnable)
### - Child becomes runnable, executes read(), then write() --> Child writes, then blocks on its read()
### Kernel wakes up the parent to continue

## NOTE:
# If you run this script, you'll notice that the avg time of threads' context switching is much more longer than process's.
# It's because of the Python runtime overhead. --> This benchmarch needs to be written in C/C++ to be more exact.
