import psutil
import sys
import time
import multiprocessing

# get process name from command line args
# ex: python Check_RAM.py (process)
# python Check_RAM.py node
if len(sys.argv) < 2:
	print ("missing process command arg")
	sys.exit()
 
class Monitor(multiprocessing.Process):
    def __init__(self, monitor_type, p_name, interval):
        multiprocessing.Process.__init__(self)
        self.monitor_type = monitor_type
        self.p_name = p_name
        self.interval = interval
    def run(self):
        self.monitor_type(self.p_name, self.interval)

def check_process_ram(name, interval):
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

def check_process_threads(name, interval):
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
        
        
def check_process_cpu(name, interval):
    sum = 0.0
    while True:
        for p in psutil.process_iter():
            if p.name() == name:
                cpu_percent = p.cpu_percent()
                print("PID " + str(p.pid) + " : " + name + " " +
                        str(cpu_percent) + " %")
                
                sum += cpu_percent
                continue
        print("Total CPU used by process " + name + " : " + str(sum) + " %\n")
        sum = 0
        time.sleep(interval)
        

def check_current_ram():
    mem = psutil.virtual_memory()
    total = str(round(mem.total / 1024**2, 2))
    used = str(round(mem.used / 1024**2, 2))
    used_per = str(round(mem.percent))
    free = str(round(mem.free / 1024**2, 2))
    print("Total memory size : " + total + " MB")
    print("Total used memory :" + used + " MB(" + used_per + "%)")
    print("Total available memory :" + free + " MB\n")


if __name__ == "__main__":
    
    # RAM monitorining
    check_current_ram()
    process_name = sys.argv[1]
    interval = 3
    p1 = Monitor(check_process_ram, process_name, interval)
    p2 = Monitor(check_process_threads, process_name, interval)
    p3 = Monitor(check_process_cpu, process_name, interval)
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
