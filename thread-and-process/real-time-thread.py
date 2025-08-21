import threading
import time

# Shared resources
## Creates a lock object --> Ensures only one thread modifies shared data at a time
mutex = threading.Lock()

## Internally uses the `mutex`. Allows a thread to wait until another signals that new data is ready
data_cond = threading.Condition(mutex)

## Telling whether new data has been produced
data_ready = False
shared_data = 0.0

## Flag to tell the consumer to stop gracefully
stop_signal = False

def real_time_producer():
    global shared_data, data_ready, stop_signal
    for i in range(10):
        with data_cond:
            shared_data = i * 1.5
            data_ready = True
            data_cond.notify() # Signal consumer
        time.sleep(0.1) # 100ms
    
    # After producing, send stop signal
    with data_cond:
        stop_signal = True
        data_cond.notify()

def real_time_consumer():
    global shared_data, data_ready, stop_signal
    while True:
        with data_cond:
            while not data_ready and not stop_signal:
                data_cond.wait() # Releases the mutex and suspends the thread until `notify()` is called by the producer. Once woken, it re-acquires
                ## the lock and continues.
            if stop_signal:
                break

            print(f"Received data: {shared_data}")
            data_ready = False # Resets the flag so the consumer doesn't reprocess the same data

if __name__ == "__main__":
    producer_thread = threading.Thread(target=real_time_producer)
    consumer_thread = threading.Thread(target=real_time_consumer)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
