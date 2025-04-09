import random
import math
import copy
import generator
import time
import multiprocessing
from State import State
from State import HELPER_PENALTY
import numpy as np
helperArray = [
[0 ,5 ,0 ,6 ,0 ,0 ,8 ,0 ,9 ,],
[8 ,7 ,9 ,0 ,4 ,0 ,2 ,6 ,0 ,],
[6 ,2 ,0 ,0 ,0 ,0 ,4 ,0 ,0 ,],
[0 ,0 ,0 ,1 ,0 ,6 ,0 ,0 ,8 ,],
[0 ,4 ,5 ,2 ,0 ,0 ,6 ,1 ,3 ,],
[1 ,0 ,0 ,4 ,9 ,0 ,0 ,0 ,2 ,],
[4 ,0 ,3 ,8 ,0 ,1 ,0 ,0 ,7 ,],
[0 ,0 ,8 ,7 ,0 ,0 ,0 ,0 ,6 ,],
[0 ,1 ,0 ,0 ,6 ,0 ,3 ,0 ,4 ,],
]
# bestState = State( [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#                 ])
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
        

    

        

def fitnessfunction2(sudoku, helperArray)-> int:# try to minimize(max is 5000000)
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
    return 5000000-fitness


def addInference():
        
    poss = np.ones((9, 9, 10))
    for i in range(9):
        for j in range(9):
            if(helperArray[i][j] != 0):
                numm = helperArray[i][j]
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
                if(helperArray[i][j] != 0):
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
                    helperArray[i][j] = nums
                    blockRow , blockCol = i//3 * 3 , j //3 * 3
                    for k in range(9):
                        poss[i][k][nums] = 0
                        
                    for k in range(9):
                        poss[k][j][nums] = 0
                        
                    for k in range(blockRow, blockRow + 3):
                        for h in range(blockCol , blockCol + 3):
                            poss[k][h][nums] == 0
                        
                    print("yesss")       
                
        
        




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
        printState(self.helperArray)
        


    
        
    
                        
                    

    def createPopulation(self, size):#return 3D array
        population=[]
        for i in range(0,size):
            for _ in range(5):
                state = self.genrate()
                fl = True
                for st in population:
                    if(state.table == st.table):
                        fl = False
                if(fl):
                    population.append(self.genrate())
                    break
            

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
                            
        return State(population, self.helperArray)

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
                    
        return State(child1, self.helperArray),State(child2, self.helperArray)

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
        # global bestState

        population = self.createPopulation(self.POPULATION_SIZE)
        cnt = 0
        while cnt < self.ITERATIONS_NUM:
            # with answerLock:
                
            if(population[0].score == 5000000):
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
            newPopulation = []
            newPopulation.append(population[0])
            for i in range(1, len(population)):
                if(self.POPULATION_SIZE > len(newPopulation) and population[i].table != population[i - 1].table):
                    newPopulation.append(population[i])
                    
            
            if(cnt % 100 == 0):
                print(population[0].score)
                        
                
            
            if(population[0].score == 5000000):
                continue
            while(len(population) > self.POPULATION_SIZE):
                population.pop()
        
        
        
def solve(helperArray):
    addInference()
    queue = multiprocessing.Queue()
    workers = [ None,None ,None ,None ,None]
    processes = [ None,None ,None ,None ,None]
    for i in range(5):
        print("process", i)
        workers[i] = GA(helperArray)
        processes[i] = multiprocessing.Process(target = workers[i].main , args = (queue,))
        processes[i].start()
        
    result = queue.get()
        
    for process in processes:
        if(process.is_alive()):
            process.kill()
    # worker = GA(helperArray)
    # worker.main(queue)
    print("donneeeee")
    printState(result.table)
    
    return result.table
        
