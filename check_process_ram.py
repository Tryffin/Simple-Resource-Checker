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

print(check_process_ram("Code.exe"))