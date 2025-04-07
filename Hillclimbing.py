import random
from generator import generateCase

helperArray=[[0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
             [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
             [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
             [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
             [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
             [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
             [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
             [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]


sudoku_grid=[]

def genrate():
        population=[[],[],[],[],[],[],[],[],[]]
        for i in range(0,3):
            for j in range(0,3):
                numbers={1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9}
                checkHelperArray(numbers,i,j)#removes the numbers of the sub array in helper array from numbers
                for k in range(0,3):
                    for kk in range(0,3): 
                        num=random.randint(1,9)
                        while not num in numbers and len(numbers)>0:
                            num=random.randint(1,9)#pick a number that not in the sub array of helper array
                        if helperArray[3*i+k][3*j+kk]==0:
                            population[3*i+k].insert(3*j+kk,num)
                            numbers.pop(num)
                        else:
                            num=helperArray[3*i+k][3*j+kk]
                            population[3*i+k].insert(3*j+kk,num)
        return population
def checkHelperArray(numbers,i,j):#return valuse in the sub array
        for k in range(0,3):
            for kk in range(0,3):
                if helperArray[3*i+k][3*j+kk]!=0:
                    numbers.pop(helperArray[3*i+k][3*j+kk])



def printState(arr):
        print("[")
        for row in arr:
            print("[",end="")
            for element in row:
                print(element,end=" ,")
            print("]",end=",")
            print("")
        print("]")

def main():
    helperArray=generateCase()
    sudoku_grid=genrate()
    printState(helperArray)
    print()
    printState(sudoku_grid)


if __name__=="__main__":
    main()