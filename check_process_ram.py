import psutil as ps


def check_process_ram(name):
    sum = 0
    for i in range(len(ps.pids())):
        p = ps.Process(ps.pids()[i])
        if p.name() == name:
            print("PID " + str(ps.pids()[i]) + " : " + name + " " +
                  str(round(p.memory_percent() * (ps.virtual_memory()[0]/(1024**2) )/100, 2)) + 
                    " MB")
            sum += round(p.memory_percent() * (ps.virtual_memory()[0]/(1024**2) )/100, 2)
            continue
    print("Total memory use : " + str(round(sum, 2)) + " MB")

def check_current_ram():
    mem = ps.virtual_memory()
    total = str(round(mem.total / 1024**2, 2))
    used = str(round(mem.used / 1024**2, 2))
    used_per = str(round(mem.percent))
    free = str(round(mem.free / 1024**2, 2))
    print("Total memory size : " + total + " MB")
    print("Total used memory :" + used + " MB(" + used_per + "%)")
    print("Total available memory :" + free + " MB")

print(check_current_ram())