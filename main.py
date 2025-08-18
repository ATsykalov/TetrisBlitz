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
    
    # Show login screen
    username = show_login_screen(screen, clock, auth_manager)
    if not username:
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
            show_game_over(screen, clock, game.score, auth_manager, username)
            game = TetrisGame(screen, username, auth_manager)
        
        game.draw()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

def show_login_screen(screen, clock, auth_manager):
    """Display login screen and return username"""
    import time
    font = pygame.font.Font(None, 36)
    input_font = pygame.font.Font(None, 24)
    username = ""
    active = True
    
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
        
        screen.fill((0, 0, 0))
        
        # Title
        title = font.render("TETRIS", True, (255, 255, 255))
        screen.blit(title, (400 - title.get_width() // 2, 200))
        
        # Instructions
        inst = input_font.render("Enter your username:", True, (255, 255, 255))
        screen.blit(inst, (400 - inst.get_width() // 2, 280))
        
        # Input box
        input_rect = pygame.Rect(300, 320, 200, 30)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
        
        # Username text
        text_surface = input_font.render(username, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        
        # Blinking cursor animation
        cursor_visible = (int(time.time() * 2) % 2) == 0  # Blinks every 0.5 seconds
        if cursor_visible:
            cursor_x = input_rect.x + 5 + text_surface.get_width()
            pygame.draw.line(screen, (255, 255, 255), 
                           (cursor_x, input_rect.y + 5), 
                           (cursor_x, input_rect.y + 20), 2)
        
        # Enter instruction
        enter_text = input_font.render("Press ENTER to start", True, (200, 200, 200))
        screen.blit(enter_text, (400 - enter_text.get_width() // 2, 380))
        
        pygame.display.flip()
        clock.tick(60)

def show_menu(screen, clock, auth_manager, username):
    """Show pause menu and return action"""
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
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Menu box
        menu_rect = pygame.Rect(250, 200, 300, 200)
        pygame.draw.rect(screen, (50, 50, 50), menu_rect)
        pygame.draw.rect(screen, (255, 255, 255), menu_rect, 2)
        
        # Title
        title = font.render("PAUSED", True, (255, 255, 255))
        screen.blit(title, (400 - title.get_width() // 2, 220))
        
        # Menu items
        for i, (text, action) in enumerate(menu_items):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            item_text = small_font.render(text, True, color)
            screen.blit(item_text, (400 - item_text.get_width() // 2, 260 + i * 30))
        
        pygame.display.flip()
        clock.tick(60)

def show_stats(screen, clock, auth_manager, username):
    """Show user statistics"""
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    stats = auth_manager.get_user_stats(username)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return
        
        screen.fill((0, 0, 0))
        
        # Title
        title = font.render("STATISTICS", True, (255, 255, 255))
        screen.blit(title, (400 - title.get_width() // 2, 200))
        
        # Username
        username_text = small_font.render(f"Player: {username}", True, (255, 255, 255))
        screen.blit(username_text, (400 - username_text.get_width() // 2, 280))
        
        # High score
        score_text = small_font.render(f"Best Score: {stats['high_score']}", True, (255, 255, 255))
        screen.blit(score_text, (400 - score_text.get_width() // 2, 320))
        
        # Games played
        games_text = small_font.render(f"Games Played: {stats['games_played']}", True, (255, 255, 255))
        screen.blit(games_text, (400 - games_text.get_width() // 2, 360))
        
        # Instructions
        inst = small_font.render("Press any key to return", True, (200, 200, 200))
        screen.blit(inst, (400 - inst.get_width() // 2, 420))
        
        pygame.display.flip()
        clock.tick(60)

def show_game_over(screen, clock, score, auth_manager, username):
    """Show game over screen"""
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    # Update user stats
    auth_manager.update_user_score(username, score)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Game over box
        box_rect = pygame.Rect(200, 200, 400, 200)
        pygame.draw.rect(screen, (50, 50, 50), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
        
        # Title
        title = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(title, (400 - title.get_width() // 2, 230))
        
        # Score
        score_text = small_font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (400 - score_text.get_width() // 2, 280))
        
        # High score
        stats = auth_manager.get_user_stats(username)
        high_score_text = small_font.render(f"Best Score: {stats['high_score']}", True, (255, 255, 255))
        screen.blit(high_score_text, (400 - high_score_text.get_width() // 2, 310))
        
        # Instructions
        inst = small_font.render("Press any key to continue", True, (200, 200, 200))
        screen.blit(inst, (400 - inst.get_width() // 2, 350))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
