import time
import threading
from queue import Queue
from tqdm import trange
from random import randint as r

runningThreads = dict()

class ThreadControls:
    """_"""
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
    def check_run(self):
        return self.__running.is_set()
    def check_flag(self):
        self.__flag.wait()

class MainThread(threading.Thread):
    def __init__(self, cid=None):
        super().__init__()
        self.cid = cid
        self.name = f"Worker{self.cid}"
        self.queue = Queue()
        self.controls = ThreadControls()
        self.counter = 0

        observer = ThreadObserver(cid=self.cid, queue=self.queue)
        observer.start()

    def run(self):
        __t = trange(1200, leave=False)
        for _ in __t:
            self.controls.check_flag()
            item = r(100, 10000)
            if item > 9950:
                self.counter += 1
                __t.set_description(f"[{self.name} | {self.counter} | {round(time.time()* 1000, 2)}]")
                self.queue.put(1)
            time.sleep(0.03)
        self.queue.put(None)
        self.controls.stop()

class ThreadObserver(threading.Thread):
    def __init__(self, cid=None, queue=None):
        super().__init__()
        self.cid = cid
        self.queue = queue
    
    def run(self):
        while True:
            item = self.queue.get()
            if item is not None:
                self.PauseAll(self.cid)
                time.sleep(2)
                self.ResumeAll(self.cid)
            else:
                break

    def PauseAll(self, running):
        for idx, item in runningThreads.items():
            if idx != running:
                item.controls.pause()
    def ResumeAll(self, running):
        for idx, item in runningThreads.items():
            if idx != running:
                item.controls.resume()

for i in range(3):
    thr = MainThread(cid=i)
    runningThreads[i] = thr
    thr.start()
