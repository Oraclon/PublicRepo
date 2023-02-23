from random import randint as r
import threading
import time
import os

#################################################################
#   Question: How can we control a Single Thread from pythons   #
#             Threading Module on a WHILE loop                  #
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
    def check_flag(self):
        self.__flag.wait()
    def check_run(self):
        return self.__running.is_set()

class MainThread(threading.Thread):
    """
        This is the main thread that will be
        controlled by a ThreadControls class
    """
    def __init__(self, counter=None):
        super().__init__()
        self.counter = counter
        self.controls = ThreadControls()
    def run(self):
        while self.controls.check_run():
            os.system("clear")
            t = round(time.time() * 1000, 3)
            self.controls.check_flag()
            item = r(100, 10000)
            if item > 9990:
                self.controls.stop()
                print(f"Terminated [{t} | {item}]")

            elif ((item >=9700) and (item <=9989)):
                self.controls.pause()
                print(f"Paused [{t} | {item}]")
                time.sleep(1)
                self.controls.resume()
                print(f"Resumed [{t} | {item}]")

s = MainThread()
s.start()