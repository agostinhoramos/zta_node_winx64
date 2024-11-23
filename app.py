#!/usr/bin/python3

import threading, sys, os
from controller import app as ControllerApp
from automation import auto as WorkerAuto

def main():
    
    PROJECT_NAME="ZTA"
    
    print(f"Starting **{PROJECT_NAME}** server\n")
    
    func_threads = [
        [ControllerApp.run, (), {'host': '0.0.0.0', 'port': 5000, 'ssl_context': ('cert.pem', 'key.pem')}],
        [WorkerAuto.run, (), {}],
    ]

    # Start threads
    threads = []
    for fn in func_threads:
        target_function = fn[0]
        args = fn[1] if len(fn) > 1 else ()
        kwargs = fn[2] if len(fn) > 2 else {} 

        th = threading.Thread(target=target_function, args=args, kwargs=kwargs)
        th.start()
        threads.append(th)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()