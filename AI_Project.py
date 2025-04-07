import pygame as pg
from sys import exit
import generator
import Backtracking 
import copy
import GA
pg.init()

difficulty = 35  # Default number of empty squares
min_difficulty = 25  # Minimum number of empty cells (easier)
max_difficulty = 60  # Maximum number of empty cells (harder)

WIDTH,HEIGHT=600,750
CELL_SIZE=WIDTH//9
WHITE = (248, 249, 250)  # Slightly off-white for better eye comfort
BLACK = (33, 37, 41)  # Softer black
BLUE = (13, 110, 253)  # Modern blue
LIGHT_BLUE = (108, 142, 255)  # Lighter blue for hover effects
GREY = (222, 226, 230)  # Lighter grey for empty cells
BOARD_BG = (255, 255, 255)  # Pure white for board background
FILLED_CELL = (233, 236, 239)  # Very light grey for prefilled cells
EMPTY_CELL = (248, 249, 250)  # Almost white for editable cells
TEXT_COLOR = (33, 37, 41)  # Dark text
HIGHLIGHT_COLOR = (233, 236, 239)  # Color for highlighting cells
screen=pg.display.set_mode((WIDTH,HEIGHT))
font = pg.font.SysFont("Arial", 50, bold=True)

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
    # Fill the board background
    pg.draw.rect(screen, BOARD_BG, (0, 0, WIDTH, WIDTH))
    
    # Draw cells with different colors for original vs. editable cells
    for row in range(9):
        for col in range(9):
            if OG_grid[row][col] == 0:
                pg.draw.rect(screen, EMPTY_CELL, ((col * CELL_SIZE, row * CELL_SIZE), (CELL_SIZE, CELL_SIZE)))
            else:
                pg.draw.rect(screen, FILLED_CELL, ((col * CELL_SIZE, row * CELL_SIZE), (CELL_SIZE, CELL_SIZE)))
                
    # Draw grid lines
    for i in range(0, 10):
        if i % 3 == 0: 
            thickness = 4
        else:
            thickness = 1
        pg.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)  # Horizontal lines 
        pg.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), thickness)  # Vertical lines
    
    pg.display.update()
 
def draw_numbers(mode=0):
    """
    Update only the cells that were originally empty.
    The fixed cells (from OG_grid) remain unchanged.
    """
    # Loop over the board and update only dynamic cells
    for row in range(9):
        for col in range(9):
            if OG_grid[row][col] == 0:
                # Clear the cell first
                pg.draw.rect(screen, EMPTY_CELL, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                # Draw the new number if one is present
                if sudoku_grid[row][col] != 0:
                    text = pg.font.Font(None, 48).render(str(sudoku_grid[row][col]), True, BLUE)
                    text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE//2,
                                                      row * CELL_SIZE + CELL_SIZE//2))
                    screen.blit(text, text_rect)
                if mode == 1:
                    pg.display.update()
                    frameRate.tick(30)
    # Redraw grid lines (so they appear over updated cells)
    for i in range(0, 10):
        thickness = 4 if i % 3 == 0 else 1
        pg.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)
        pg.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), thickness)
    pg.display.update()



def draw_difficulty_slider():
    # Clear the slider area in the UI panel (clear only the left side where the slider is)
    pg.draw.rect(screen, WHITE, (30, 680, 256, 40))
    
    # Draw difficulty slider background in the new area
    slider_rect = pg.Rect(30, 670, 256, 20)
    pg.draw.rect(screen, GREY, slider_rect, border_radius=10)
    pos = 30 + int((difficulty - min_difficulty) * 256 / (max_difficulty - min_difficulty))
    pg.draw.circle(screen, BLUE, (pos, 680), 10)
    
    # Draw labels
    small_font = pg.font.SysFont("Arial", 24, bold=True)
    text_easy = small_font.render("Easy", True, BLACK)
    text_hard = small_font.render("Hard", True, BLACK)
    text_level = small_font.render(f"Empty cells: {difficulty}", True, BLACK)
    
    screen.blit(text_easy, (20, 705))
    screen.blit(text_hard, (275, 705))
    screen.blit(text_level, (90, 690))

def draw_fixed_numbers():
    # Draw the given (fixed) numbers from the original grid (OG_grid)
    for row in range(9):
        for col in range(9):
            if OG_grid[row][col] != 0:
                text = pg.font.Font(None, 50).render(str(sudoku_grid[row][col]), True, BLACK)
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE//2,
                                                  row * CELL_SIZE + CELL_SIZE//2))
                screen.blit(text, text_rect)
    pg.display.update()

