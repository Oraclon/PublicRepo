from random import randint as r
from tqdm import trange
import threading
import time

#################################################################
#   Question: How can we control a Single Thread from pythons   #
#             Threading Module on a FOR loop                    #
#                                                               #
#   Answer: By default when you create a Thread with Pythons    #
#           Threading Module it has 2 hidden values the FLAG    #
#           and RUNNING so if you define a Threading Event in   #
#           them like it happens in ThreadControls class        #
#           you can use by using SET or CLEAR in order to       #
#           be able to control the thread on each itteration    #
#################################################################

CreatedThreads = dict()

class ThreadControls:
    """
        This will control the attached Thread
    """
    def __init__(self):
        self.__running = threading.Event()
        self.__running.set()
        self.__flag = threading.Event()
        self.__flag.set()
        
    def pause(self):
        self.__flag.clear()
    def resume(self):
        self.__flag.set()
    def stop(self):
        self.__flag.set()
        self.__running.clear()
    def check_running(self):
        return self.__running.is_set()
    def check_flag(self):
        self.__flag.wait()

class MainThread(threading.Thread):
    """
        This is the main thread that will be
        controlled by a ThreadControls class
    """
    def __init__(self, counter=None):
        super().__init__()
        self.counter = counter
        self.name = f"[WORKER{self.counter}]"
        self.controls = ThreadControls()
    def run(self):
        __t = trange(2200, leave=False)
        for _ in __t:
            self.controls.check_flag()
            t = round(time.time() * 1000, 3)
            item = r(100, 10000)
            if item > 9600:
                self.controls.pause()
                __t.set_description(f"[{item} | {t}]")
                time.sleep(2)
                self.controls.resume()
            time.sleep(0.03)

# s = MainThread()
# s.start()
    