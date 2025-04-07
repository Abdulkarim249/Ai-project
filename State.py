import math
import copy
import time

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

class State:
    def __init__(self, table):
        self.rowCount = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                         ]
        
        self.colCount = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                         ]
        
        self.table = []
        self.setTable(table)
        
        
    def setTable(self, table):
        self.table = copy.deepcopy(table)
        for i in range(9):
            for j in range(9):
                # print(i)
                # print(self.table[i][j])
                self.rowCount[i][self.table[i][j]] +=1
                self.colCount[j][self.table[i][j]] +=1
                
        self.score = fitnessfunction2(self.table)
        
        
    def swap(self, pos1 , pos2):
        i1,j1 = pos1
        i2,j2 = pos2
        if( self.rowCount[i2][self.table[i1][j1]] >= 2 or  self.colCount[j2][self.table[i1][j1]] >= 2 or self.rowCount[i1][self.table[i2][j2]] >= 2 or self.colCount[j1][self.table[i2][j2]] >= 2 ):
            return
        self.rowCount[i1][self.table[i1][j1]] -= 1
        self.colCount[j1][self.table[i1][j1]] -= 1
        
        self.rowCount[i2][self.table[i2][j2]] -= 1
        self.colCount[j2][self.table[i2][j2]] -= 1
        
        
        self.rowCount[i2][self.table[i1][j1]] += 1
        self.colCount[j2][self.table[i1][j1]] += 1
        
        self.rowCount[i1][self.table[i2][j2]] += 1
        self.colCount[j1][self.table[i2][j2]] += 1
        
        
        swap(pos1, pos2, self.table)
        self.score = fitnessfunction2(self.table)
        