import random
import math
import copy
import generator
import time
import multiprocessing
from State import State
import numpy as np
helperArray = [
[0 ,5 ,4 ,6 ,1 ,0 ,8 ,0 ,9 ,],
[8 ,7 ,9 ,0 ,4 ,0 ,2 ,6 ,0 ,],
[6 ,2 ,0 ,0 ,0 ,0 ,4 ,0 ,0 ,],
[0 ,0 ,0 ,1 ,0 ,6 ,0 ,0 ,8 ,],
[0 ,4 ,5 ,2 ,8 ,0 ,6 ,1 ,3 ,],
[1 ,0 ,0 ,4 ,9 ,0 ,7 ,5 ,2 ,],
[4 ,0 ,3 ,8 ,0 ,1 ,0 ,0 ,7 ,],
[0 ,0 ,8 ,7 ,0 ,0 ,0 ,0 ,6 ,],
[0 ,1 ,0 ,0 ,6 ,0 ,3 ,0 ,4 ,],
]
bestState = State( [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                ])
# answerLock = threading.Lock()
def swap(pos1, pos2, table):
    temp = table[pos1[0]][pos1[1]]
    table[pos1[0]][pos1[1]] = table[pos2[0]][pos2[1]]
    table[pos2[0]][pos2[1]] = temp
    
def printState(arr):
        print("[")
        for row in arr:
            print("[",end="")
            for element in row:
                print(element,end=" ,")
            print("]",end=",")
            print("")
        print("]")
        

    

        

def fitnessfunction2(sudoku)-> int:# try to minimize(max is 5000)
    fitness=0
    for i in range(0,9):
        Hreaccurance=[0,0,0,0,0,0,0,0,0,0]#first index is not considered so i can start with 1 to 9(Horizontal reaccurance)
        Vreaccurance=[0,0,0,0,0,0,0,0,0,0]#first index is not considered so i can start with 1 to 9(virtecal reaccurance)
        for j in range(0,9):
            if Hreaccurance[sudoku[i][j]]>=1 and sudoku[i][j]!=0:
                fitness+=1
            if Vreaccurance[sudoku[j][i]]>=1 and sudoku[j][i]!=0:
                fitness+=1
            Hreaccurance[sudoku[i][j]]+=1
            Vreaccurance[sudoku[j][i]]+=1
    return 5000-fitness


        
                
        
        




