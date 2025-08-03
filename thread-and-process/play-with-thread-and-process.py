from multiprocessing import Process
import os
import time
import threading

def task(name):
    print(f"[{name}] Thread ID: {threading.get_ident()}")
    print(f"[{name}] Starting work...")
    time.sleep(2)
    print(f"[{name}] Work done!")

if __name__ == "__main__":
    #p1 = Process(target=task, args=("Task-1",))
    #p2 = Process(target=task, args=("Task-2",))

    #p1.start() # Start first Process
    #p1.join()

    #p2.start() # Start second process
    #p2.join()

    #print("Main process waiting for subprocesses to finish...")
    #p1.join()
    #p2.join()

    #print("Main process done.")

    t1 = threading.Thread(target=task, args=("Thread-1",))
    t2 = threading.Thread(target=task, args=("Thread-2",))

    t1.start()
    t2.start()

    print("Main thread waiting for threads to finish...")
    t1.join()
    t2.join()

    print("Main thread done.")
