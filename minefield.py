import pygame
import random
import sys
import time
import math  # Add math module for trigonometric functions

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 40
GRID_SIZE = 10
MINES_COUNT = 10
WINDOW_SIZE = CELL_SIZE * GRID_SIZE
BUTTON_HEIGHT = 40

# Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
GRAY = (180, 180, 180)
DARK_GRAY = (140, 140, 140)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Number colors
NUMBER_COLORS = {
    1: BLUE,
    2: GREEN,
    3: RED,
    4: PURPLE,
    5: ORANGE,
    6: CYAN,
    7: MAGENTA,
    8: YELLOW
}

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:
                return True
        return False

class Minesweeper:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + BUTTON_HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.restart_button = Button(WINDOW_SIZE // 2 - 60, WINDOW_SIZE + 5, 120, 30, 
                                   "Restart", LIGHT_GRAY, GRAY)
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.flags = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.game_over = False
        self.won = False
        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < MINES_COUNT:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if self.grid[y][x] != -1:  # -1 represents a mine
                self.grid[y][x] = -1
                mines_placed += 1

    def calculate_numbers(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] != -1:
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            new_x, new_y = x + dx, y + dy
                            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                                if self.grid[new_y][new_x] == -1:
                                    count += 1
                    self.grid[y][x] = count

    def reveal_cell(self, x, y):
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return
        if self.revealed[y][x] or self.flags[y][x]:
            return

        self.revealed[y][x] = True
        if self.grid[y][x] == -1:
            self.game_over = True
            # Reveal all mines when game is over
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if self.grid[i][j] == -1:
                        self.revealed[i][j] = True
            return

        if self.grid[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    self.reveal_cell(x + dx, y + dy)

        # Check win condition
        if all(self.revealed[y][x] or self.grid[y][x] == -1 for y in range(GRID_SIZE) for x in range(GRID_SIZE)):
            self.won = True
            # Reveal all mines when game is won
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if self.grid[i][j] == -1:
                        self.revealed[i][j] = True

    def toggle_flag(self, x, y):
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return
        if not self.revealed[y][x]:
            self.flags[y][x] = not self.flags[y][x]

    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw grid
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                # Draw cell background
                if self.revealed[y][x]:
                    if self.grid[y][x] == -1 and self.game_over:
                        # Draw mine with simple graphics
                        pygame.draw.rect(self.screen, RED, rect)
                        center_x = x * CELL_SIZE + CELL_SIZE // 2
                        center_y = y * CELL_SIZE + CELL_SIZE // 2
                        pygame.draw.circle(self.screen, BLACK, (center_x, center_y), CELL_SIZE // 3)
                    else:
                        pygame.draw.rect(self.screen, LIGHT_GRAY, rect)
                    
                    # Add shadow effect for revealed cells
                    pygame.draw.line(self.screen, DARK_GRAY, 
                                   (x * CELL_SIZE, y * CELL_SIZE),
                                   (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE), 2)
                    pygame.draw.line(self.screen, DARK_GRAY,
                                   (x * CELL_SIZE, y * CELL_SIZE),
                                   (x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 2)
                else:
                    # Draw 3D effect for unrevealed cells
                    pygame.draw.rect(self.screen, GRAY, rect)
                    pygame.draw.line(self.screen, WHITE,
                                   (x * CELL_SIZE, y * CELL_SIZE),
                                   (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE), 2)
                    pygame.draw.line(self.screen, WHITE,
                                   (x * CELL_SIZE, y * CELL_SIZE),
                                   (x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 2)
                    pygame.draw.line(self.screen, DARK_GRAY,
                                   (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE),
                                   (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 2)
                    pygame.draw.line(self.screen, DARK_GRAY,
                                   (x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE),
                                   (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 2)

                # Draw cell content
                if self.revealed[y][x]:
                    if self.grid[y][x] > 0:
                        # Draw number with better styling
                        text = self.font.render(str(self.grid[y][x]), True, NUMBER_COLORS.get(self.grid[y][x], BLACK))
                        text_rect = text.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2,
                                                        y * CELL_SIZE + CELL_SIZE // 2))
                        self.screen.blit(text, text_rect)
                elif self.flags[y][x]:
                    # Draw flag with better graphics
                    flag_points = [
                        (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 4),
                        (x * CELL_SIZE + CELL_SIZE * 3 // 4, y * CELL_SIZE + CELL_SIZE // 2),
                        (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE * 3 // 4)
                    ]
                    pygame.draw.polygon(self.screen, RED, flag_points)
                    # Add flag pole
                    pygame.draw.line(self.screen, BLACK,
                                   (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 4),
                                   (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE * 3 // 4), 2)

        # Draw game status with improved visibility
        if self.game_over:
            # Create a semi-transparent overlay
            overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Draw game over text
            text = self.font.render("OYUN BİTTİ!", True, RED)
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            self.screen.blit(text, text_rect)
        elif self.won:
            # Create a semi-transparent overlay
            overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Draw win text
            text = self.font.render("KAZANDINIZ!", True, GREEN)
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            self.screen.blit(text, text_rect)

        # Draw restart button
        self.restart_button.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[1] < WINDOW_SIZE:  # Click on grid
                        x = event.pos[0] // CELL_SIZE
                        y = event.pos[1] // CELL_SIZE
                        if event.button == 1:  # Left click
                            if not self.game_over and not self.won:
                                self.reveal_cell(x, y)
                        elif event.button == 3:  # Right click
                            if not self.game_over and not self.won:
                                self.toggle_flag(x, y)
                    else:  # Click on button
                        if self.restart_button.handle_event(event):
                            self.reset_game()
                elif event.type == pygame.MOUSEMOTION:
                    if event.pos[1] >= WINDOW_SIZE:
                        self.restart_button.handle_event(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reset game with R key
                        self.reset_game()

            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Minesweeper()
    game.run() 