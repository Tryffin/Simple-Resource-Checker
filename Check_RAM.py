import psutil, os, tracemalloc
from memory_profiler import profile

def check_process_ram(name):
    sum = 0
    for i in range(len(psutil.pids())):
        p = psutil.Process(psutil.pids()[i])
        if p.name() == name:
            print("PID " + str(psutil.pids()[i]) + " : " + name + " " +
                    str(round(p.memory_info()[0] / 1024**2, 2)) + " MB")
            
            sum += round(p.memory_info()[0] / 1024**2, 2)
            continue
    print("Total memory used by process " + name + " : " + str(round(sum, 2)) + " MB")

def check_process_threads(name):
    sum = 0
    for i in range(len(psutil.pids())):
        p = psutil.Process(psutil.pids()[i])
        if p.name() == name:
            print("PID " + str(psutil.pids()[i]) + " : " + name + " " +
                    str(p.num_threads()) + " threads")
            
            sum += p.num_threads()
            continue
    print("Total threads used by process " + name + " : " + str(sum) + " threads")

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

func1()

tracemalloc.start()
func2()
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**2}MB; Peak was {peak / 10**2}MB")
tracemalloc.stop()

check_current_ram()
check_process_ram("javaw.exe")
check_process_threads("javaw.exe")
