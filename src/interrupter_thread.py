# -*- coding: utf-8 -*-
import threading

class InterrupterThread(threading.Thread):
    def __init__(self, interrupt_condition):
        threading.Thread.__init__(self)
        self.interrupt_condition = interrupt_condition
        self.thread_lock = threading.Lock()
        
    def run(self):
        input()
        self.thread_lock.acquire()
        if self.interrupt_condition:
            self.interrupt_condition = False
        else:
            self.interrupt_condition = True
        self.thread_lock.release()

    def should_interrupt(self):
        self.thread_lock.acquire()
        return_value = self.interrupt_condition
        self.thread_lock.release()
        return return_value
