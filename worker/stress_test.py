#!./venv/bin/python3

import sys
import threading
import requests


url = 'http://127.0.0.1:8001'
num_threads = 1000 if len(sys.argv) == 1 else int(sys.argv[1])

def make_request():
    try:    
        _ = requests.get(url)
        print(f'{threading.current_thread().name} 200')
    except Exception as e:
        print(f'{threading.current_thread().name} raised {e}')
        
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=make_request, name=f'Thread-{i+1}')
    thread.start()
    threads.append(thread)
    
for thread in threads: thread.join()