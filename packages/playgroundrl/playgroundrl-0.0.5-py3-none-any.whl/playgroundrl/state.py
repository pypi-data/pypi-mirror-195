import attrs 
from typing import List, Dict
"""
Module with various game state representations
"""

@attrs.define
class GameState():
    player_moving: str
    """user_id of player who's current turn it is"""

    model_name: str
    """name of model who's turn it is next"""

@attrs.define
class ChessState(GameState):
    fen: str 
    """FEN representation of current board state"""


@attrs.define
class SnakeState(GameState):
    apple: List[int]
    """(x, y) of apple"""

    snake: List[List[int]]
    """[(x1, y1), (x2, y2), ... of snake's coordinates]"""


@attrs.define
class TicTacToeState(GameState):
    board: List[List[int]]
    """Current tic tac toe board"""


@attrs.define
class CatanState(GameState):
    tiles: Dict[str, Dict[str, str]]
    """first level keys are tile ids 1... 18.
        second level keys are "resource" with values SHEEP, BRICK, etc
        and "number" with dice sum values 2, 3 etc.
    """

    nodes: Dict[str, Dict[str, str]]
    """first level keys are node ids of the format x_y_z indicating up to
        three tiles that meet at a vertex where the node is.
        second level keys are "building" with values CITY or SETTLEMENT
        and "color" denoting the player color who owns that node
    """

    edges: Dict[str, Dict[str, str]]
    """first level keys are edge ids of the format [node_id]_[node_id]
        to uniquely identify the endpoints of the edge.
        second level keys are "color" with values denoting the player who owns the road
    """

    player_state: Dict[str, str]
    """a variety of properties about the player's state including WOOD_IN_HAND,
        HAS_ROAD, VICTORY_POINTS_IN_HAND, etc.
    """

    colors: List[str]
    """list of all player colors in the game"""

    is_initial_build_phase: bool
    """whether or not in the initial phase of placing first buildings and settlements"""

    robber_coordinate: int
    """tile with the robber"""

    current_prompt: str
    """prompt for the player's action"""

    playable_actions: List[Dict[str, str | List[str]]]
    """all possible actions for the player"""

    longest_roads_by_player: Dict[str, int]
    """length of the longest roads for each player"""

    winning_color: str
    """null if the game is not over, or a player color if someone has won"""


