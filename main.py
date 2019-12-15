import os
import logging
import threading

def thread_api():
    os.system("python3 backend/api/api.py")

def thread_canteen():
    os.system("python3 microservices/canteen.py")
    
def thread_rooms():
    os.system("python3 microservices/rooms.py")
    
def thread_secretariats():
    os.system("python3 microservices/secretariats.py")

x = []
x.append(threading.Thread(target=thread_api))
x.append(threading.Thread(target=thread_canteen))
x.append(threading.Thread(target=thread_rooms))
x.append(threading.Thread(target=thread_secretariats))

for y in x:
    y.start()