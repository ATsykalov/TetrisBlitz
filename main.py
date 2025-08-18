import pygame
import sys
from game import TetrisGame
from auth import AuthManager

def main():
    """Main entry point for the Tetris game"""
    pygame.init()
    
    # Initialize display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tetris Game")
    clock = pygame.time.Clock()
    
    # Initialize authentication
    auth_manager = AuthManager()
    
    # Show main menu first
    while True:
        action = show_main_menu(screen, clock)
        if action == "new_game":
            username = show_login_screen(screen, clock, auth_manager)
            if username:
                break
        elif action == "quit":
            pygame.quit()
            sys.exit()
    
    # Initialize game
    game = TetrisGame(screen, username, auth_manager)
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Show menu
                    action = show_menu(screen, clock, auth_manager, username)
                    if action == "quit":
                        running = False
                    elif action == "restart":
                        game = TetrisGame(screen, username, auth_manager)
                    elif action == "stats":
                        show_stats(screen, clock, auth_manager, username)
                else:
                    game.handle_input(event)
        
        if not game.update():
            # Game over
            action = show_game_over(screen, clock, game.score, auth_manager, username)
            if action == "play_again":
                game = TetrisGame(screen, username, auth_manager)
            elif action == "main_menu":
                # Return to main menu
                main()
                return
        
        game.draw()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

