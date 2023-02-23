from tqdm import trange
from random import randint as r
import threading
from queue import Queue
import time

class ThreadControls:
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
    def keep_up(self):
        self.__flag.wait()
    def check_run(self):
        return self.__running.is_set()

class MainThread(threading.Thread):
    def __init__(self, count = None):
        super().__init__()
        self.name = f"WORK[{count}]"
        self.count = count
        self.controls = ThreadControls()
        self.counter = 0
        self.queue = Queue()

        self.observer = ThreadObserver(countrols=self.controls,
                                       queue=self.queue,
                                       counter=count)
        self.observer.start()

    def run(self):
        __t = trange(2000, leave=False)
        for _ in __t:
            self.controls.keep_up()
            item = r(100, 10000)
            if item > 9900:
                ti = round(time.time() * 1000, 3)
                self.counter += 1
                __t.set_description(f"[ WORK{self.count} | {self.counter} | {ti}]")
                self.queue.put(1)
            time.sleep(0.01)
        self.queue.put(None)
        self.controls.stop()

class ThreadObserver(threading.Thread):
    def __init__(self, countrols=None, 
                       queue = None, 
                       counter = None):
        super().__init__()
        self.controls = countrols
        self.queue = queue
        self.name = f"OBSER[{counter}]"
    
    def run(self):
        while self.controls.check_run():
            item = self.queue.get()
            if item is not None:
                self.controls.pause()
                time.sleep(2)
                self.controls.resume()
            else:
                break

# threa = MainThread(count=1)
# threa.start()