class GA:
    def __init__(self, helperArray):
        self.PM=0.6#probability of mutation
        self.PM2 = 0.0
        self.POPULATION_SIZE = 5
        self.CHILDREN_NUM = 10
        self.ITERATIONS_NUM = 5000
        self.helperArray= helperArray
        printState(self.helperArray)
        print()
        self.addInference()
        printState(self.helperArray)
        


    
        
    def addInference(self):
        # pass
        poss = np.ones((9, 9, 10))
        for i in range(9):
            for j in range(9):
                if(self.helperArray[i][j] != 0):
                    numm = self.helperArray[i][j]
                    blockRow , blockCol = i//3 * 3 , j //3 * 3
                    for k in range(9):
                    
                        poss[i][k][numm] = 0
                        
                    for k in range(9):
                        poss[k][j][numm] = 0
                        
                    for k in range(blockRow, blockRow + 3):
                        for h in range(blockCol , blockCol + 3):
                            
                            # print(k, h, numm)
                            poss[k][h][numm] == 0
        
        
        fl = 0
        while fl == 0:
            fl = 1               
            for i in range(9):
                for j in range(9):
                    if(self.helperArray[i][j] != 0):
                        continue
                    poss[i][j][0] = 0
                    ones = 0
                    nums = None
                    for numm in range(10):
                        if(poss[i][j][numm] == 1):
                            ones += 1
                            nums = numm
                            
                    if(ones == 1):
                        fl = 0
                        self.helperArray[i][j] = nums
                        blockRow , blockCol = i//3 * 3 , j //3 * 3
                        for k in range(9):
                            poss[i][k][nums] = 0
                            
                        for k in range(9):
                            poss[k][j][nums] = 0
                            
                        for k in range(blockRow, blockRow + 3):
                            for h in range(blockCol , blockCol + 3):
                                poss[k][h][nums] == 0
                            
                        print("yesss")
                        
                    

    def createPopulation(self, size):#return 3D array
        population=[]
        for i in range(0,size):
            population.insert(i,self.genrate())

        return population

    def genrate(self):
        population=[[],[],[],[],[],[],[],[],[]]
        for i in range(0,3):
            for j in range(0,3):
                numbers={1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9}
                self.checkHelperArray(numbers,i,j)#removes the numbers of the sub array in helper array from numbers
                for k in range(0,3):
                    for kk in range(0,3): 
                        num=random.randint(1,9)
                        while not num in numbers and len(numbers)>0:
                            num=random.randint(1,9)#pick a number that not in the sub array of helper array
                        if self.helperArray[3*i+k][3*j+kk]==0:
                            population[3*i+k].insert(3*j+kk,num)
                            numbers.pop(num)
                        else:
                            num=self.helperArray[3*i+k][3*j+kk]
                            population[3*i+k].insert(3*j+kk,num)
                            
        return State(population)

    def checkHelperArray(self, numbers,i,j):#return valuse in the sub array
        for k in range(0,3):
            for kk in range(0,3):
                if self.helperArray[3*i+k][3*j+kk]!=0:
                    numbers.pop(self.helperArray[3*i+k][3*j+kk])
                
    def cross(self, parent1,parent2):#parent is 9 by 9 grid
        randPoint=random.randint(0,80)//9
        child1=copy.deepcopy(parent1)
        child2=copy.deepcopy(parent2)
        
        # printState(child1)
        # print(type(child1))
        # printState(child2)
        # print()
        for i in range(0,9):
            for j in range(0,9):
                index=(i//3)*3+(j//3)
                if index<randPoint:
                    
                    temp= child1[i][j]
                    child1[i][j]=child2[i][j]
                    child2[i][j]=temp
                    
        return State(child1),State(child2)

    def mutaion(self, child):
        for i in range(0,3):
            for j in range(0,3):
                if(random.random() > self.PM):
                    continue
                rounds = random.randint(1, 2)
                for m in range(rounds):
                
                    numbers={1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9}
                    self.checkHelperArray(numbers,i,j)#removes the numbers of the sub array in helper array from numbers
                    if len(numbers)<2:
                        continue
                    k1=random.randint(0, 2)
                    kk1=random.randint(0,2)
                    while self.helperArray[i*3+k1][j*3+kk1]!=0:
                        k1=random.randint(0,2)
                        kk1=random.randint(0,2)
                        
                    
                    k2=random.randint(0, 2)
                    kk2=random.randint(0,2)
                    while self.helperArray[i*3+k2][j*3+kk2]!=0:
                        k2=random.randint(0,2)
                        kk2=random.randint(0,2)
                        
                    
                    child.swap((i*3+k2, j*3+kk2), (i*3+k1, j*3+kk1))
                
                





    def main(self, queue):
        print("suii")
        # global answerLock
        global bestState

        population = self.createPopulation(self.POPULATION_SIZE)
        cnt = 0
        while cnt < self.ITERATIONS_NUM:
            # with answerLock:
                
            if(population[0].score == 5000):
                queue.put(population[0])
                return
                
                
                
            cnt+=1
            cnt %= self.ITERATIONS_NUM
            if(cnt % 100 == 0):
                print("case:" , cnt)
            if(cnt == 0):
                population = self.createPopulation(self.POPULATION_SIZE)
                
                
                
            sumFitness = 0
            for state in population:
                sumFitness += state.score


            for i in range(self.CHILDREN_NUM):
                par1 = random.randint(0, len(population) -1)
                parent1 = []
                for state in population:
                    if(par1 == 0):
                        parent1 = state.table
                        break
                    else:
                        par1 -= 1
                        
                par2 = random.randint(0, len(population) - 1)
                parent2 = []
                for state in population:
                    if(par2 == 0):
                        parent2 = state.table
                        break
                    else:
                        par2 -= 1
                
                if(parent1 == [] and parent2 == []):
                    print("whaaaaat")
                    
                child1, child2 = self.cross(parent1, parent2)
                self.mutaion(child1)
                self.mutaion(child2)
                
                population.append(child1)
                population.append(child2)
            
            
            
            # for state in population:
            #     if(random.random() < self.PM2):
                    
            #         self.mutaion(state)
                
                
            population.sort(key = lambda x: -x.score)
            if(cnt % 100 == 0):
                print(population[0].score)
            # while(population[0].score == 4996):
                
            #     printState(population[0].table)
            #     print(fitnessfunction3(population[0]))
            #     population[0].fitnessfunction2()
            #     # return population[0]
            # if(population[0].score < 5000):
            #     for i in range(self.POPULATION_SIZE):
            #         if(population[i].score == 4996):
            #             printState(population[i].table)
            #             print(fitnessfunction3(population[i]))
                        # if(population)
                        
                
            
            if(population[0].score == 5000):
                continue
            while(len(population) > self.POPULATION_SIZE):
                population.pop()
        
        
        
# gr = [[4, 5, 1, 2, 3, 7, 8, 9, 6], [2, 7, 6, 1, 8, 9, 3, 4, 5], [3, 8, 9, 5, 6, 4, 1, 2, 7], [5, 1, 2, 3, 7, 8, 9, 6, 4], [6, 3, 8, 9, 4, 2, 5, 7, 1], [7, 9, 4, 6, 1, 5, 2, 3, 8], [8, 4, 5, 7, 9, 3, 6, 1, 2], [9, 6, 7, 8, 2, 1, 4, 5, 3], [1, 2, 3, 4, 5, 6, 7, 8, 9]]
# print(fitnessfunction2(gr))
def solve(helperArray):
    queue = multiprocessing.Queue()
    workers = [ None,None ,None ,None ,None]
    processes = [ None,None ,None ,None ,None]
    for i in range(5):
        print("process", i)
        workers[i] = GA(helperArray)
        processes[i] = multiprocessing.Process(target = workers[i].main , args = (queue,))
        # time.sleep(1)
        processes[i].start()
        
    result = queue.get()
        
    for process in processes:
        if(process.is_alive()):
            process.kill()
    # worker = GA(helperArray)
    # worker.main(queue)
    printState(result.table)
    
    return result.table
        
if __name__ == '__main__':
    # freeze.support()    
    multiprocessing.set_start_method('fork')  
    times = []
    for a in range(1):
        start_time = time.time() * 1000
        # helperArray = generator.generateCase()
        print(helperArray)
        solve(helperArray)
        state = bestState
        
        # printState(state.table)
        end_time = time.time() * 1000
        times.append(end_time- start_time  )
    print(times)
    