import random

# Tetris piece shapes and colors
TETRIS_SHAPES = {
    'I': {
        'shape': [
            ['....'],
            ['IIII'],
            ['....'],
            ['....']
        ],
        'color': (0, 255, 255)  # Cyan
    },
    'O': {
        'shape': [
            ['OO'],
            ['OO']
        ],
        'color': (255, 255, 0)  # Yellow
    },
    'T': {
        'shape': [
            ['.T.'],
            ['TTT'],
            ['...']
        ],
        'color': (128, 0, 128)  # Purple
    },
    'S': {
        'shape': [
            ['.SS'],
            ['SS.'],
            ['...']
        ],
        'color': (0, 255, 0)  # Green
    },
    'Z': {
        'shape': [
            ['ZZ.'],
            ['.ZZ'],
            ['...']
        ],
        'color': (255, 0, 0)  # Red
    },
    'J': {
        'shape': [
            ['J..'],
            ['JJJ'],
            ['...']
        ],
        'color': (0, 0, 255)  # Blue
    },
    'L': {
        'shape': [
            ['..L'],
            ['LLL'],
            ['...']
        ],
        'color': (255, 165, 0)  # Orange
    }
}

class TetrisPiece:
    def __init__(self, piece_type=None):
        if piece_type is None:
            piece_type = random.choice(list(TETRIS_SHAPES.keys()))
        
        self.type = piece_type
        self.color = TETRIS_SHAPES[piece_type]['color']
        self.shape = self.convert_shape(TETRIS_SHAPES[piece_type]['shape'])
        self.x = 0
        self.y = 0
    
    def convert_shape(self, string_shape):
        """Convert string representation to boolean matrix"""
        converted = []
        for row in string_shape:
            converted_row = []
            for char in row:
                converted_row.append(char != '.')
            converted.append(converted_row)
        return converted
    
    def get_rotated_shape(self):
        """Return the shape rotated 90 degrees clockwise"""
        rows = len(self.shape)
        cols = len(self.shape[0])
        
        # Create new shape with swapped dimensions
        rotated = [[False for _ in range(rows)] for _ in range(cols)]
        
        for i in range(rows):
            for j in range(cols):
                rotated[j][rows - 1 - i] = self.shape[i][j]
        
        return rotated
    
    def rotate(self):
        """Rotate the piece 90 degrees clockwise"""
        self.shape = self.get_rotated_shape()
    
    def copy(self):
        """Create a copy of this piece"""
        new_piece = TetrisPiece(self.type)
        new_piece.shape = [row[:] for row in self.shape]
        new_piece.x = self.x
        new_piece.y = self.y
        return new_piece
