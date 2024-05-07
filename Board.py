from coordinate import Coordinate
from orientation import Orientation
from ship import Ship
from ship_type import ShipType
from ship_state import ShipState
from cell_state import CellState


class Player:
    BOARDSIZE = 10

    def __init__(self, name: str):
        self.name = name
        self.board = [[Coordinate(row, col) for col in range(Player.BOARDSIZE)] for row in range(Player.BOARDSIZE)]
        self.ships = []

    def add_ship(self, start_coord: Coordinate, ship_type: ShipType, orientation: Orientation) -> None:
        # Calculate ship size
        ship_size = Ship.ship_size(ship_type)

        # Determine positions for the ship
        positions = set()
        for offset in range(ship_size):
            coord = start_coord.add_offset(offset, orientation)
            if not (0 <= coord.row < Player.BOARDSIZE and 0 <= coord.col < Player.BOARDSIZE):
                raise ValueError(f"Ship placement is outside the board at ({coord.row}, {coord.col})")
            if self.board[coord.row][coord.col].get_state()!= CellState.NONE:
                raise ValueError("Ship placement overlaps with another ship")
            positions.add(self.board[coord.row][coord.col])

        # Create and place the ship
        new_ship = Ship(ship_type, list(positions))
        self.ships.append(new_ship)
        for pos in positions:
            pos.set_state(CellState.SHIP)

    def __str__(self) -> str:
        return f"Player {self.name}:\n" + "\n".join(
            " ".join(str(cell.get_state_char()) for cell in row) for row in self.board)


# Example of usage:
player = Player("Alice")
try:
    start_position = Coordinate(0, 0)
    player.add_ship(start_position, ShipType.DESTROYER, Orientation.EAST)
except Exception as e:
    print(e)

print(player)
