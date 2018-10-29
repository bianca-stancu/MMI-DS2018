import threading

class MyThread(threading.Thread):
    def __init__(self,id):
        threading.Thread.__init__(self)
        self.id = id
        
    def run(self):
        print("Hello, from thread {}".format(self.id))
    
for i in range(10):
    c = MyThread(i)
    c.start()
