import pygame as pg
from sys import exit
import generator
import Backtracking 
import copy
import GA
pg.init()

WIDTH,HEIGHT=506,600
CELL_SIZE=WIDTH//9
WHITE=(255,255,255)
BLACK=(0,0,0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
GREY = (169, 169, 169)
screen=pg.display.set_mode((WIDTH,HEIGHT))
font=pg.font.Font(None,50)

pg.display.set_caption("Sudoku")
screen.fill
frameRate=pg.time.Clock()


OG_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
sudoku_grid = [
    [0, 0, 0, 0, 1, 9, 2, 5, 6],
    [0, 0, 1, 7, 0, 0, 0, 0, 9],
    [0, 0, 0, 0, 5, 4, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 9, 1, 0],
    [0, 0, 0, 0, 0, 0, 4, 0, 7],
    [1, 0, 0, 0, 4, 0, 6, 8, 3],
    [0, 8, 5, 0, 0, 0, 1, 0, 2],
    [0, 3, 0, 0, 0, 6, 0, 0, 0],
    [2, 0, 9, 0, 0, 3, 7, 0, 0]
]
def drawBoard():
    
    for row in range(9):
        for col in range(9):
            if OG_grid[row][col] == 0:
                pg.draw.rect(screen, GREY, ((col * CELL_SIZE, row * CELL_SIZE), (CELL_SIZE ,  CELL_SIZE )))
                
                
    for i in range(0,10):
        if i % 3 == 0: 
            thickness = 4
        else:
            thickness = 1
        pg.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)  # Horizontal lines 
        pg.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), thickness)  # Vertical lines
        
                
            
    
    pg.display.update()
 
def draw_numbers(mode=0):
    
    """Draws the numbers on the Sudoku board"""
    #screen.fill(WHITE)
    
    drawBoard()
    
            
            
            
    for row in range(9):
        for col in range(9):
            if sudoku_grid[row][col] != 0:
                text = font.render(str(sudoku_grid[row][col]), True, BLACK)
                screen.blit(text, (col * CELL_SIZE + 18, row * CELL_SIZE + 15))  # Positioning text
                pg.display.update()
        if(mode==1):
            frameRate.tick(7)#change how fast the number appear
        else:
            frameRate.tick(90)
            
    
            
            
    
    
   


def main():
    global sudoku_grid
    global OG_grid
    
    genrate_button = pg.Rect(30, 515, 256, 40)
    button_color = BLUE
    font = pg.font.Font(None, 36)
    text1 = font.render("Generate new puzzle", True, WHITE)
    text_rect1 = text1.get_rect(center=genrate_button.center)

    solve_button = pg.Rect(300, 515, 184, 40)
    button_color2 = BLUE
    font = pg.font.Font(None, 36)
    text2 = font.render("Solve using BT", True, WHITE)
    text_rect2 = text2.get_rect(center=solve_button.center)

    solveGA_button = pg.Rect(300, 556, 184, 40)
    button_color3 = BLUE
    font = pg.font.Font(None, 36)
    text3 = font.render("Solve using GA", True, WHITE)
    text_rect3 = text3.get_rect(center=solveGA_button.center)


    OG_grid = generator.generateCase()
    sudoku_grid = copy.deepcopy(OG_grid)
    screen.fill(WHITE)
    drawBoard()
    draw_numbers()         
    while True:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                exit()
            mouse_pos = pg.mouse.get_pos()
            mouse_click = pg.mouse.get_pressed()

            if genrate_button.collidepoint(mouse_pos):
                button_color = LIGHT_BLUE
                if mouse_click[0]:  # Left mouse button clicked
                    screen.fill(WHITE)
                    OG_grid=generator.generateCase()
                    sudoku_grid = copy.deepcopy(OG_grid)
                    draw_numbers()
            else:
                button_color = BLUE

            if solve_button.collidepoint(mouse_pos):
                button_color2 = LIGHT_BLUE
                if mouse_click[0]:  # Left mouse button clicked
                    Backtracking.solve(sudoku_grid)
                    draw_numbers(1)
            else:
                button_color2 = BLUE

            if solveGA_button.collidepoint(mouse_pos):
                button_color3 = LIGHT_BLUE
                if mouse_click[0]:  # Left mouse button clicked
                    sudoku_grid = GA.solve(sudoku_grid)
                    draw_numbers(1)
                    # print("GA")
            else:
                button_color3 = BLUE
            
            pg.draw.rect(screen, button_color, genrate_button, border_radius=10)
            pg.draw.rect(screen, button_color2, solve_button, border_radius=10)
            pg.draw.rect(screen, button_color3, solveGA_button, border_radius=10)
            screen.blit(text1, text_rect1)
            screen.blit(text2, text_rect2)
            screen.blit(text3, text_rect3)

            
            
            pg.display.update()

if __name__=="__main__":
    
    main()

    
