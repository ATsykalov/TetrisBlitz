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
        
        # Animation system
        self.animation_time = 0
        self.piece_pos_x = 0.0  # Smooth floating position
        self.piece_pos_y = 0.0
        self.target_pos_x = 0.0
        self.target_pos_y = 0.0
        self.move_animation_speed = 8.0  # Animation speed multiplier
        
        # Line clearing animation
        self.clearing_lines = []
        self.line_clear_animation_time = 0
        self.line_clear_flash_time = 0
        
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
        
        # Initialize smooth animation positions
        self.piece_pos_x = float(self.current_piece.x)
        self.piece_pos_y = float(self.current_piece.y)
        self.target_pos_x = float(self.current_piece.x)
        self.target_pos_y = float(self.current_piece.y)
        
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

    def check_lines_to_clear(self):
        """Check for completed lines and return them"""
        lines_to_clear = []
        
        # Find completed lines
        for y in range(self.GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)
        
        return lines_to_clear
    
    def start_line_clear_animation(self, lines_to_clear):
        """Start the line clearing animation"""
        self.clearing_lines = lines_to_clear
        self.line_clear_animation_time = 0
        self.line_clear_flash_time = 0
        
        # Update score immediately
        lines_cleared = len(lines_to_clear)
        self.lines_cleared += lines_cleared
        
        # Scoring system: 1 line = 1 point, 2 lines = 4 points, 3 lines = 9 points, 4 lines = 16 points
        points = lines_cleared ** 2
        self.score += points
        
        # Level up every 500 points
        new_level = (self.score // 500) + 1
        if new_level > self.level:
            self.level = new_level
            # Increase fall speed with level (max speed cap)
            self.fall_speed = max(50, 500 - (self.level - 1) * 30)
    
    def finish_line_clear(self):
        """Complete the line clearing process"""
        # Remove completed lines
        for y in sorted(self.clearing_lines, reverse=True):
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(self.GRID_WIDTH)])
        
        # Reset animation state and spawn new piece
        self.clearing_lines = []
        self.line_clear_animation_time = 0
        self.line_clear_flash_time = 0
        self.spawn_new_piece()
    
    def clear_lines(self):
        """Legacy function for immediate line clearing (kept for compatibility)"""
        lines_to_clear = self.check_lines_to_clear()
        if lines_to_clear:
            self.start_line_clear_animation(lines_to_clear)
            self.finish_line_clear()

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
        """Move the current piece with smooth animation"""
        if not self.current_piece:
            return False
        new_x = self.current_piece.x + dx
        new_y = self.current_piece.y + dy
        
        if not self.check_collision(new_x, new_y, self.current_piece.coords):
            self.current_piece.x = new_x
            self.current_piece.y = new_y
            
            # Update animation targets
            self.target_pos_x = float(new_x)
            self.target_pos_y = float(new_y)
            
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
        """Update game state with animations"""
        if self.game_over:
            return False
        
        if self.paused:
            return True
        
        current_time = time.time() * 1000
        dt = current_time - self.last_time
        self.fall_time += dt
        self.last_time = current_time
        
        # Update smooth piece position animations
        if self.current_piece:
            # Smooth interpolation towards target position
            speed = self.move_animation_speed * dt / 1000.0
            
            self.piece_pos_x += (self.target_pos_x - self.piece_pos_x) * speed
            self.piece_pos_y += (self.target_pos_y - self.piece_pos_y) * speed
            
            # Snap to target if very close
            if abs(self.piece_pos_x - self.target_pos_x) < 0.01:
                self.piece_pos_x = self.target_pos_x
            if abs(self.piece_pos_y - self.target_pos_y) < 0.01:
                self.piece_pos_y = self.target_pos_y
        
        # Handle line clearing animation
        if self.clearing_lines:
            self.line_clear_animation_time += dt
            if self.line_clear_animation_time >= 500:  # 0.5 seconds total
                self.finish_line_clear()
                return True
            elif self.line_clear_animation_time >= 200:  # Flash for 0.2 seconds
                self.line_clear_flash_time += dt
        
        # Natural piece falling (only if not clearing lines)
        if not self.clearing_lines and self.fall_time >= self.fall_speed:
            if not self.move_piece(0, 1):
                self.place_piece()
                lines_cleared = self.check_lines_to_clear()
                if lines_cleared:
                    self.start_line_clear_animation(lines_cleared)
                else:
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
        
        # Draw placed pieces with modern flat style and line clearing animation
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                if self.grid[y][x]:
                    # Check if this line is being cleared
                    is_clearing_line = y in self.clearing_lines
                    flash_effect = False
                    
                    if is_clearing_line and self.line_clear_flash_time > 0:
                        # Flash effect during line clearing
                        flash_intensity = int((self.line_clear_flash_time / 50) % 2)
                        flash_effect = flash_intensity == 1
                    
                    # Main block
                    rect = pygame.Rect(self.GRID_X + x * self.CELL_SIZE + 1,
                                     self.GRID_Y + y * self.CELL_SIZE + 1,
                                     self.CELL_SIZE - 2, self.CELL_SIZE - 2)
                    
                    if flash_effect:
                        # White flash during clearing
                        pygame.draw.rect(self.screen, (255, 255, 255), rect)
                    else:
                        pygame.draw.rect(self.screen, self.grid[y][x], rect)
                    
                    # Subtle border for definition
                    border_color = tuple(max(0, c - 30) for c in self.grid[y][x])
                    pygame.draw.rect(self.screen, border_color, rect, 1)
        
        # Draw current piece with smooth animation
        if self.current_piece and not self.clearing_lines:
            for dx, dy in self.current_piece.coords:
                # Use animated position for smooth movement
                px = self.piece_pos_x + dx
                py = self.piece_pos_y + dy
                
                # Convert to pixel coordinates
                pixel_x = self.GRID_X + px * self.CELL_SIZE + 1
                pixel_y = self.GRID_Y + py * self.CELL_SIZE + 1
                
                # Only draw visible parts
                if (0 <= px < self.GRID_WIDTH and py >= 0 and 
                    py < self.GRID_HEIGHT):
                    rect = pygame.Rect(pixel_x, pixel_y, 
                                     self.CELL_SIZE - 2, self.CELL_SIZE - 2)
                    
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
        # Information panel (left side, aligned)
        info_x = 50
        score_text = self.font.render(f"SCORE: {self.score}", True, self.TEXT_COLOR)
        self.screen.blit(score_text, (info_x, 80))
        
        level_text = self.font.render(f"LEVEL: {self.level}", True, self.TEXT_COLOR)
        self.screen.blit(level_text, (info_x, 110))
        
        lines_text = self.font.render(f"LINES: {self.lines_cleared}", True, self.TEXT_COLOR)
        self.screen.blit(lines_text, (info_x, 140))
        
        # Controls panel (left side, below info)
        controls_y_start = 200
        controls = [
            "CONTROLS:",
            "← → : Move",
            "↓ : Soft Drop", 
            "↑/Space : Rotate",
            "C : Hard Drop",
            "P : Pause",
            "ESC : Menu"
        ]
        
        for i, text in enumerate(controls):
            color = self.TEXT_COLOR if i == 0 else self.LIGHT_GRAY
            font_to_use = self.font if i == 0 else pygame.font.Font(None, 20)
            control_text = font_to_use.render(text, True, color)
            self.screen.blit(control_text, (info_x, controls_y_start + i * 22))
        
        # Next piece panel (right side)
        self.draw_next_piece()

    def draw_next_piece(self):
        """Draw the next piece preview with modern styling"""
        if not self.next_piece:
            return
        
        # Next piece box with title
        next_x = 600
        next_y = 80
        box_width = 120
        box_height = 120
        
        # Draw title
        title_text = self.font.render("NEXT", True, self.TEXT_COLOR)
        self.screen.blit(title_text, (next_x, next_y))
        
        # Draw preview box background
        preview_box = pygame.Rect(next_x, next_y + 30, box_width, box_height)
        pygame.draw.rect(self.screen, self.WHITE, preview_box)
        pygame.draw.rect(self.screen, self.LIGHT_GRAY, preview_box, 2)
        
        # Center the piece in the box
        piece_center_x = next_x + box_width // 2
        piece_center_y = next_y + 30 + box_height // 2
        
        for dx, dy in self.next_piece.coords:
            x = piece_center_x + dx * 18 - 9  # Center and scale
            y = piece_center_y + dy * 18 - 9
            rect = pygame.Rect(x, y, 16, 16)
            
            # Main block
            pygame.draw.rect(self.screen, self.next_piece.color, rect)
            
            # Subtle border
            border_color = tuple(max(0, c - 30) for c in self.next_piece.color)
            pygame.draw.rect(self.screen, border_color, rect, 1)

    def draw_pause_overlay(self):
        """Draw pause overlay with darkening effect"""
        # Dark semi-transparent overlay as specified
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(int(255 * 0.7))  # 70% transparency
        overlay.fill((51, 51, 51))  # #333333 dark gray
        self.screen.blit(overlay, (0, 0))
        
        # Large PAUSED text in white
        pause_font = pygame.font.Font(None, 72)
        pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(400, 280))
        self.screen.blit(pause_text, text_rect)
        
        # Instruction text below in white
        instruction_font = pygame.font.Font(None, 28)
        resume_text = instruction_font.render("Press P to resume or ESC for menu", True, (255, 255, 255))
        resume_rect = resume_text.get_rect(center=(400, 340))
        self.screen.blit(resume_text, resume_rect)
