import threading
import time

balance = 100

def withdraw(amount):
    global balance
    if balance >= amount:
        time.sleep(0.01) # Simulate processing delay
        balance -= amount
        print(f"Withdrew {amount}, remaining balance: {balance}")
    else:
        print(f"Insufficient funds for {amount}, balance: {balance}")

def perform_withdrawals():
    for _ in range(10):
        withdraw(10)

threads = []

for index in range(10):
    t = threading.Thread(target=perform_withdrawals)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final balance: {balance}")
