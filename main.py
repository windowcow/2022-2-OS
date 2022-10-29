from OperatingSystem import OperatingSystem

if "__main__" == __name__:
    # file = open("input1.txt", "r")
    # file = open("input2.txt", "r")
    # file = open("input3.txt", "r")
    file = open("input4.txt", "r")
    input = file.readlines()
    file.close()
    
    operatingSystem = OperatingSystem(input)
    operatingSystem.showInitialState()
    operatingSystem.isSafeState()
    operatingSystem.showInitialState()