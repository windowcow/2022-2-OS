from bisect import insort_right
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
            
        
        self.running = []
        self.asleep = []
        self.terminated = []
        
        self.r_queue0 = []
        self.r_queue1 = []
        self.r_queue2 = []
        
        self.time = -1
        self.time_quantum = 0 # time_quantum이 2면 queue0, 4면 queue1, sys.maxsize 면 queue2다.
        self.remaining_time_quantum = 0
        
        for i in temp_processes:
            if i.init_queue == 0:
                self.r_queue0.append(i)
            elif i.init_queue == 1:
                self.r_queue1.append(i)
            elif i.init_queue == 2:
                self.r_queue2.append(i)
            else:
                print(f"Process{i} has invalid init_queue_number")
                exit()
        
        # q2를 [[cpu burst, io burst] ...] 로 만든다
        for i in temp_processes:
            temp_list = []
            for j, k in enumerate(i.burst_cycles):
                temp_list.append([j%2, k]) # 0은 cpu_burst, 1은 io_burst
            i.burst_cycles = temp_list
        
        
        # 각각의 queue 정렬
        self.sort_q0()
        self.sort_q1()
        self.sort_q2()
        
        
        # 이제 모든 process들이 ready_queue에 들어있고 burst가 시작된다.
    # burst time은 1 단위로 계산한다.
        
    def start_running(self):
        temp_queue = []
        try:
            temp_queue.append(self.r_queue0.pop())
            self.time_quantum = 2
        except:
            try:
                temp_queue.append(self.r_queue1.pop())
                self.time_quantum = 4
            except:
                try:
                    temp_queue.append(self.r_queue2.pop())
                    self.time_quantum = sys.maxsize
                except:
                    pass
        
            
        self.running.append(temp_queue[0])
        self.remaining_time_quantum = self.time_quantum
        
        while self.num_of_remaining_processes() > 0:
            self.main_loop()
    
    def get_next_process_to_run(self):
        pass
    
    def main_loop(self):
        # 1. 현재 running process 처리하기
        # 2. asleep processes 처리
        # 3. ready processes 관리
        # 4. 다음 running process 고르기
        
        
        # 1. 현재 running process 처리하기
        # running 상태의 process의 burst time을 1 감소시킨다.  cpu_burst time = 0이면 burst_cycles.pop()을 하고 burst_cycles가 비어있으면 terminated로 보낸다.
        
        #### 여기에서 시간이 1 흐른다고 가정 ####
        # 1. in running에서
        self.time += 1
        self.burst_history.append([self.time, self.running[0].pid])
        
        self.remaining_time_quantum -= 1
        original_process = self.running[0]
        
        if self.running[0].burst_cycles[0][1] == 0: # 해당 cpu burst cycle이 끝난 경우. (remaining time quantum이 있는데 끝난 경우를 의미!)
            self.running[0].burst_cycles[0].pop(0) # burst cycle 하나를 없앤다. 
            if self.running[0].burst_cycles == []:
                self.terminated.append(self.running.pop(0)) # burst cycle이 남아있지 않은 경우에 terminated로 보낸다.
            elif self.running[0].burst_cycles[0][0] == 1: # 다음 burst cycle이 io_burst인 경우
                if self.time_quantum == 2:
                    temp_destination = self.r_queue0
                elif self.time_quantum == 4:
                    temp_destination = self.r_queue0
                elif self.time_quantum == sys.maxsize:
                    temp_destination = self.r_queue1
                
                self.asleep.append([self.running.pop(0), temp_destination]) # burst cycle이 남아있는 경우에 asleep로 보낸다. (다음 burst cycle은 io_burst이기 때문임)
            else: # 다음 burst cycle이 cpu_burst인 경우
                pass
                #근데 이 경우에는 원래 어디로 가야하는지도 정보를 보내야 한다.
        else: # 해당 프로세스의 cpu burst cycle이 끝나지 않은 경우.
            if self.remaining_time_quantum == 0: # 근데 남은 time quantum이 0인 경우(남은 타임 퀀텀을 다 쓴 경우임. Qi+1로 보냄)
                if self.time_quantum == 2: # queue0에서 온 프로세스를 의미
                    self.r_queue1.append(self.running.pop(0)) # running에서 빼고 queue1에 넣는다.
                elif self.time_quantum == 4: # queue1에서 온 프로세스를 의미
                    self.r_queue2.append(self.running.pop(0)) # running에서 빼고 queue2에 넣는다.
                else: # queue2에서 온 프로세스를 의미
                    self.r_queue2.append(self.running.pop(0)) # running에서 빼고 queue2에 넣는다.
            else: # 남은 타임 퀀텀을 쓰지도 않고 cpu burst cycle도 끝나지 않은 경우. preemption을 고려해야한다. 이 경우 원래 있던 큐로 넣는다고 가정.
                if self.time_quantum == 2:
                    if self.r_queue0 != []:
                        if self.r_queue0[0].arrival_time < original_process.arrival_time: 
                            self.r_queue0.append(self.running.pop(0))
                            self.running.append(self.r_queue0.pop(0))
                            return
                
                if self.time_quantum == 4:
                    if self.r_queue0 != []:
                        self.r_queue0.append(self.running.pop(0)) # 이 두 줄은 그냥 서로 바꾸는 의미다. 
                        self.running.append(self.r_queue0.pop(0))
                        return
                            
                    if self.r_queue1 != []:
                        if self.r_queue1[0].arrival_time < original_process.arrival_time: 
                            self.r_queue1.append(self.running.pop(0))
                            self.running.append(self.r_queue1.pop(0))
                            return
                
                if self.time_quantum == sys.maxsize:
                    if self.r_queue0 != []:
                        self.r_queue0.append(self.running.pop(0)) # 이 두 줄은 그냥 서로 바꾸는 의미다. 
                        self.running.append(self.r_queue0.pop(0))
                        return
                            
                    if self.r_queue1 != []:
                        self.r_queue1.append(self.running.pop(0)) # 이 두 줄은 그냥 서로 바꾸는 의미다. 
                        self.running.append(self.r_queue1.pop(0))
                        return
                        
                    if self.r_queue2 != []:
                        if self.r_queue2[0].remaining_time < original_process.remaining_time: 
                            self.r_queue2.append(self.running.pop(0))
                            self.running.append(self.r_queue2.pop(0))
                            return
                
                target_process = self.running[0]
                original_process = self.running[0]
                self.sort_q1()
                
                if target_process != original_process:
                    
                    self.running.append(target_process)
                    return
                
                # 2번쨰 preemption 조건
                for process in self.r_queue1:
                    if process.arrival_time <= target_process.arrival_time:
                        if self.time_quantum == 2:
                            self.r_queue0.append(self.running.pop(0))
                        elif self.time_quantum == 4:
                            self.r_queue1.append(self.running.pop(0))
                        else:
                            self.r_queue2.append(self.running.pop(0))
                        target_process = process
                if target_process != original_process:
                    self.running.append(target_process)
                    return
                
                # 3번째 preemption 조건
                for process in self.r_queue2:
                    if process.arrival_time <= target_process.arrival_time:
                        if self.time_quantum == 2:
                            self.r_queue0.append(self.running.pop(0))
                        elif self.time_quantum == 4:
                            self.r_queue1.append(self.running.pop(0))
                        else:
                            self.r_queue2.append(self.running.pop(0))
                        target_process = process  
                          
                if target_process != original_process:
                    self.running.append(target_process)
                    return
                
                
        # 2. in asleep에서
        for index, (process, destination) in enumerate(self.asleep):
            process.burst_cycles[0][1] -= 1
            # 남은 io burst 가 0인 경우에는 ready queue로 보낸다.
            if process.burst_cycles[0][1] == 0:
                process.burst_cycles.pop(0)
                if process.burst_cycles == []:
                    self.finished_processes.append(process)
                    self.running.remove(process)
                self.asleep.pop(index)
                destination.append(process)
                
        # 3. in ready 에서
        for process in self.r_queue0:
            process.waiting_time += 1
        
        for process in self.r_queue1:
            process.waiting_time += 1
        
        for process in self.r_queue2:
            process.waiting_time += 1
        #### 여기에서 시간이 1 흐른다고 가정 #### END
        self.running.append(self.get_next_process())
        
        
    def sort_q0(self):
        self.r_queue0.sort(key=lambda x: x.arrival_time)
        
    def sort_q1(self):
        self.r_queue1.sort(key=lambda x: x.arrival_time)
        
    def sort_q2(self):
        self.r_queue2.sort(key=lambda x: sum([int(i[1]) for i in x.burst_cycles if i[0]%2 == 0]))
        
    def num_of_remaining_processes(self):
        return len(self.r_queue0) + len(self.r_queue1) + len(self.r_queue2) + len(self.asleep) + len(self.running)
    
    def get_next_process(self):
        if self.running == []:
            if self.r_queue0 != []:
                return self.r_queue0.pop(0)
            elif self.r_queue1 != []:
                return self.r_queue1.pop(0)
            elif self.r_queue2 != []:
                return self.r_queue2.pop(0)
            else:
                return None

                



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
        sum = 0
        for i in self.burst_cycles:
            if i[0] == 0:
                sum += i[1]
                
        return sum
    
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
    scheduler = Scheduler(input)
    scheduler.start_running()