from stockfish import Stockfish, StockfishException

class ChessEngine:
    def __init__(self, stockfish_path, threads=1, hash_size=16, skill_level=20, ponder=False):
        """Initialize the Stockfish chess engine with custom settings."""
        self.stockfish = None
        self.stockfish_path = stockfish_path
        
        # Custom parameters for engine strength and speed
        self.parameters = {
            "Threads": threads,  # Number of threads to use for calculations (CPU cores)
            "Hash": hash_size,  # Hash size in MB, affects the engine's memory usage
            "Skill Level": skill_level,  # Skill level (0-20)
            "Ponder": "true" if ponder else "false",  # Whether the engine should ponder
            "Minimum Thinking Time": 20,  # Minimum thinking time in milliseconds
        }

    def initialize(self):
        """Initialize the Stockfish engine with custom parameters."""
        try:
            self.stockfish = Stockfish(path=self.stockfish_path, parameters=self.parameters)
            print("Stockfish initialized successfully with custom parameters.")
        except StockfishException as e:
            print(f"Error initializing Stockfish: {e}")
            self.cleanup()

    def set_position(self, moves):
        """Set a position by a sequence of moves."""
        try:
            if self.stockfish:
                self.stockfish.set_position(moves)
                print("Position set successfully.")
            else:
                raise Exception("Stockfish is not initialized.")
        except Exception as e:
            print(f"Error setting position: {e}")
            self.cleanup()

    def get_best_move(self):
        """Get the best move from Stockfish."""
        try:
            if self.stockfish:
                best_move = self.stockfish.get_best_move()
                return best_move
            else:
                raise Exception("Stockfish is not initialized.")
        except Exception as e:
            print(f"Error getting best move: {e}")
            self.cleanup()

    def update_parameters(self, new_parameters):
        """Update Stockfish parameters dynamically."""
        try:
            if self.stockfish:
                self.stockfish.update_engine_parameters(new_parameters)
                print("Engine parameters updated successfully.")
            else:
                raise Exception("Stockfish is not initialized.")
        except Exception as e:
            print(f"Error updating parameters: {e}")
            self.cleanup()

    def cleanup(self):
        """Clean up by shutting down the Stockfish engine."""
        if self.stockfish:
            self.stockfish = None
            print("Stockfish engine shut down.")

# Usage example:

if __name__ == "__main__":
    # Set the correct path to the Stockfish binary (adjust path as necessary)
    stockfish_path = "stockfish/stockfish-ubuntu-x86-64-avx2"
    
    # Initialize the ChessEngine with custom strength and speed settings
    engine = ChessEngine(stockfish_path, threads=1, hash_size=2048, skill_level=15, ponder=True)

    # Initialize the Stockfish engine
    engine.initialize()

    # Set up a position (e.g., after 1.e4 e5)
    engine.set_position(["e2e4", "e7e5"])

    # Get the best move
    best_move = engine.get_best_move()
    print(f"Best move: {best_move}")

    # Example of updating parameters dynamically (increase hash size and threads)
    engine.update_parameters({"Threads": 8, "Hash": 4096})

    # Clean up (shut down the Stockfish engine)
    engine.cleanup()
