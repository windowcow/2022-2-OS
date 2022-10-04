from tabulate import tabulate
import sys



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
            
        
        self.in_running = []
        self.in_asleep = []
        self.terminated = []
        
        self.queue0 = []
        self.queue1 = []
        self.queue2 = []
        
        self.time_quantum = 0 # time_quantum이 2면 queue0, 4면 queue1, sys.maxint 면 queue2다.
        self.remaining_time_quantum = 0
        
        for i in temp_processes:
            if i.init_queue == 0:
                self.queue0.append(i)
            elif i.init_queue == 1:
                self.queue1.append(i)
            elif i.init_queue == 2:
                self.queue2.append(i)
            else:
                print(f"Process{i} has invalid init_queue_number")
                exit()
        self.queue0.sort(key=lambda x: x.arrival_time)
        self.queue1.sort(key=lambda x: x.arrival_time)
        
        # q2를 [[cpu burst, io burst] ...] 로 만든다
        for i in temp_processes:
            temp_list = []
            for j, k in enumerate(i.burst_cycles):
                temp_list.append([j%2, k]) # 0은 cpu_burst, 1은 io_burst
            i.burst_cycles = temp_list
        
        
        # 여기서 q2_SRTF를 정렬해야함!
        self.sort_q2()
        
        
        
        # 이제 각 큐가 프로세스들로 채워졌음
        print(self.queue2[0].burst_cycles)
        print(self.queue2[1].burst_cycles)
        print(self.queue2[2].burst_cycles)
        print(self.queue2[2].total_burst_time)
        
        # 이제 모든 process들이 ready_queue에 들어있고 burst가 시작된다.
    # burst time은 1 단위로 계산한다.
        
    def start_running():
        self.in_running.append(self.queue0.pop(0))
        self.time_quantum = 2
        self.remaining_time_quantum = self.time_quantum
        
        while self.num_of_remaining_processes() > 0:
            things_to_be_done_in_next_1_turn()
    
    
            
    def things_to_be_done_in_next_1_turn():
        # 1. 현재 running process 처리하기
        # 2. asleep processes 처리
        # 3. ready processes 관리
        # 4. 다음 running process 고르기
        
        
        # 1. 현재 running process 처리하기
        # running 상태의 process의 burst time을 1 감소시킨다.  cpu_burst time = 0이면 burst_cycles.pop()을 하고 burst_cycles가 비어있으면 terminated로 보낸다.
        
        #### 여기에서 시간이 1 흐른다고 가정 ####
        # 1. in running에서
        self.in_running[0].burst_cycles[0][1] -= 1
        self.remaining_time_quantum -= 1
        
        if self.in_running[0].burst_cycles[0][1] == 0: # 해당 cpu burst cycle이 끝난 경우. (remaining time quantum이 있는데 끝난 경우를 의미!)
            self.in_running[0].burst_cycles.pop(0) # burst cycle 하나를 없앤다. 
            if self.in_running[0].burst_cycles == []:
                self.terminated.append(self.in_running.pop(0)) # burst cycle이 남아있지 않은 경우에 terminated로 보낸다.
            else:
                self.in_asleep.append(self.in_running.pop(0)) # burst cycle이 남아있는 경우에 asleep로 보낸다. (다음 burst cycle은 io_burst이기 때문임)
        else: # 해당 cpu burst cycle이 끝나지 않은 경우.
            if self.remaining_time_quantum == 0: # 근데 남은 time quantum이 0인 경우(남은 타임 퀀텀을 다 쓴 경우임. Qi+1로 보냄)
                if self.time_quantum == 2: # queue0에서 온 프로세스를 의미
                    self.queue1.append(self.in_running.pop(0)) # running에서 빼고 queue1에 넣는다.
                else if: self.time_quantum == 4: # queue1에서 온 프로세스를 의미
                    self.queue2.append(self.in_running.pop(0)) # running에서 빼고 queue2에 넣는다.
                else: # queue2에서 온 프로세스를 의미
                    self.queue2.append(self.in_running.pop(0)) # running에서 빼고 queue2에 넣는다.
            else: # 남은 타임 퀀텀을 쓰지도 않고 cpu burst cycle도 끝나지 않은 경우. 그냥 다음 턴으로 넘어간다.
                pass
        
        # 2. in asleep에서
        for process in self.in_asleep:
            process.burst_cycles[0][1] -= 1
            # 남은 io burst 가 0인 경우에는 ready queue로 보낸다.
            if process.burst_cycles[0][1] == 0:
                process.burst_cycles.pop(0)
                self.in_asleep.remove(process)
                self.in_running.append(process)
                
        # 3. in ready 에서
        for process in self.queue0:
            process.waiting_time += 1
        
        for process in self.queue1:
            process.waiting_time += 1
        
        for process in self.queue2:
            process.waiting_time += 1
        #### 여기에서 시간이 1 흐른다고 가정 #### END
        
        
        
        
        
        
        
            
            
            
        
        
        # 1. running 상태의 process를 계속 running에 두거나(q2만 남고 조건 만족 경우), ready_queue 중 하나 / in_asleep 으로  옮긴다. -
        # if self.time_quantum == sys.maxint:
        #     for process in queue2:
        #         pass
            
        
        # 2. waiting 상태의 process의 waiting time을 1 증가 또는 남은 io_burst를 1 감소시킨다. / io_burst = 0이면 ready queue로 보낸다.
        # 3. running이 비어있는 경우 ready queue에 있는 process 하나를 올려보낸다.
            
        
        

        
    def sort_q2(self):
        self.queue2.sort(key=lambda x: sum([int(i[1]) for i in x.burst_cycles if i[0]%2 == 0]))
        

                



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
    
    def next_burst(self):
        return self.burst_cycles[0]
    
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