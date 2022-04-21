import psutil, os, tracemalloc
from memory_profiler import profile

def check_process_ram(name):
    sum = 0
    for i in range(len(psutil.pids())):
        p = psutil.Process(psutil.pids()[i])
        if p.name() == name:
            print("PID " + str(psutil.pids()[i]) + " : " + name + " " +
                  str(round(p.memory_percent() * (psutil.virtual_memory()[0]/(1024**2) )/100, 2)) + 
                    " MB")
            sum += round(p.memory_percent() * (psutil.virtual_memory()[0]/(1024**2) )/100, 2)
            continue
    print("Total memory use : " + str(round(sum, 2)) + " MB")

def check_current_ram():
    mem = psutil.virtual_memory()
    total = str(round(mem.total / 1024**2, 2))
    used = str(round(mem.used / 1024**2, 2))
    used_per = str(round(mem.percent))
    free = str(round(mem.free / 1024**2, 2))
    print("Total memory size : " + total + " MB")
    print("Total used memory :" + used + " MB(" + used_per + "%)")
    print("Total available memory :" + free + " MB")

# inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

# decorator function
# def profile(func):
#     def wrapper(*args, **kwargs):

#         mem_before = round(process_memory()/ 1024**2, 2)
#         result = func(*args, **kwargs)
#         mem_after = round(process_memory()/ 1024**2, 2)
#         print("Fucntion {} :consumed memory: {:,} MB".format(
#             func.__name__,
#             mem_before, mem_after, mem_after - mem_before))
#         return result
#     return wrapper

# instantiation of decorator function
@profile
# main code for which
# memory has to be monitored
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

func1()
tracemalloc.start()
func2()
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**2}MB; Peak was {peak / 10**2}MB")
tracemalloc.stop()
