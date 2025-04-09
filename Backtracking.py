import generator
import copy


# sudoku_grid = [
#     [1, 4, 0, 0, 0, 0, 0, 0, 6],
#     [0, 0, 0, 0, 2, 0, 0, 0, 0],
#     [3, 0, 0, 1, 0, 7, 9, 0, 0],
#     [0, 0, 0, 0, 5, 0, 8, 0, 0],
#     [2, 0, 0, 0, 9, 0, 0, 0, 0],
#     [0, 3, 0, 8, 0, 2, 0, 4, 0],
#     [7, 0, 0, 3, 0, 8, 1, 0, 0],
#     [0, 0, 1, 0, 0, 0, 0, 9, 0],
#     [0, 0, 0, 5, 0, 0, 0, 0, 0]
# ]
helperArray=[
    [4 ,5 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,7 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,8],
    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    ]


            
def isPossible(sudoku_grid,row,column,number):
    for i in range(0,9):# horizantol 
        if sudoku_grid[i][column]==number:
            return False
    
    for i in range(0,9):
        if sudoku_grid[row][i]==number:
            return False
        
    start=row-(row%3)
    start2=column-(column%3)
    for i in range(0,3):
        for j in range(0,3):
            if sudoku_grid[start+i][start2+j]==number:
                return False
    return True

def solve2(sudoku_grid, stop_event):
    # if(stop_event.is_set()): 
    #     return True
    
    for i in range(0,9):
        for j in range(0,9):
            if sudoku_grid[i][j]==0:
                for k in range(1,10):
                    if isPossible(sudoku_grid,i,j,k):
                        sudoku_grid[i][j]=k
                        if solve2(sudoku_grid, stop_event):
                            return True
                        sudoku_grid[i][j]=0
                return False
    return True

def solve(sudoku_grid, stop_event):
    s=copy.deepcopy(sudoku_grid)
    solve2(s, stop_event)
    return s

def printa(sudoku_grid1):
    for i in range(0,9):
        for j in range(0,9):
            print(sudoku_grid1[i][j],end=" ")
        print()

def check(grid):


    for row in grid:

        dicti = {1: 0 , 2: 0 , 3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9: 0}
        for cell in row:
            if cell==0:
                return False
            dicti[cell] += 1
            if(dicti[cell] == 2):
                return False


    for j in range(0 , 9):
        dicti = {1: 0 , 2: 0 , 3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9: 0}
        for i in range(0 , 9):
            if grid[i][j]==0:
                return False
            dicti[grid[i][j]] += 1
            if(dicti[grid[i][j]] == 2):
                return False

    for k in range(0, 3):
        for h in range(0, 3):

            dicti = {1: 0 , 2: 0 , 3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9: 0}
            for i in range(0 , 3):
                for j in range(0 , 3):
                    cell = grid[3 * k + i][3 * h + j]
                    if cell==0:
                        return False
                    dicti[cell] += 1
                    if(dicti[cell] == 2):
                        return False


    return True



# count=1

# while True: 
#     sudoku_grid=generator.generateCase()
#     s=sudoku_grid
#     print()
#     solve(sudoku_grid)
#     if check(sudoku_grid):
#         print(f"Test number:{count} passed")
#         count+=1   
#     else:
#         printa(s)
#         print()
#         print(sudoku_grid)    
#         break
# solve(helperArray)
# print(helperArray)
