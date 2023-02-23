from random import randint as r
from tqdm import trange
import threading
import time

################################################################
#   Question: How can we control a Single Thread from pythons  #
#             Threading Module on a WHILE loop                 #
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