import random

# Tetris piece shapes using coordinate system
TETRIS_SHAPES = {
    'I': {
        'coords': [(0, -1), (0, 0), (0, 1), (0, 2)],
        'color': (100, 180, 180)  # Приглушенный голубой
    },
    'O': {
        'coords': [(0, 0), (1, 0), (0, 1), (1, 1)],
        'color': (200, 200, 80)  # Приглушенный жёлтый
    },
    'T': {
        'coords': [(0, 0), (-1, 0), (1, 0), (0, 1)],
        'color': (150, 80, 150)  # Приглушенный фиолетовый
    },
    'S': {
        'coords': [(0, 0), (1, 0), (0, -1), (-1, -1)],
        'color': (80, 180, 80)  # Приглушенный зелёный
    },
    'Z': {
        'coords': [(0, 0), (-1, 0), (0, -1), (1, -1)],
        'color': (180, 80, 80)  # Приглушенный красный
    },
    'L': {
        'coords': [(0, 0), (-1, 0), (1, 0), (1, 1)],
        'color': (200, 140, 80)  # Приглушенный оранжевый
    },
    'J': {
        'coords': [(0, 0), (-1, 0), (1, 0), (-1, 1)],
        'color': (80, 120, 180)  # Приглушенный синий
    }
}

class TetrisPiece:
    def __init__(self, piece_type=None):
        if piece_type is None:
            piece_type = random.choice(list(TETRIS_SHAPES.keys()))
        
        self.type = piece_type
        self.color = TETRIS_SHAPES[piece_type]['color']
        self.coords = TETRIS_SHAPES[piece_type]['coords'][:]  # Copy coordinates
        self.x = 0
        self.y = 0
    
    def get_absolute_coords(self):
        """Get absolute coordinates of all blocks"""
        return [(self.x + dx, self.y + dy) for dx, dy in self.coords]
    
    def get_rotated_coords(self):
        """Return coordinates rotated 90 degrees clockwise"""
        # Rotate each coordinate: (x, y) -> (y, -x)
        return [(dy, -dx) for dx, dy in self.coords]
    
    def rotate(self):
        """Rotate the piece 90 degrees clockwise"""
        self.coords = self.get_rotated_coords()
    
    def copy(self):
        """Create a copy of this piece"""
        new_piece = TetrisPiece(self.type)
        new_piece.coords = self.coords[:]
        new_piece.x = self.x
        new_piece.y = self.y
        return new_piece
