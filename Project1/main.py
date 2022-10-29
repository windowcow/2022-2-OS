from tabulate import tabulate




class Scheduler:
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
                                            [int(i) for i in temp_process[4].split(" ")]))
        
        
                
                
        except:
            print("File is not in a right format")
            exit()
        
        
                
        self.q0_RR = []
        self.q1_RR = []
        self.q2_SRTF = []
        
        
        for i in temp_processes:
            if i.init_queue == 0:
                self.q0_RR.append(i)
            elif i.init_queue == 1:
                self.q1_RR.append(i)
            elif i.init_queue == 2:
                self.q2_SRTF.append(i)
            else:
                print(f"Process{i} has invalid init_queue_number")
                exit()
        self.q0_RR.sort(key=lambda x: x.arrival_time)
        self.q1_RR.sort(key=lambda x: x.arrival_time)
        
        # q2를 [[cpu burst, io burst] ...] 로 만든다
        for i in temp_processes:
            temp_list = []
            for j, k in enumerate(i.burst_cycles):
                temp_list.append([j%2, k]) # 0은 cpu_burst, 1은 io_burst
            i.burst_cycles = temp_list
        
        
        # 여기서 q2_SRTF를 정렬해야함!
        self.sort_q2()
        
        
        
        # 이제 각 큐가 프로세스들로 채워졌음
        print(self.q2_SRTF[0].burst_cycles)
        print(self.q2_SRTF[1].burst_cycles)
        print(self.q2_SRTF[2].burst_cycles)
        print(self.q2_SRTF[2].total_burst_time)
        
    def sort_q2(self):
        self.q2_SRTF.sort(key=lambda x: sum([int(i[1]) for i in x.burst_cycles if i[0]%2 == 0]))
        
    def scheduling(self):
        pass
    
    def q0_burst(self):
        
        # q0에서 time quantum을 전부 쓰는 process를 처리하는 경우
        if (self.q0_RR[0].burst_cycle[0][1] > 2):
            self.q0_RR[0].burst_cycle[0][1] -= 2
            self.q1_RR.append(self.q0_RR.pop(0))
                
    def perform_io_burst(self, time: int):
        # ready_queue에 있는 process들에 대해서 io_burst가 필요한 프로세스들에게 하는 행동.
        for ready_queue in [self.q0_RR, self.q1_RR, self.q2_SRTF]:
            for process in ready_queue:
                # io_burst를 기다리는 경우!
                if process.burst_cycles[0][0] == 1:
                    if process.burst_cycles[0][1] <= time:
                        process.burst_cycles.pop(0)
                        # io burst도 안하고 ready queue 에서 기다리는 시간
                        process.waiting_time += time - process.burst_cycles[0][1]
                    
                
    def process_in_waiting(self):
        
    def dispatch(self):
        
        if len(self.q0_RR) > 0:
            time_quantum = 2
        elif len(self.q1_RR) > 0:
            time_quantum = 4
        elif len(self.q2_SRTF) > 0:
            time_quantum = 999
        else:
            exit()

        def burst_proc(process: Process):
            if len(self.q0_RR) > 0:
                pass
            
    


class Process:
    def __init__(self, pid: int, arrival_time: int, init_queue: int, num_of_cycles: int, burst_cycles: list):
        self.pid = pid
        self.arrival_time = arrival_time
        self.init_queue = init_queue
        self.num_of_cycles = num_of_cycles
        self.burst_cycles = burst_cycles
        
        self.total_burst_time = sum(self.burst_cycles) 
        self.waiting_time = 0
        self.turnaround_time = 0 # turnaround time은 waiting time + cpu burst time + io burst time이다.
        # cpu_burst_time이 0이면 끝난 프로세스다.
        
    def remaining_time(self):
        pass
    
    def cpu_burst_time(self, burst_time: int):
        pass
    
    def turnaround_time(self):
        return self.waiting_time + self.total_burst_time
    
        
    
    



#down arrow
down_arrow = "|\nV"


f = open("input.txt", "r")
input = f.readlines()
f.close

if __name__ == "__main__":
    Scheduler(input)