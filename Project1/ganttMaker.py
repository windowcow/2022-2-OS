# process들의 정보를 받아서 gantt chart를 그려주는 프로그램
# 1초당 어떤 프로세스가 실행되는지를 표시
# 0: 
import string

test = [[1, 2], [2, 4], [3, 6], [4, 8], [5, 10], [6, 10], [7, 10], [7, 10], [7, 10], [7, 10]]


    


def textPieceFormatter(time : int ):

    
    return str(time).rjust(4)+"|"



def ganttMaker(processes : list):
    """
        time, pid를 형식에 맡게 바꾸어 다시 넣어주는 함수
    """
    def ganttPieceListMaker(time : int , pid : int ) :
        """
            time : |0001|
            pid : |0001|
        """
        return [textPieceFormatter(time), textPieceFormatter(pid)]
    
    gantt = []
    for process in processes:
        gantt.append(ganttPieceListMaker(process[0], process[1]))
        for i in range(len(gantt)-1):
            if gantt[i][1] == gantt[i+1][1] :
                gantt[i+1][1] = "-----"
    
    print("|", end="")
    for i in range(len(gantt)):
        print(gantt[i][0], end="")
    print("\n", end="")
    print("|", end="")
    for i in range(len(gantt)):
        print(gantt[i][1], end="")
        
                
    
    return gantt


gantt = ganttMaker(test)
