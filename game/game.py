import pygame
import sys
from board import Board
from settings import *

class Game:
    def __init__(self, board_data, board_backup):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sudoku")
        self.font = pygame.font.SysFont("comicsans", 40)
        self.board_data = board_data  # Guarda o board original
        self.board = Board(board_data)
        self.board_backup = board_backup
        self.selected = (0, 0)
        self.game_over = False
        self.start_time = None

    def run(self):
        while True:
            self.win.fill(WHITE)
            self.board.draw(self.win, self.font, self.game_over)
            self.draw_selection()
            self.handle_events()

            if self.board.is_solved() and not self.game_over:
                self.game_over = True
                self.start_time = pygame.time.get_ticks()  
                self.show_victory_message()

            if self.game_over and pygame.time.get_ticks() - self.start_time > 2000:
                self.reset_game()

            pygame.display.update()

    def draw_selection(self):
        if self.selected and not self.game_over:
            row, col = self.selected
            pygame.draw.rect(self.win, LIGHTBLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < WIDTH:
                    self.selected = (x // CELL_SIZE, y // CELL_SIZE)
            elif event.type == pygame.KEYDOWN:
                if not self.game_over:
                    row, col = self.selected
                    if event.key == pygame.K_LEFT:
                        col = max(col - 1, 0)
                    elif event.key == pygame.K_RIGHT:
                        col = min(col + 1, GRID_SIZE - 1)
                    elif event.key == pygame.K_UP:
                        row = max(row - 1, 0)
                    elif event.key == pygame.K_DOWN:
                        row = min(row + 1, GRID_SIZE - 1)
                    elif event.key == pygame.K_SPACE:
                        current = self.board.board[row][col]
                        self.board.update_cell(row, col, (current + 1) % 10)
                    elif event.unicode.isdigit():
                        num = int(event.unicode)
                        self.board.update_cell(row, col, num)
                    self.selected = (row, col)

    def show_victory_message(self):
        win_text = self.font.render("Você Venceu!", True, GREEN)
        self.win.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
        pygame.display.update()

    def reset_game(self):
        self.board = Board(self.board_backup) 
        self.game_over = False
        self.selected = (0, 0) 
