from random import randint as r
from tqdm import trange
import threading
import time

CreatedThreads = dict()

class ThreadControls:
    """
        This will control the attached Thread
    """
    def __init__(self):
        self.running = threading.Event()
        self.flag = threading.Event()

        self.running.set()
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
        controlled
    """
    def __init__(self, counter=None):
        super().__init__()
        self.counter = counter
        self.controls = ThreadControls()
        self.status = self.controls.flag._flag
    def run(self):
        __t = trange(10000, leave=False)
        while self.controls.running.is_set():
            for _ in __t:
                if self.controls.running.is_set():
                    self.controls.flag.wait()
                    item = r(100, 10000)

                    __t.set_description(f"[{item}]")
                    if item >= 9900:
                        self.controls.stop()
                        time.sleep(1)

                    elif item >= 9800:
                        self.controls.pause()
                        time.sleep(2)
                        self.controls.resume()
            
                time.sleep(0.01)
            break
                
s = MainThread()
s.start()