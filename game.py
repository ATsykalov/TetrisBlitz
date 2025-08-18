import pygame
import random
import time
from pieces import TetrisPiece, TETRIS_SHAPES

class TetrisGame:
    def __init__(self, screen, username, auth_manager):
        self.screen = screen
        self.username = username
        self.auth_manager = auth_manager
        
        # Game dimensions
        self.GRID_WIDTH = 10
        self.GRID_HEIGHT = 20
        self.CELL_SIZE = 25
        self.GRID_X = 300
        self.GRID_Y = 50
        
        # Modern Classic Color Palette
        self.BACKGROUND_COLOR = (224, 224, 224)  # Светло-серый фон
        self.GAME_FIELD_COLOR = (208, 208, 208)  # Игровое поле
        self.GRID_LINE_COLOR = (192, 192, 192)   # Линии сетки
        self.TEXT_COLOR = (51, 51, 51)           # Основной текст
        self.WHITE = (255, 255, 255)
        self.LIGHT_GRAY = (200, 200, 200)
        
        # Game state
        self.grid = [[0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds
        self.paused = False
        self.game_over = False
        
        # Initialize pieces
        self.spawn_new_piece()
        self.next_piece = TetrisPiece()
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        
        # Last update time
        self.last_time = time.time() * 1000

    def spawn_new_piece(self):
        """Spawn a new piece at the top of the grid"""
        if self.next_piece:
            self.current_piece = self.next_piece
        else:
            self.current_piece = TetrisPiece()
        
        self.current_piece.x = self.GRID_WIDTH // 2 - 1
        self.current_piece.y = 0
        
        # Check for game over
        if self.check_collision(self.current_piece.x, self.current_piece.y, self.current_piece.coords):
            self.game_over = True
        
        self.next_piece = TetrisPiece()

    def check_collision(self, x, y, coords):
        """Check if a piece collides with the grid or boundaries"""
        for dx, dy in coords:
            nx, ny = x + dx, y + dy
            if (nx < 0 or nx >= self.GRID_WIDTH or 
                ny >= self.GRID_HEIGHT or 
                (ny >= 0 and self.grid[ny][nx])):
                return True
        return False

    def place_piece(self):
        """Place the current piece on the grid"""
        if not self.current_piece:
            return
        for dx, dy in self.current_piece.coords:
            nx, ny = self.current_piece.x + dx, self.current_piece.y + dy
            if 0 <= ny < self.GRID_HEIGHT and 0 <= nx < self.GRID_WIDTH:
                self.grid[ny][nx] = self.current_piece.color

    def clear_lines(self):
        """Clear completed lines and return number of lines cleared"""
        lines_to_clear = []
        
        for y in range(self.GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)
        
        # Remove cleared lines
        for y in reversed(lines_to_clear):
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(self.GRID_WIDTH)])
        
        # Update score
        lines_cleared = len(lines_to_clear)
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            
            # Scoring system
            score_values = {1: 1, 2: 3, 3: 5, 4: 8}
            self.score += score_values.get(lines_cleared, 0)
            
            # Level progression every 500 points
            new_level = (self.score // 500) + 1
            if new_level > self.level:
                self.level = new_level
                self.fall_speed = max(50, 500 - (self.level - 1) * 50)
        
        return lines_cleared

    def handle_input(self, event):
        """Handle keyboard input"""
        if self.game_over:
            return
        
        if event.type == pygame.KEYDOWN:
            # Pause can be toggled even when paused
            if event.key == pygame.K_p:
                self.paused = not self.paused
                return
            
            # Other controls only work when not paused
            if self.paused:
                return
                
            if event.key == pygame.K_LEFT:
                self.move_piece(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.move_piece(1, 0)
            elif event.key == pygame.K_DOWN:
                self.move_piece(0, 1)
            elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                self.rotate_piece()
            elif event.key == pygame.K_c:
                self.hard_drop()

    def move_piece(self, dx, dy):
        """Move the current piece"""
        if not self.current_piece:
            return False
        new_x = self.current_piece.x + dx
        new_y = self.current_piece.y + dy
        
        if not self.check_collision(new_x, new_y, self.current_piece.coords):
            self.current_piece.x = new_x
            self.current_piece.y = new_y
            return True
        return False

    def rotate_piece(self):
        """Rotate the current piece"""
        if not self.current_piece:
            return
        rotated_coords = self.current_piece.get_rotated_coords()
        
        # Try rotation at current position
        if not self.check_collision(self.current_piece.x, self.current_piece.y, rotated_coords):
            self.current_piece.coords = rotated_coords
            return
        
        # Try wall kicks
        kicks = [(1, 0), (-1, 0), (0, -1), (2, 0), (-2, 0)]
        for dx, dy in kicks:
            if not self.check_collision(self.current_piece.x + dx, self.current_piece.y + dy, rotated_coords):
                self.current_piece.x += dx
                self.current_piece.y += dy
                self.current_piece.coords = rotated_coords
                return

    def hard_drop(self):
        """Drop piece to the bottom instantly"""
        while self.move_piece(0, 1):
            pass
        self.place_piece()
        self.clear_lines()
        self.spawn_new_piece()

    def update(self):
        """Update game state"""
        if self.game_over:
            return False
        
        if self.paused:
            return True
        
        current_time = time.time() * 1000
        self.fall_time += current_time - self.last_time
        self.last_time = current_time
        
        # Natural piece falling
        if self.fall_time >= self.fall_speed:
            if not self.move_piece(0, 1):
                self.place_piece()
                self.clear_lines()
                self.spawn_new_piece()
            self.fall_time = 0
        
        return True

    def draw(self):
        """Draw the game"""
        # Fill background with light gray
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # Draw grid background
        grid_rect = pygame.Rect(self.GRID_X, self.GRID_Y, 
                               self.GRID_WIDTH * self.CELL_SIZE, 
                               self.GRID_HEIGHT * self.CELL_SIZE)
        pygame.draw.rect(self.screen, self.GAME_FIELD_COLOR, grid_rect)
        
        # Draw grid lines (subtle)
        for x in range(self.GRID_WIDTH + 1):
            pygame.draw.line(self.screen, self.GRID_LINE_COLOR,
                           (self.GRID_X + x * self.CELL_SIZE, self.GRID_Y),
                           (self.GRID_X + x * self.CELL_SIZE, self.GRID_Y + self.GRID_HEIGHT * self.CELL_SIZE), 1)
        
        for y in range(self.GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, self.GRID_LINE_COLOR,
                           (self.GRID_X, self.GRID_Y + y * self.CELL_SIZE),
                           (self.GRID_X + self.GRID_WIDTH * self.CELL_SIZE, self.GRID_Y + y * self.CELL_SIZE), 1)
        
        # Draw placed pieces with modern flat style
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                if self.grid[y][x]:
                    # Main block
                    rect = pygame.Rect(self.GRID_X + x * self.CELL_SIZE + 1,
                                     self.GRID_Y + y * self.CELL_SIZE + 1,
                                     self.CELL_SIZE - 2, self.CELL_SIZE - 2)
                    pygame.draw.rect(self.screen, self.grid[y][x], rect)
                    
                    # Subtle border for definition
                    border_color = tuple(max(0, c - 30) for c in self.grid[y][x])
                    pygame.draw.rect(self.screen, border_color, rect, 1)
        
        # Draw current piece with modern flat style
        if self.current_piece:
            for dx, dy in self.current_piece.coords:
                px = self.current_piece.x + dx
                py = self.current_piece.y + dy
                if 0 <= px < self.GRID_WIDTH and py >= 0:  # Only draw visible parts
                    x = self.GRID_X + px * self.CELL_SIZE + 1
                    y = self.GRID_Y + py * self.CELL_SIZE + 1
                    rect = pygame.Rect(x, y, self.CELL_SIZE - 2, self.CELL_SIZE - 2)
                    
                    # Main block
                    pygame.draw.rect(self.screen, self.current_piece.color, rect)
                    
                    # Subtle border for definition  
                    border_color = tuple(max(0, c - 30) for c in self.current_piece.color)
                    pygame.draw.rect(self.screen, border_color, rect, 1)
        
        # Draw UI
        self.draw_ui()
        
        if self.paused:
            self.draw_pause_overlay()

    def draw_ui(self):
        """Draw user interface elements"""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, self.TEXT_COLOR)
        self.screen.blit(score_text, (50, 100))
        
        # Level
        level_text = self.font.render(f"Level: {self.level}", True, self.TEXT_COLOR)
        self.screen.blit(level_text, (50, 130))
        
        # Lines
        lines_text = self.font.render(f"Lines: {self.lines_cleared}", True, self.TEXT_COLOR)
        self.screen.blit(lines_text, (50, 160))
        
        # Username
        user_text = self.font.render(f"Player: {self.username}", True, self.TEXT_COLOR)
        self.screen.blit(user_text, (50, 50))
        
        # Next piece
        next_text = self.font.render("Next:", True, self.TEXT_COLOR)
        self.screen.blit(next_text, (600, 100))
        
        if self.next_piece:
            self.draw_next_piece()
        
        # Controls
        controls = [
            "Controls:",
            "←→ Move",
            "↓ Soft Drop",
            "↑/Space Rotate",
            "C Hard Drop",
            "P Pause",
            "ESC Menu"
        ]
        
        for i, text in enumerate(controls):
            color = self.TEXT_COLOR if i == 0 else self.LIGHT_GRAY
            control_text = self.font.render(text, True, color)
            self.screen.blit(control_text, (50, 250 + i * 25))

    def draw_next_piece(self):
        """Draw the next piece preview with modern styling"""
        if not self.next_piece:
            return
        
        # Draw preview box background
        preview_box = pygame.Rect(580, 115, 100, 80)
        pygame.draw.rect(self.screen, self.WHITE, preview_box)
        pygame.draw.rect(self.screen, self.LIGHT_GRAY, preview_box, 1)
        
        start_x = 600
        start_y = 130
        
        for dx, dy in self.next_piece.coords:
            x = start_x + (dx + 2) * 18  # Slightly smaller preview blocks
            y = start_y + (dy + 2) * 18
            rect = pygame.Rect(x, y, 16, 16)
            
            # Main block
            pygame.draw.rect(self.screen, self.next_piece.color, rect)
            
            # Subtle border
            border_color = tuple(max(0, c - 30) for c in self.next_piece.color)
            pygame.draw.rect(self.screen, border_color, rect, 1)

    def draw_pause_overlay(self):
        """Draw pause overlay"""
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill(self.BACKGROUND_COLOR)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.big_font.render("PAUSED", True, self.TEXT_COLOR)
        text_rect = pause_text.get_rect(center=(400, 300))
        self.screen.blit(pause_text, text_rect)
        
        resume_text = self.font.render("Press P to resume or ESC for menu", True, self.TEXT_COLOR)
        resume_rect = resume_text.get_rect(center=(400, 350))
        self.screen.blit(resume_text, resume_rect)
