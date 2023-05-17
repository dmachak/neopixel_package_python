# import the threading module
import threading
import time
 
class thread(threading.Thread):
    def __init__(self, thread_name, thread_ID, iterations):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.iterations = iterations
 
        # helper function to execute the threads
    def run(self):
        for i in range(self.iterations):
          print(str(self.thread_name) +" "+ str(self.thread_ID));
          time.sleep(1)
 
thread1 = thread("GFG", 1000, 5)
thread2 = thread("GeeksforGeeks", 2000, 10);
 
thread1.start()
thread2.start()
 
print("Exit")