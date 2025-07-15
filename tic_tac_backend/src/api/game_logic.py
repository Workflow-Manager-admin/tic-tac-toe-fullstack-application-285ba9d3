# game_logic.py
from typing import List, Optional, Dict, Any
import uuid

# Board is a 3x3 grid. 'X', 'O', or '' for empty
def new_board() -> List[List[str]]:
    return [["" for _ in range(3)] for _ in range(3)]

class Game:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.board = new_board()
        self.current_player = "X"
        self.status = "ongoing"  # 'ongoing', 'win', 'draw'
        self.winner: Optional[str] = None
        self.moves = 0

    # PUBLIC_INTERFACE
    def make_move(self, row: int, col: int) -> Dict[str, Any]:
        """Attempt a move; update board, and change turn if valid. Returns new state."""
        if self.status != "ongoing":
            return {"valid": False, "error": "Game is already over."}
        if not (0 <= row < 3 and 0 <= col < 3):
            return {"valid": False, "error": "Move out of bounds."}
        if self.board[row][col] != "":
            return {"valid": False, "error": "Cell already taken."}
        self.board[row][col] = self.current_player
        self.moves += 1

        # Check for win/draw after the move
        if self.check_win(self.current_player):
            self.status = "win"
            self.winner = self.current_player
        elif self.moves == 9:
            self.status = "draw"
            self.winner = None
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
        return {"valid": True, "state": self.to_dict()}

    # PUBLIC_INTERFACE
    def check_win(self, player: str) -> bool:
        """Check if the specified player has won."""
        b = self.board
        for i in range(3):
            if all(cell == player for cell in b[i]):
                return True
            if all(b[j][i] == player for j in range(3)):
                return True
        if all(b[i][i] == player for i in range(3)) or all(b[i][2 - i] == player for i in range(3)):
            return True
        return False

    # PUBLIC_INTERFACE
    def to_dict(self) -> Dict[str, Any]:
        """Represent the game state as a dictionary (for API response)."""
        return {
            "id": self.id,
            "board": self.board,
            "current_player": self.current_player,
            "status": self.status,
            "winner": self.winner,
            "moves": self.moves,
        }

# Game store (in-memory)
class GameStore:
    def __init__(self):
        self.games: Dict[str, Game] = {}

    # PUBLIC_INTERFACE
    def create_game(self) -> Game:
        """Create and store a new game instance."""
        game = Game()
        self.games[game.id] = game
        return game

    # PUBLIC_INTERFACE
    def get_game(self, game_id: str) -> Optional[Game]:
        """Retrieve a game by its ID."""
        return self.games.get(game_id)

    # PUBLIC_INTERFACE
    def list_games(self) -> List[Dict[str, Any]]:
        """List all games' basic info."""
        return [g.to_dict() for g in self.games.values()]

# Single global store instance for MVP/demo
store = GameStore()
