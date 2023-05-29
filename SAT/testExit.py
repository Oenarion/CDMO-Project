import sys
import time, threading
from multiprocessing import Process


finished = False

def foo():
    print("executing foo")
    print(time.time())
    # if finished == False:
    #     print("chiusura forzata")
    #     raise SystemExit(0)
    # #sys.exit("Error message")

# foo()


def main():
    time.sleep(10)
    print("ciao")
    

if __name__ == "__main__":
    thread = Process(target=main, args=())
    thread.start()
    startingTime = time.time()
    print("inizio")
    
    while(thread.is_alive() and time.time()-startingTime<5):
        continue

    if thread.is_alive():
        thread.terminate()
        
        print("thread killed")
   