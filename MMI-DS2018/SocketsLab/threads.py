from threading import Thread
from time import sleep

def say_hi(args):
    print ("Hi, I'm thread {}".format(args))
    sleep(10)
    

thread1 = Thread(target = say_hi, args = (1, ))
thread1.start()
thread2 = Thread(target = say_hi, args = (2, ))
thread2.start()
thread2.join()