# def update_cell(row, col):
#     """Update only one cell if it was originally empty."""
#     if OG_grid[row][col] == 0:
#         cell_rect = (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
#         pg.draw.rect(screen, EMPTY_CELL, cell_rect)
#         if sudoku_grid[row][col] != 0:
#             text = pg.font.Font(None, 48).render(str(sudoku_grid[row][col]), True, BLUE)
#             text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE//2,
#                                               row * CELL_SIZE + CELL_SIZE//2))
#             screen.blit(text, text_rect)
#         pg.display.update(cell_rect)


            


def main():
    global sudoku_grid
    global OG_grid
    global difficulty
    
    # Create a more sophisticated UI with rounded buttons
    generate_button = pg.Rect(30, 610, 256, 40)
    solve_bt_button = pg.Rect(320, 610, 250, 40)
    solve_ga_button = pg.Rect(320, 660, 250, 40)

    
    # Initialize fonts
    button_font = pg.font.Font(None, 32)
    small_font = pg.font.Font(None, 24)
    
    # Button labels
    text1 = button_font.render("Generate New Puzzle", True, WHITE)
    text2 = button_font.render("Solve with BT", True, WHITE)
    text3 = button_font.render("Solve with GA", True, WHITE)
    
    # Initially generate a puzzle
    OG_grid = generator.generateCase()
    sudoku_grid = copy.deepcopy(OG_grid)
    screen.fill(WHITE)
    drawBoard()
    draw_numbers()
    
    # Main game loop
    slider_active = False
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            
            # Handle mouse events    
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
    
            # Check if clicked on slider (new coordinates in the UI panel)
                slider_rect = pg.Rect(30, 670, 256, 20)
                if slider_rect.collidepoint(mouse_pos):
                    slider_active = True
                
                # Check other button clicks
                if generate_button.collidepoint(mouse_pos):
                    # Clear only the board area (top 600 pixels)
                    pg.draw.rect(screen, BOARD_BG, (0, 0, WIDTH, 600))
                    # Generate a new puzzle based on the chosen difficulty
                    OG_grid = generator.sudokuGenerator(difficulty)
                    sudoku_grid = copy.deepcopy(OG_grid)
                    drawBoard()           # Draw the board background and grid lines
                    draw_fixed_numbers()  # Draw the fixed (given) numbers

                
                elif solve_bt_button.collidepoint(mouse_pos):
                    Backtracking.solve(sudoku_grid)
                    drawBoard()           # Redraw the board background and grid lines
                    draw_fixed_numbers()  # Redraw the fixed (given) numbers
                    draw_numbers()        # Redraw all the numbers (which now includes the solved cells)
                                
                elif solve_ga_button.collidepoint(mouse_pos):
                    sudoku_grid = GA.solve(sudoku_grid)
                    drawBoard()           # Redraw the board background and grid lines
                    draw_fixed_numbers()  # Redraw the fixed numbers
                    draw_numbers()        # Redraw all numbers


            
            # Handle mouse movement for slider
            elif event.type == pg.MOUSEMOTION:
                if slider_active:
                    mouse_x = pg.mouse.get_pos()[0]
                    # Calculate difficulty based on slider position
                    if 30 <= mouse_x <= 286:
                        difficulty = min_difficulty + int((mouse_x - 30) * (max_difficulty - min_difficulty) / 256)
            
            # Handle mouse button release
            elif event.type == pg.MOUSEBUTTONUP:
                slider_active = False
        
        # Draw UI elements
        mouse_pos = pg.mouse.get_pos()
        
        # Button hover effects
        if generate_button.collidepoint(mouse_pos):
            button_color1 = LIGHT_BLUE
        else:
            button_color1 = BLUE
            
        if solve_bt_button.collidepoint(mouse_pos):
            button_color2 = LIGHT_BLUE
        else:
            button_color2 = BLUE
            
        if solve_ga_button.collidepoint(mouse_pos):
            button_color3 = LIGHT_BLUE
        else:
            button_color3 = BLUE
        
        # Draw buttons with rounded corners
        pg.draw.rect(screen, button_color1, generate_button, border_radius=10)
        pg.draw.rect(screen, button_color2, solve_bt_button, border_radius=10)
        pg.draw.rect(screen, button_color3, solve_ga_button, border_radius=10)
        
        # Position text in center of buttons
        text_rect1 = text1.get_rect(center=generate_button.center)
        text_rect2 = text2.get_rect(center=solve_bt_button.center)
        text_rect3 = text3.get_rect(center=solve_ga_button.center)
        
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(text3, text_rect3)
        
        # Draw the difficulty slider
        draw_difficulty_slider()
        
        pg.display.update()

if __name__=="__main__":
    
    main()

    
