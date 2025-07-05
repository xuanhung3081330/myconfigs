import os
import time

# Create a parent process with its child
processid = os.fork()
print(processid)

if processid > 0:
    print("\nParent process:")
    print("Process ID: ", os.getpid())
    print("Child's process ID: ", processid)
    time.sleep(800)
else:
    print("\nChild process:")
    print("Process ID: ", os.getpid())
    print("Parent's process ID: ", os.getppid())
    os._exit(0)


