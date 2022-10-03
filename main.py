from tabulate import tabulate

#down arrow
down_arrow = "|\nV"
f = open("input.txt", "r")
input = f.readlines()
f.close



class ReadyQueue:
    def __init__(self, input: str):
        self.num_of_processes = int(input[0])
        self.burst_history = []
        temp_processes = []
        try:
            for i in range(1, len(input)):
                temp_process = input[i].split(" ", maxsplit=4)
                temp_processes.append(Process(int(temp_process[0]), 
                                            int(temp_process[1]), 
                                            int(temp_process[2]),
                                            int(temp_process[3]),
                                            int(temp_process[4])))
        except:
            print("File is not in a right format")
            exit()
        
        q0_RR = []
        q1_RR = []
        q2_SRTF = []
        
        for i in temp_processes:
            if i.init_queue == 0:
                q0_RR.append(i)
            elif i.init_queue == 1:
                q1_RR.append(i)
            elif i.init_queue == 2:
                q2_SRTF.append(i)
            else:
                print(f"Process{i} has invalid init_queue_number")
                exit()
        # 이제 각 큐가 프로세스들로 채워졌음
    
    def burst(self):
        if len(q0_RR) > 0:
            pass
        
    


class Process:
    def __init__(self, pid: int, arrival_time: int, init_queue: int, num_of_cycles: int, burst_cycles: list):
        self.pid = pid
        self.arrival_time = arrival_time
        self.init_queue = init_queue
        self.num_of_cycles = num_of_cycles
        self.burst_cycles = burst_cycles
        self.process_state = 0 # 0: ready, 1: blocked, 2: running, 3: terminated
    
    def remaining_time(self):
        pass
    
    def burst(self, burst_time: int):
        pass