from random import randint as r
from tqdm import trange
import threading
import time
import os

################################################################
#   Question: How can we control a Single Thread from pythons  #
#             Threading Module on a FOR loop                   #
#                                                              #
#   Answer: By default when you create a Thread with Pythons   #
#           Threading Module it has 2 hidden values the FLAG   #
#           and RUNNING so if you define a Threading Event in  #
#           them like it happens in ThreadControls class       #
#           you can use by using SET or CLEAR in order to      #
#           be able to control the thread on each itteration   #
################################################################

CreatedThreads = dict()

class ThreadControls:
    """
        This will control the attached Thread
    """
    def __init__(self):
        self.running = threading.Event()
        self.running.set()
        self.flag = threading.Event()
        self.flag.set()
        
    def pause(self):
        self.flag.clear()
    def resume(self):
        self.flag.set()
    def stop(self):
        self.flag.set()
        self.running.clear()

class MainThread(threading.Thread):
    """
        This is the main thread that will be
        controlled by a ThreadControls class
    """
    def __init__(self, counter=None):
        super().__init__()
        self.counter = counter
        self.controls = ThreadControls()
        self.status = self.controls.flag._flag
    def run(self):
        while self.controls.running.is_set():
            os.system("clear")
            t = round(time.time() * 1000, 3)
            self.controls.flag.wait()
            item = r(100, 10000)
            if item > 9990:
                self.controls.stop()
                print(f"Terminated [{t} | {item}]")

            elif ((item >=9700) and (item <=9989)):
               self.controls.pause()
               print(f"Paused [{t} | {item}]")
               time.sleep(2)
               self.controls.resume()
               print(f"Resumed [{t} | {item}]")

s = MainThread()
s.start()
    