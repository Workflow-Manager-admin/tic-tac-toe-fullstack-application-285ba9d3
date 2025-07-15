from pydantic import BaseModel, Field
from typing import List, Optional

# PUBLIC_INTERFACE
class CreateGameResponse(BaseModel):
    """Response for creating a new game"""
    id: str = Field(..., description="Unique identifier for the game")
    board: List[List[str]] = Field(..., description="Tic-tac-toe board state")
    current_player: str = Field(..., description="Current player's turn ('X' or 'O')")
    status: str = Field(..., description="'ongoing', 'win', or 'draw'")
    winner: Optional[str] = Field(None, description="'X', 'O', or None")
    moves: int = Field(..., description="Number of moves made so far")

# PUBLIC_INTERFACE
class MoveRequest(BaseModel):
    """Request to submit a move in a game"""
    game_id: str = Field(..., description="Game identifier")
    row: int = Field(..., ge=0, le=2, description="Board row (0-2)")
    col: int = Field(..., ge=0, le=2, description="Board column (0-2)")

# PUBLIC_INTERFACE
class MoveResponse(BaseModel):
    """Response to a move submission"""
    valid: bool = Field(..., description="Was the move legal and accepted?")
    error: Optional[str] = Field(None, description="Error if move was invalid")
    state: Optional[CreateGameResponse] = Field(None, description="Game state after the move")

# PUBLIC_INTERFACE
class GameStateResponse(CreateGameResponse):
    """Current state of a specific game"""
    pass

# PUBLIC_INTERFACE
class GamesListResponse(BaseModel):
    """Response for listing all games"""
    games: list[CreateGameResponse] = Field(..., description="List of all game states")
