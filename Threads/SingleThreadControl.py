from random import randint as r
from tqdm import trange
import threading
import time

################################################################
#   Question: How can we control a Single Thread from pythons  #
#             Threading Module                                 #
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
        __t = trange(10000, leave=False)
        for _ in __t:
            item = r(100, 10000)
            __t.set_description(f"[{item}]")
            if item >= 9800:
                self.controls.pause()
                time.sleep(2)
                self.controls.resume()
            
            time.sleep(0.01)
                
s = MainThread()
s.start()
    