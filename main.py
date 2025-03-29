import tkinter as tk
from stockfish import ChessEngine  # Import the ChessEngine class
from gui import ChessGameGUI  # Assuming gui.py is where the game logic is defined

def main():
    # Initialize Stockfish once at the start
    stockfish_path = "stockfish/stockfish-ubuntu-x86-64-avx2"  # Update with the correct path
    engine = ChessEngine(stockfish_path, threads=4, hash_size=2048, skill_level=15, ponder=True)
    engine.initialize()

    # Start the GUI with the initialized engine
    game = ChessGameGUI(engine)
    game.start()

    # Optionally clean up after the game ends
    engine.cleanup()
    #testing new ssh key commit

if __name__ == "__main__":
    main()
