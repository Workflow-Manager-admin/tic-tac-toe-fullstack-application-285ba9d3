from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .game_logic import store
from .schemas import (
    CreateGameResponse,
    MoveRequest,
    MoveResponse,
    GameStateResponse,
    GamesListResponse,
)

openapi_tags = [
    {
        "name": "TicTacToe",
        "description": "Endpoints for managing tic-tac-toe games and moves."
    }
]

app = FastAPI(
    title="Tic Tac Toe Backend API",
    description="REST API for tic-tac-toe game logic, state management, and moves.",
    version="1.0.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["TicTacToe"], summary="Health check", description="Basic health check endpoint")
def health_check():
    """Check if the backend is running"""
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.post("/game", response_model=CreateGameResponse, tags=["TicTacToe"], summary="Create new tic-tac-toe game", description="Creates a new game and returns its initial state")
def create_game():
    """
    Creates a new tic-tac-toe game.

    Returns:
        Game state for the newly created game.
    """
    game = store.create_game()
    return CreateGameResponse(**game.to_dict())

# PUBLIC_INTERFACE
@app.post("/move", response_model=MoveResponse, tags=["TicTacToe"], summary="Submit a move", description="Attempt a tic-tac-toe move; returns new game state or error.")
def submit_move(req: MoveRequest):
    """
    Submits a move for a tic-tac-toe game.

    Args:
        req: MoveRequest with game_id, row, col.

    Returns:
        MoveResponse with validity, error, and state.
    """
    game = store.get_game(req.game_id)
    if not game:
        return MoveResponse(valid=False, error="Game not found", state=None)
    move_result = game.make_move(req.row, req.col)
    if move_result["valid"]:
        return MoveResponse(valid=True, error=None, state=CreateGameResponse(**game.to_dict()))
    else:
        return MoveResponse(valid=False, error=move_result["error"], state=CreateGameResponse(**game.to_dict()))

# PUBLIC_INTERFACE
@app.get("/game/{game_id}", response_model=GameStateResponse, tags=["TicTacToe"], summary="Get game state", description="Returns current state of specified game")
def get_game_state(game_id: str):
    """
    Get the current state of a tic-tac-toe game.

    Args:
        game_id: The ID of the game.

    Returns:
        Current game state.
    """
    game = store.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return CreateGameResponse(**game.to_dict())

# PUBLIC_INTERFACE
@app.get("/games", response_model=GamesListResponse, tags=["TicTacToe"], summary="List all games", description="(Optional) Lists all current and completed games")
def list_games():
    """
    List all tic-tac-toe games (both active and completed).

    Returns:
        A list of all games known on the server.
    """
    return GamesListResponse(games=[CreateGameResponse(**game_dict) for game_dict in store.list_games()])

# If any secrets/configs are needed, read from os.environ (from .env)
# For MVP, none are required. Example usage:
# secret = os.environ.get('SOME_ENV_KEY', 'default_value')
