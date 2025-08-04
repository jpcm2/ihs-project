import pygame
import sys

# Inicializar pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.SysFont("comicsans", 40)
SMALL_FONT = pygame.font.SysFont("comicsans", 20)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (96, 216, 232)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 150, 0)

board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

original_board = [row[:] for row in board]

# Função para desenhar a grade
def draw_grid(win):
    for i in range(GRID_SIZE + 1):
        width = 4 if i % 3 == 0 else 1
        pygame.draw.line(win, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), width)
        pygame.draw.line(win, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), width)

def draw_numbers(win):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] != 0:
                color = BLACK if original_board[i][j] != 0 else GREEN
                text = FONT.render(str(board[i][j]), True, color)
                win.blit(text, (j * CELL_SIZE + 20, i * CELL_SIZE + 15))

def is_valid(num, row, col):
    for i in range(GRID_SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_x, box_y = col // 3, row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num:
                return False
    return True

# Função principal
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    selected = None

    while True:
        win.fill(WHITE)
        draw_grid(win)
        draw_numbers(win)

        # Destacar célula selecionada
        if selected:
            pygame.draw.rect(win, LIGHTBLUE, (selected[1]*CELL_SIZE, selected[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < WIDTH:
                    row, col = y // CELL_SIZE, x // CELL_SIZE
                    selected = (row, col)

            elif event.type == pygame.KEYDOWN and selected:
                row, col = selected
                if original_board[row][col] == 0 and event.unicode.isdigit():
                    num = int(event.unicode)
                    if num != 0 and is_valid(num, row, col):
                        board[row][col] = num
                    elif (num != 0 and is_valid(num, row, col) == False):
                        board[row][col] = num
                    else: 
                        board[row][col] = 0

        pygame.display.update()

if __name__ == "__main__":
    main()
