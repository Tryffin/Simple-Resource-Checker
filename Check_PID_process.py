import sys
import time
import psutil

# get pid from command line args
# ex: python Check_PID_process.py (pid)
# python Check_PID_process.py 1234
if len(sys.argv) < 2:
	print ("missing pid command arg")
	sys.exit()

# get process from PID of input
pid = int(sys.argv[1])
p = psutil.Process(pid)

# polling interval seconds
interval = 3 

# monitor process and write data to csv file
with open("process_" + p.name() + '_' + str(pid) + ".csv", "a+") as f:
    # titles of csv 
    f.write("Time,CPU%,RAM,RAM%\n") 
    while True:
        current_time = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
        cpu_percent = p.cpu_percent()
        mem_used = p.memory_info().rss / (1024**2)
        mem_percent = p.memory_percent()
        line ="Time : " + current_time + " , CPU : " + str(cpu_percent) + " % , RAM : "+ str(round(mem_used,2)) + " MB , " + str(round(mem_percent,2)) + " %"
        print(line)
        f.write(line + "\n")
        time.sleep(interval)
