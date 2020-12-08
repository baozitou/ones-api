# -*- coding: UTF-8 -*-
import threading
import time

class MyThread(threading.Thread):
    def __init__(self,func, kwargs):
        threading.Thread.__init__(self)
        self.func = func
        self.kwargs = kwargs

    def run(self):
        print("开始线程："+self.name)
        self.func(**self.kwargs)
        print("结束线程："+self.name)


def do_thread(func_name, data_list, arg_name:str, thread_num:int=2, **kwargs):
    list_len = len(data_list)
    half_len = list_len // thread_num
    thread_list = []
    for i in range(thread_num):
        d = data_list[half_len*i: half_len*(i+1)]
        thread_i = MyThread(func=func_name, kwargs={arg_name:d, "name":"Thread-{}".format(i+1)})
        thread_list.append(thread_i)

    print(thread_list)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("完成了")
