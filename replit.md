# Tetris Game

## Overview

A classic Tetris game implementation built with Python and Pygame. The game features user authentication, score tracking, and persistent data storage. Players can log in with usernames, play Tetris with standard piece mechanics, and have their high scores and game statistics saved across sessions.

## User Preferences

Preferred communication style: Simple, everyday language.

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
- **Progressive Difficulty**: Level-based speed increases as lines are cleared
- **Score System**: Points awarded for line clears with score persistence

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