def show_login_screen(screen, clock, auth_manager):
    """Display login screen and return username"""
    import time
    # Modern Classic colors
    BACKGROUND_COLOR = (224, 224, 224)
    TEXT_COLOR = (51, 51, 51)
    INPUT_BG_COLOR = (255, 255, 255)
    INPUT_BORDER_COLOR = (150, 150, 150)
    
    font = pygame.font.Font(None, 48)  # Larger title
    input_font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 18)
    username = ""
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username.strip():
                        auth_manager.login_user(username.strip())
                        return username.strip()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 20 and event.unicode.isprintable():
                        username += event.unicode
        
        # Light gray background
        screen.fill(BACKGROUND_COLOR)
        
        # Title
        title = font.render("TETRIS", True, TEXT_COLOR)
        screen.blit(title, (400 - title.get_width() // 2, 180))
        
        # Subtitle
        subtitle = input_font.render("Modern Classic Edition", True, TEXT_COLOR)
        screen.blit(subtitle, (400 - subtitle.get_width() // 2, 230))
        
        # Instructions
        inst = input_font.render("Enter your username:", True, TEXT_COLOR)
        screen.blit(inst, (400 - inst.get_width() // 2, 290))
        
        # Input box with modern styling
        input_rect = pygame.Rect(300, 320, 200, 35)
        pygame.draw.rect(screen, INPUT_BG_COLOR, input_rect)
        pygame.draw.rect(screen, INPUT_BORDER_COLOR, input_rect, 2)
        
        # Username text
        text_surface = input_font.render(username, True, TEXT_COLOR)
        screen.blit(text_surface, (input_rect.x + 8, input_rect.y + 8))
        
        # Blinking cursor animation
        cursor_visible = (int(time.time() * 2) % 2) == 0
        if cursor_visible:
            cursor_x = input_rect.x + 8 + text_surface.get_width()
            pygame.draw.line(screen, TEXT_COLOR, 
                           (cursor_x, input_rect.y + 6), 
                           (cursor_x, input_rect.y + 26), 2)
        
        # Enter instruction
        enter_text = small_font.render("Press ENTER to start", True, (120, 120, 120))
        screen.blit(enter_text, (400 - enter_text.get_width() // 2, 380))
        
        pygame.display.flip()
        clock.tick(60)

def show_menu(screen, clock, auth_manager, username):
    """Show pause menu and return action"""
    # Modern Classic colors
    BACKGROUND_COLOR = (224, 224, 224)
    TEXT_COLOR = (51, 51, 51)
    MENU_BG_COLOR = (255, 255, 255)
    MENU_BORDER_COLOR = (150, 150, 150)
    SELECTED_COLOR = (100, 100, 255)
    
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    menu_items = [
        ("Resume", "resume"),
        ("Restart", "restart"),
        ("View Stats", "stats"),
        ("Quit", "quit")
    ]
    
    selected = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    return menu_items[selected][1]
        
        # Semi-transparent overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill(BACKGROUND_COLOR)
        screen.blit(overlay, (0, 0))
        
        # Menu box with modern styling
        menu_rect = pygame.Rect(250, 200, 300, 220)
        pygame.draw.rect(screen, MENU_BG_COLOR, menu_rect)
        pygame.draw.rect(screen, MENU_BORDER_COLOR, menu_rect, 2)
        
        # Title
        title = font.render("PAUSED", True, TEXT_COLOR)
        screen.blit(title, (400 - title.get_width() // 2, 230))
        
        # Menu items
        for i, (text, action) in enumerate(menu_items):
            color = SELECTED_COLOR if i == selected else TEXT_COLOR
            item_text = small_font.render(text, True, color)
            screen.blit(item_text, (400 - item_text.get_width() // 2, 270 + i * 35))
        
        pygame.display.flip()
        clock.tick(60)

def show_stats(screen, clock, auth_manager, username):
    """Show user statistics"""
    # Modern Classic colors
    BACKGROUND_COLOR = (224, 224, 224)
    TEXT_COLOR = (51, 51, 51)
    STATS_BG_COLOR = (255, 255, 255)
    STATS_BORDER_COLOR = (150, 150, 150)
    
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    tiny_font = pygame.font.Font(None, 18)
    
    stats = auth_manager.get_user_stats(username)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return
        
        screen.fill(BACKGROUND_COLOR)
        
        # Stats box
        stats_rect = pygame.Rect(200, 180, 400, 280)
        pygame.draw.rect(screen, STATS_BG_COLOR, stats_rect)
        pygame.draw.rect(screen, STATS_BORDER_COLOR, stats_rect, 2)
        
        # Title
        title = font.render("STATISTICS", True, TEXT_COLOR)
        screen.blit(title, (400 - title.get_width() // 2, 210))
        
        # Username
        username_text = small_font.render(f"Player: {username}", True, TEXT_COLOR)
        screen.blit(username_text, (400 - username_text.get_width() // 2, 280))
        
        # High score
        score_text = small_font.render(f"Best Score: {stats['high_score']}", True, TEXT_COLOR)
        screen.blit(score_text, (400 - score_text.get_width() // 2, 320))
        
        # Games played
        games_text = small_font.render(f"Games Played: {stats['games_played']}", True, TEXT_COLOR)
        screen.blit(games_text, (400 - games_text.get_width() // 2, 360))
        
        # Instructions
        inst = tiny_font.render("Press any key to return", True, (120, 120, 120))
        screen.blit(inst, (400 - inst.get_width() // 2, 420))
        
        pygame.display.flip()
        clock.tick(60)

def show_game_over(screen, clock, score, auth_manager, username):
    """Show game over screen with buttons"""
    # Update user stats
    auth_manager.update_user_score(username, score)
    stats = auth_manager.get_user_stats(username)
    is_new_record = score == stats['high_score'] and score > 0
    
    selected = 0
    menu_items = [
        ("ИГРАТЬ СНОВА", "play_again"),
        ("ГЛАВНОЕ МЕНЮ", "main_menu")
    ]
    
    fade_alpha = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    return menu_items[selected][1]
        
        # Fade in effect
        fade_alpha = min(180, fade_alpha + 3)
        
        # Dark semi-transparent overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(fade_alpha)
        overlay.fill((51, 51, 51))  # #333333 dark gray
        screen.blit(overlay, (0, 0))
        
        if fade_alpha >= 180:  # Only show content when fully faded
            # Large GAME OVER text in white
            title_font = pygame.font.Font(None, 64)
            title = title_font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(title, (400 - title.get_width() // 2, 150))
            
            # Score information
            score_font = pygame.font.Font(None, 32)
            
            # New record notification
            if is_new_record:
                record_text = score_font.render("NEW RECORD!", True, (100, 255, 100))
                screen.blit(record_text, (400 - record_text.get_width() // 2, 220))
            
            # Final score
            final_score_text = score_font.render(f"FINAL SCORE: {score}", True, (255, 255, 255))
            screen.blit(final_score_text, (400 - final_score_text.get_width() // 2, 260))
            
            # Menu buttons
            button_font = pygame.font.Font(None, 28)
            button_y_start = 350
            button_height = 40
            button_width = 180
            button_spacing = 60
            
            for i, (text, action) in enumerate(menu_items):
                is_selected = i == selected
                button_rect = pygame.Rect(310, button_y_start + i * button_spacing, button_width, button_height)
                
                # Button styling
                if is_selected:
                    pygame.draw.rect(screen, (255, 255, 255), button_rect)
                    pygame.draw.rect(screen, (200, 200, 200), button_rect, 2)
                    text_color = (51, 51, 51)
                else:
                    pygame.draw.rect(screen, (100, 100, 100), button_rect)
                    pygame.draw.rect(screen, (150, 150, 150), button_rect, 2)
                    text_color = (255, 255, 255)
                
                # Button text
                button_text = button_font.render(text, True, text_color)
                text_x = button_rect.x + (button_width - button_text.get_width()) // 2
                text_y = button_rect.y + (button_height - button_text.get_height()) // 2
                screen.blit(button_text, (text_x, text_y))
        
        pygame.display.flip()
        clock.tick(60)

def show_main_menu(screen, clock):
    """Display main menu and return action"""
    import random
    import math
    
    # Modern Classic colors
    BACKGROUND_COLOR = (224, 224, 224)
    TEXT_COLOR = (51, 51, 51)
    BUTTON_COLOR = (255, 255, 255)
    BUTTON_HOVER_COLOR = (51, 51, 51)
    BUTTON_TEXT_COLOR = (51, 51, 51)
    BUTTON_TEXT_HOVER_COLOR = (255, 255, 255)
    DECORATIVE_ALPHA = 30
    
    title_font = pygame.font.Font(None, 64)
    button_font = pygame.font.Font(None, 32)
    
    menu_items = [
        ("НОВАЯ ИГРА", "new_game"),
        ("ВЫХОД", "quit")
    ]
    
    selected = 0
    
    # Generate decorative tetromino positions
    decorative_pieces = []
    piece_colors = [(0, 255, 255), (255, 255, 0), (128, 0, 128), (0, 128, 0), 
                   (255, 0, 0), (255, 165, 0), (0, 0, 255)]
    
    for _ in range(8):
        decorative_pieces.append({
            'x': random.randint(-50, 850),
            'y': random.randint(-50, 650),
            'color': random.choice(piece_colors),
            'rotation': random.randint(0, 3) * 90,
            'size': random.randint(40, 80)
        })
    
    fade_alpha = 0
    fade_in = True
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    return menu_items[selected][1]
        
        # Fade in effect
        if fade_in:
            fade_alpha = min(255, fade_alpha + 5)
            if fade_alpha >= 255:
                fade_in = False
        
        screen.fill(BACKGROUND_COLOR)
        
        # Draw decorative background tetrominos
        for piece in decorative_pieces:
            surf = pygame.Surface((piece['size'], piece['size']), pygame.SRCALPHA)
            color_with_alpha = (*piece['color'], DECORATIVE_ALPHA)
            surf.fill(color_with_alpha)
            rotated_surf = pygame.transform.rotate(surf, piece['rotation'])
            screen.blit(rotated_surf, (piece['x'], piece['y']))
        
        # Apply fade overlay
        if fade_alpha < 255:
            fade_overlay = pygame.Surface((800, 600))
            fade_overlay.set_alpha(255 - fade_alpha)
            fade_overlay.fill(BACKGROUND_COLOR)
            screen.blit(fade_overlay, (0, 0))
        
        # Title
        title = title_font.render("TETRIS GAME", True, TEXT_COLOR)
        screen.blit(title, (400 - title.get_width() // 2, 150))
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, 24)
        subtitle = subtitle_font.render("Modern Classic Edition", True, TEXT_COLOR)
        screen.blit(subtitle, (400 - subtitle.get_width() // 2, 210))
        
        # Menu buttons
        button_y_start = 300
        button_height = 50
        button_width = 200
        button_spacing = 70
        
        for i, (text, action) in enumerate(menu_items):
            is_selected = i == selected
            button_rect = pygame.Rect(300, button_y_start + i * button_spacing, button_width, button_height)
            
            # Button background
            button_color = BUTTON_HOVER_COLOR if is_selected else BUTTON_COLOR
            text_color = BUTTON_TEXT_HOVER_COLOR if is_selected else BUTTON_TEXT_COLOR
            
            pygame.draw.rect(screen, button_color, button_rect)
            pygame.draw.rect(screen, (150, 150, 150), button_rect, 2)
            
            # Button text
            button_text = button_font.render(text, True, text_color)
            text_x = button_rect.x + (button_width - button_text.get_width()) // 2
            text_y = button_rect.y + (button_height - button_text.get_height()) // 2
            screen.blit(button_text, (text_x, text_y))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
