import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
TILE_SIZE = WIDTH // 8
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (169, 169, 169)
PIECE_SIZE = int(TILE_SIZE * 0.8)  # Pieces are 80% of the tile size

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Game')

# Board setup: 8x8 grid of pieces (standard initial setup)
board = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["",   "",   "",   "",   "",   "",   "",   ""],
    ["",   "",   "",   "",   "",   "",   "",   ""],
    ["",   "",   "",   "",   "",   "",   "",   ""],
    ["",   "",   "",   "",   "",   "",   "",   ""],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]

# Load piece images (filenames match the board codes, e.g., "wK.png", "bR.png", etc.)
images = {
    "wK": pygame.image.load('images/wK.png'),
    "wQ": pygame.image.load('images/wQ.png'),
    "wR": pygame.image.load('images/wR.png'),
    "wB": pygame.image.load('images/wB.png'),
    "wN": pygame.image.load('images/wN.png'),
    "wP": pygame.image.load('images/wP.png'),
    "bK": pygame.image.load('images/bK.png'),
    "bQ": pygame.image.load('images/bQ.png'),
    "bR": pygame.image.load('images/bR.png'),
    "bB": pygame.image.load('images/bB.png'),
    "bN": pygame.image.load('images/bN.png'),
    "bP": pygame.image.load('images/bP.png')
}

# Resize piece images
for key in images:
    images[key] = pygame.transform.scale(images[key], (PIECE_SIZE, PIECE_SIZE))

# Function to get tile label based on perspective.
def get_tile_label(row, col, player_color='white'):
    """
    Generate chess notation for a tile.
    For white: bottom-left = A1, bottom-right = H1, top-left = A8.
    For black: bottom-left = H8, bottom-right = A8, top-left = H1.
    """
    if player_color == 'white':
        columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        return f"{columns[col]}{8 - row}"
    else:
        # For black, reverse the columns and row numbering:
        columns_rev = ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
        return f"{columns_rev[col]}{row + 1}"

# Draw the chessboard
def draw_board(player_color):
    for row in range(8):
        for col in range(8):
            # Draw the squares
            color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            
            # Get the piece from the board.
            piece = board[row][col]
            if piece:
                # If the player is black, flip the rendering of the board (rotate 180 degrees)
                if player_color == 'black':
                    # Flip the row and column for black player's perspective
                    display_row = 7 - row
                    display_col = 7 - col
                    # Print the square being drawn for black pieces
                    print(f"Drawing {piece} at {get_tile_label(display_row, display_col, 'black')}")
                else:
                    # No flipping for white player's perspective
                    display_row = row
                    display_col = col
                
                # Blit the piece at the correct location
                screen.blit(images[piece], (
                    display_col * TILE_SIZE + (TILE_SIZE - PIECE_SIZE) // 2, 
                    display_row * TILE_SIZE + (TILE_SIZE - PIECE_SIZE) // 2
                ))
            
            # Draw the tile label in the bottom-left corner
            label = get_tile_label(row, col, player_color)
            font = pygame.font.Font(None, 20)  # You can adjust the label size here
            label_text = font.render(label, True, (0, 0, 0))
            screen.blit(label_text, (col * TILE_SIZE + 5, row * TILE_SIZE + TILE_SIZE - 20))



# Global game state class
class GameState:
    def __init__(self, player_color):
        self.player_color = player_color
        self.bot_color = 'black' if player_color == 'white' else 'white'
        # White always goes first. We'll designate the turn as either "player" or "bot"
        # If player is white, player goes first; if player is black, bot goes first.
        self.turn = "player" if player_color == 'white' else "bot"
        self.selected_tile = None  # (row, col) of currently selected piece

    def switch_turn(self):
        """Switch turns between player and bot."""
        self.turn = 'bot' if self.turn == 'player' else 'player'

# Main game loop
def main():
    # Randomly determine if the player is white or black.
    player_color = random.choice(['white', 'black'])
    game_state = GameState(player_color)
    
    # Turn always starts with white.
    turn = game_state.turn
    print(f"You are playing as {player_color}. {turn} goes first.")

    running = True
    selected_tile = None  # (row, col) of the selected piece

    while running:
        screen.fill((0, 0, 0))  # Clear the screen.
        draw_board(game_state.player_color)  # Draw the board based on the player's perspective.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // TILE_SIZE, x // TILE_SIZE

                # When the player is black, flip the input coordinates.
                if game_state.player_color == 'black':
                    row, col = 7 - row, 7 - col

                # If a tile is already selected, attempt to move.
                if selected_tile:
                    sel_row, sel_col = selected_tile
                    # Ensure the selected piece belongs to the current turn.
                    if (turn == 'white' and board[sel_row][sel_col][0] == 'w') or \
                       (turn == 'black' and board[sel_row][sel_col][0] == 'b'):
                        # Move piece from selected_tile to (row, col)
                        board[row][col] = board[sel_row][sel_col]
                        board[sel_row][sel_col] = ""
                        selected_tile = None
                        # Switch turn after move.
                        turn = 'black' if turn == 'white' else 'white'
                    else:
                        # Deselect if the piece doesn't match the turn.
                        selected_tile = None
                else:
                    # If no piece is selected, select the piece on the clicked square (if any).
                    if board[row][col]:
                        selected_tile = (row, col)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