if __name__ == '__main__':
    # multiprocessing.set_start_method('fork')  
    # times = { 0 : [] , 1 : [] , 2 : [] , 5 : [] ,  10 : [] , 20 : [] , 50 : [] , 100 : [] , 200 : [] , 500 : [] , 1000 : [] , 2000 : [] , 5000 : [] , 10000 : [] }
    
    # for a in range(10):
    #     helperArray = generator.generateCase()
    #     # print(helperArray)
    #     for i in times.keys():
    #         HELPER_PENALTY = i
    #         start_time = time.time() * 1000
    #         solve(helperArray)
    #         end_time = time.time() * 1000
    #         times[i].append(end_time - start_time )
        
    # print(times)
    
    
    # dic = {0: [2308.17724609375, 56527.837158203125, 2403.629150390625, 4954.816162109375, 18825.4140625, 21059.80029296875, 12290.183837890625, 11012.198974609375, 2709.3740234375, 8836.240234375], 1: [4070.352783203125, 104688.58813476562, 818.410888671875, 2778.85693359375, 10653.094970703125, 25616.30615234375, 6722.42724609375, 6636.906005859375, 4299.02001953125, 22899.317138671875], 2: [2348.552978515625, 2332252.2270507812, 1626.9931640625, 9057.97216796875, 127913.037109375, 11322.080078125, 4798.47509765625, 5956.441162109375, 3534.380126953125, 1287.19384765625], 5: [12448.682861328125, 10312526.926269531, 1509.414794921875, 5194.76513671875, 55818.3203125, 122567.29223632812, 7612.22412109375, 11604.18798828125, 7185.48583984375, 12509.28271484375], 10: [9448.43603515625, 2587203.697265625, 1158.903076171875, 7051.48193359375, 90285.29418945312, 927019.1137695312, 3553.691162109375, 1900.386962890625, 3908.659912109375, 4677.425048828125], 20: [7383.80908203125, 3658635.1450195312, 2386.421875, 4844.715087890625, 79718.541015625, 1861756.1838378906, 16283.579833984375, 14584.126220703125, 4551.9033203125, 17398.586181640625], 50: [2921.83837890625, 14088678.947021484, 814.022216796875, 12713.60400390625, 80277.72705078125, 910221.705078125, 5601.676025390625, 7036.701904296875, 5178.279052734375, 12657.105712890625], 100: [5136.213134765625, 12363048.974121094, 1793.805908203125, 19039.599853515625, 27017.244873046875, 5780.024169921875, 74993.81591796875, 22676.42724609375, 16744.13720703125, 5975.895751953125], 200: [14232.941162109375, 2683910.9770507812, 439.446533203125, 4182.6220703125, 93305.486328125, 77979.35107421875, 5050.69482421875, 6542.68017578125, 5110.314208984375, 43400.930908203125], 500: [9503.1552734375, 17725.1787109375, 1474.2939453125, 12761.14111328125, 93740.77685546875, 291225.630859375, 9732.51806640625, 23934.043212890625, 2533.199951171875, 59612.155029296875], 1000: [6548.18115234375, 52776.583984375, 875.83984375, 10467.848876953125, 45885.476318359375, 78756.92919921875, 3763.126708984375, 3171.383056640625, 961.4189453125, 9041.810302734375], 2000: [73142.06616210938, 5509.60791015625, 2801.950927734375, 8835.79296875, 81112.57397460938, 30833.802978515625, 46132.319091796875, 5794.973876953125, 2959.909912109375, 4226.156982421875], 5000: [11025.09912109375, 66048.9521484375, 2136.259033203125, 11724.281005859375, 88781.716796875, 5159.76416015625, 19514.751953125, 7277.48095703125, 4234.10400390625, 8404.169189453125], 10000: [4937.683837890625, 231014.28393554688, 2523.010009765625, 9376.212158203125, 57854.2421875, 45026.1650390625, 4165.18115234375, 70583.69091796875, 4143.826904296875, 51408.069091796875]}
    # for i,j in dic.items():
    #     print(i , end = ' ')
    #     n = len(j)
    #     sum = 0
    #     for k in j:
    #         sum += k 
    #     sum /= n
    #     print(sum)