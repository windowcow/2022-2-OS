import numpy as np
from itertools import permutations
from prettytable import PrettyTable as pt

class Scheduler:
    """ Scheduling 을 행하는 클래스
    
    property:
        self.process_num : int / process의 개수
        self.resource_type_num : int / resource type의 갯수
        self.resource_unit_num : list[int] / resource type별 resource unit의 갯수
        
        
    
    """
    
    def __init__(self, input : list[str]):
        # input의 공백이나 빈 줄을 처리하는 부분
        input = [line.strip() for line in input]
        input = [line for line in input if line != '']
        
        # 첫 줄에 있는 metadata를 처리하는 부분
        first_line = input.pop(0)
        first_line = first_line.split(maxsplit = 2)
        self.process_num = int(first_line[0])
        self.resource_type_num = int(first_line[1])
        self.resource_units = first_line[2].split()
        self.resource_units = [int(i) for i in self.resource_units]
        
        # process의 current alloc, max claim 행렬을 저장하는 부분
        self.current_alloc_matrix = []
        self.max_claim_matrix = []
        
        for i in range(self.process_num):
            temp = input.pop(0)
            temp = temp.split()
            temp = [int(i) for i in temp]
            self.max_claim_matrix.append(temp)
            
        for i in range(self.process_num):
            temp = input.pop(0)
            temp = temp.split()
            temp = [int(i) for i in temp]
            self.current_alloc_matrix.append(temp)
        
        self.resource_units = np.array(self.resource_units)
        self.max_claim_matrix = np.array(self.max_claim_matrix)
        self.current_alloc_matrix = np.array(self.current_alloc_matrix)
        
    @property
    def available_resource_units(self):
        result = self.resource_units - self.current_alloc_matrix.sum(axis = 0)
        return result
    
    @property
    def additional_need(self):
        result = self.max_claim_matrix - self.current_alloc_matrix
        return result
    
    
    def showInitialState(self):
        print("\n====================================================")
        print("========== I N I T I A L    S T A T E ==============")
        print("====================================================\n")
        resourceUnitsNumTable = pt()
        processMaxClameTable = pt()
        processCurrentAllocTable = pt()
        processAdditionalNeedTable = pt()
        
        resourceUnitsNumTable.title = "Resource Units Numbers"
        processMaxClameTable.title = "Max Claim Matrix"
        processCurrentAllocTable.title = "Current Allocation Matrix"
        processAdditionalNeedTable.title = "Additional Need Matrix"
        
        resourceUnitsNumTableField_names = []
        processMaxClameTableField_names = ["Process Name"]
        processCurrentAllocTableField_names = ["Process Name"]
        processAdditionalNeedTableField_names = ["Process Name"]
        
        for i in range(self.resource_type_num):
            resourceUnitsNumTableField_names.append(f"Resource {i+1}")
            processMaxClameTableField_names.append(f"Resource {i+1}")
            processCurrentAllocTableField_names.append(f"Resource {i+1}")
            processAdditionalNeedTableField_names.append(f"Resource {i+1}")
            
        resourceUnitsNumTable.field_names = resourceUnitsNumTableField_names
        processMaxClameTable.field_names = processMaxClameTableField_names
        processCurrentAllocTable.field_names = processCurrentAllocTableField_names
        processAdditionalNeedTable.field_names = processAdditionalNeedTableField_names
        
        resourceUnitsNumTable.add_row(self.resource_units)
        for i in range(self.process_num):
            processMaxClameTable.add_row([f"Process {i+1}", *self.max_claim_matrix[i]])
            processCurrentAllocTable.add_row([f"Process {i+1}",  *self.current_alloc_matrix[i]])
            processAdditionalNeedTable.add_row([f"Process {i+1}",  *self.additional_need[i]])
       
       
        print(resourceUnitsNumTable, end = "\n\n")
        print(processMaxClameTable, end = "\n\n")
        print(processCurrentAllocTable, end = "\n\n")
        print(processAdditionalNeedTable, end = "\n\n")
        
    def isSafeState(self):
        """ 
        """
        target_cases = list(permutations(range(self.process_num)))
        count = 1
        
        for target_case in target_cases:
            isSafe = True
            print(f"\n=============================\n===========Case {count}===========")
            print(f"=============================")
            print("[  Test  ]: ", end = "")
            tempCount = 0
            for i in target_case:
                if tempCount == 0:
                    print(f"process {i+1}", end = " ")
                    tempCount += 1
                else:
                    print(f" -> process {i+1}", end = " ")
                
            temp_available_resource = self.available_resource_units
            print("\n[ Result ]: ", end= "")
            
            tempCount = 0
            for process_index in target_case:
                if (self.additional_need[process_index] <= temp_available_resource).all():
                    tempCount += 1
                    temp_available_resource += self.current_alloc_matrix[process_index]
                    print(f"process {process_index+1}", end = " ")
                    if tempCount != self.process_num:
                        print(" ->" , end = " ")
                else:
                    unsafeReasonList = temp_available_resource - self.additional_need[process_index]
                    print(f"process {process_index+1} // process {process_index+1} Makes State Unsafe")
                    # print(unsafeReasonList)
                    unsafeResourceIndex = np.where(unsafeReasonList < 0)[0]
                    tempReasonResourceIndex = unsafeResourceIndex
                    
                    lackResourceTable = pt()
                    lackResourceTable.title = "Lack Resource Table"
                    lackResourceTable.field_names = ["Process Name", *[f"Resource {i+1}" for i in range(self.resource_type_num)]]
                    lackResourceTable.add_row([f"Process {process_index+1}", *unsafeReasonList])
                    
                    tempString = ""
                    for i in unsafeResourceIndex:
                        if i == tempReasonResourceIndex[0]:
                            tempString += f"Resource Type {i+1}"
                        else:
                            tempString += f", Resource Type {i+1}"
                    print(lackResourceTable)
                    
                    print(f"Not enough {tempString} for the process {process_index+1}")
                    isSafe = False
                    break
                
            if isSafe:
                break
            else:
                print(f"=> NOT A SAFE STATE")
                count += 1
                # print("------------------------------")
                continue
        
        # if safe
        print(f"\n\n=> SAFE STATE for case {count} sequence")
        print("\n\n================================================================")
        print("======================= R E S U L T ============================")
        print("================================================================")
        
        print("\n\n==========================================================")
        print("============= S A F E    S E Q U E N C E =================")
        print("==========================================================\n")
        
        tempCount = 0
        for i in target_case:
            if tempCount == 0:
                print(f"process {i+1}", end = " ")
                tempCount += 1
            else:
                print(f" -> process {i+1}", end = " ")
        print("\n")
        
                
        return True
                
if __name__ == "__main__":
    file = open("input.txt", "r")
    input = file.readlines()
    file.close()
    scheduler = Scheduler(input)
    scheduler.showInitialState()
    scheduler.isSafeState()
    # scheduler.run()