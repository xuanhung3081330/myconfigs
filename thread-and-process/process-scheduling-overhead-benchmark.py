import os
import time

# Number of iterations between parent and child processes
# Each iteration includes 2 context switches (parent -> child, child -> parent)
NUM_ITERATIONS = 1_000_000

def measure_context_switch_overhead():
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
    print(f"The total seconds to run the switching process: {elapsed:.6f} seconds")

    avg_us = (elapsed * 1_000_000) / (NUM_ITERATIONS * 2)
    print(f"Average context switch time: {avg_us:.6f} microseconds")

if __name__ == "__main__":
    measure_context_switch_overhead()


## Every time:
### - Parent writes, then blocks on read() --> Kernel puts parent to sleep (not runnable)
### - Child becomes runnable, executes read(), then write() --> Child writes, then blocks on its read()
### Kernel wakes up the parent to continue
