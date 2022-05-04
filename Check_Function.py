import os, psutil, tracemalloc

from memory_profiler import profile

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
        print("Fucntion {} : used memory: {:,} MB\n".format(
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
    func1()
    
    tracemalloc.start()
    func2()
    current, peak = tracemalloc.get_traced_memory()
    print(f"func2 : Current memory usage is {current / 10**2}MB; Peak was {peak / 10**2}MB\n")
    tracemalloc.stop()
    
    func3()