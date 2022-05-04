import os, psutil, tracemalloc
import time
import multiprocessing
from memory_profiler import profile
from py import process


interval = 3
def check_process_ram(name):
    sum = 0
    while True:
        for p in psutil.process_iter():
            if p.name() == name:
                print("PID " + str(p.pid) + " : " + name + " " +
                        str(round(p.memory_info()[0] / 1024**2, 2)) + " MB")
                
                sum += round(p.memory_info()[0] / 1024**2, 2)
                continue
        print("Total memory used by process " + name + " : " + str(round(sum, 2)) + " MB\n")
        sum = 0
        time.sleep(interval)

def check_process_threads(name):
    sum = 0
    while True:
        for p in psutil.process_iter():
            if p.name() == name:
                print("PID " + str(p.pid) + " : " + name + " " +
                        str(p.num_threads()) + " threads")
                
                sum += p.num_threads()
                continue
        print("Total threads used by process " + name + " : " + str(sum) + " threads\n")
        sum = 0
        time.sleep(interval)
        
        
def check_process_cpu(name):
    sum = 0
    while True:
        for p in psutil.process_iter():
            if p.name() == name:
                print("PID " + str(p.pid) + " : " + name + " " +
                        str(p.cpu_percent()) + " %")
                
                sum += p.cpu_percent()
                continue
        print("Total CPU used by process " + name + " : " +  str(round(sum, 2)) + " %\n")
        sum = 0
        time.sleep(interval)
        
class Monitor(multiprocessing.Process):
    def __init__(self, monitor_type, p_name):
        multiprocessing.Process.__init__(self)
        self.monitor_type = monitor_type
        self.p_name = p_name
        
    def run(self):
        self.monitor_type(self.p_name)
        

def check_current_ram():
    mem = psutil.virtual_memory()
    total = str(round(mem.total / 1024**2, 2))
    used = str(round(mem.used / 1024**2, 2))
    used_per = str(round(mem.percent))
    free = str(round(mem.free / 1024**2, 2))
    print("Total memory size : " + total + " MB")
    print("Total used memory :" + used + " MB(" + used_per + "%)")
    print("Total available memory :" + free + " MB\n")

#inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def profile_psutil(func):
    def wrapper(*args, **kwargs):
        mem_before = round(process_memory()/ 1024**2, 2)
        result = func(*args, **kwargs)
        mem_after = round(process_memory()/ 1024**2, 2)
        print("Fucntion {} :consumed memory: {:,} MB\n".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before))
        return result
    return wrapper

@profile
def func1():
    x = [x for x in range(0, 1000)]
    y = [y*100 for y in range(0, 1500)]
    del x
    return y

def func2():
    x = [x for x in range(0, 1000)]
    y = [y*100 for y in range(0, 1500)]
    del x
    return y

@profile_psutil
def func3():
    x = [x for x in range(0, 1000)]
    y = [y*100 for y in range(0, 1500)]
    del x
    return y

if __name__ == "__main__":
    # Function memory monitorining
    func1()
    
    tracemalloc.start()
    func2()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10**2}MB; Peak was {peak / 10**2}MB\n")
    tracemalloc.stop()
    
    func3()
    
    # RAM monitorining
    check_current_ram()
    process_name = "SpaceClaim.exe"
    p1 = Monitor(check_process_ram, process_name)
    p2 = Monitor(check_process_threads, process_name)
    p3 = Monitor(check_process_cpu, process_name)
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
