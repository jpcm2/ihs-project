import pygame
from settings import *
import copy

class Board:
    def __init__(self, board_data):
        self.board = board_data
        self.original = copy.deepcopy(board_data)
        self.wrong_cells = set()

    def draw(self, win, font, game_over=False):
        for i in range(GRID_SIZE + 1):
            width = 4 if i % 3 == 0 else 1
            pygame.draw.line(win, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), width)
            pygame.draw.line(win, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), width)

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                num = self.board[i][j]
                if num != 0:
                    if self.original[i][j] != 0:
                        color = GREY
                    elif game_over and self.is_valid(num, i, j):
                        color = GREEN
                    elif (i, j) in self.wrong_cells:
                        color = RED
                    else:
                        color = GREEN

                    text = font.render(str(num), True, color)
                    win.blit(text, (j * CELL_SIZE + 20, i * CELL_SIZE + 15))

    def is_valid(self, num, row, col):
        for i in range(GRID_SIZE):
            if self.board[row][i] == num and i != col:
                return False
            if self.board[i][col] == num and i != row:
                return False
        box_x, box_y = col // 3, row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != (row, col):
                    return False
        return True

    def update_cell(self, row, col, value):
        if self.original[row][col] != 0:
            return
        self.board[row][col] = value
        if value == 0:
            self.wrong_cells.discard((row, col))
        elif self.is_valid(value, row, col):
            self.wrong_cells.discard((row, col))
        else:
            self.wrong_cells.add((row, col))

    def is_solved(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == 0 or not self.is_valid(self.board[i][j], i, j):
                    return False
        return True
