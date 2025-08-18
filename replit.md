# Tetris Game

## Overview

A complete classic Tetris game implementation built with Python and Pygame, featuring Modern Classic design, smooth animations, and user authentication system. The game combines retro 80s aesthetics with contemporary smooth animations and a light color scheme. Players can log in with usernames, enjoy fluid gameplay with animated piece movement and line clearing effects, and have their high scores and statistics saved across sessions.

## User Preferences

Preferred communication style: Simple, everyday language in Russian.
Language: Russian language for all communication with the user.
Design style: Modern Classic - combining 8-bit aesthetics with contemporary clean interface and flat design.

## System Architecture

### Game Engine Architecture
- **Main Game Loop**: Built with Pygame for real-time rendering and event handling
- **Modular Design**: Separated into distinct modules for game logic, authentication, database, and piece management
- **State Management**: Game state includes grid, current/next pieces, score, level, and timing mechanics
- **Event-Driven Input**: Handles keyboard input for piece movement, rotation, and menu navigation

### Authentication System
- **Simple Username-Based Auth**: No password authentication - uses username as unique identifier
- **Session Management**: Tracks current logged-in user throughout game session
- **User Data Integration**: Seamlessly integrates with game mechanics for score updates

### Data Storage Strategy
- **Dual Storage Approach**: Automatically detects and uses Replit DB when available, falls back to local JSON file storage
- **User Profile Schema**: Stores username, high_score, and games_played for each user
- **Automatic Initialization**: Creates default user profiles on first login

### Game Mechanics  
- **Standard Tetris Rules**: Implements classic 7-piece Tetris with standard shapes (I, O, T, S, Z, J, L)
- **Grid-Based System**: 10x20 playing field with collision detection
- **Progressive Difficulty**: Level-based speed increases as lines are cleared (every 500 points)
- **Score System**: Quadratic scoring (1²-4² points for 1-4 lines) with score persistence
- **Smooth Animations**: Fluid piece movement with interpolated positions and line clearing effects
- **Modern Interface**: Clean UI with WASD/Arrow key support and intuitive navigation

## External Dependencies

### Core Dependencies
- **Pygame**: Primary game engine for graphics, input handling, and game loop management
- **Replit DB**: Cloud-based key-value storage for user data (when available)
- **JSON**: Fallback data serialization for local file storage

### Python Standard Library
- **os**: File system operations for local database fallback
- **time**: Game timing and fall speed mechanics  
- **random**: Piece generation and shuffling
- **sys**: Application lifecycle management

### Optional Dependencies
- **replit**: Replit-specific database integration (gracefully handled if unavailable)

The architecture prioritizes simplicity and reliability, with automatic fallbacks ensuring the game works in any Python environment while taking advantage of Replit-specific features when available.

## Recent Changes (August 2025)

### Animation System Implementation
- Added smooth interpolated movement for falling pieces using floating-point positions
- Implemented line clearing animations with white flash effects during 500ms animation cycles
- Enhanced visual feedback with progressive fade-in effects on menu screens

### Interface Improvements  
- Created animated main menu with decorative tetromino background elements
- Updated pause screen with 70% dark overlay as specified
- Redesigned Game Over screen with "Play Again" and "Main Menu" navigation buttons
- Fixed control text display by replacing Unicode arrows with WASD text
- Added dual input support for both WASD and arrow keys

### User Experience Enhancements
- Removed "Player" label from game interface for cleaner appearance  
- Improved Next piece preview box with centered positioning and better styling
- Enhanced button navigation with consistent highlight/selection states
- Added comprehensive README.md documentation with full project details

### Technical Architecture Updates
- Modular animation system with configurable timing and interpolation speeds
- Event-driven state management for smooth menu transitions
- Optimized rendering pipeline for 60 FPS gameplay with animation support

### Deployment Configuration (August 18, 2025)
- **Issue Identified**: Current deployment configured as Autoscale (Cloud Run) expecting HTTP web application
- **Problem**: Tetris is a desktop GUI application requiring VNC display, not HTTP endpoints
- **Solution Required**: Change to Reserved VM deployment with VNC output for proper Pygame support
- **Run Command**: `python main.py` (entry point verified and working)
- **Dependencies**: pygame>=2.6.1 (already installed via pyproject.toml)