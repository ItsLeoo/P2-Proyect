# Importa las clases desde sus respectivos archivos
from orientation import Orientation
from ship_type import ShipType
from coordinate import Coordinate
from ship import Ship
import sys

class Player:
    BOARDSIZE = 10
    SHIP_SIZES = {ShipType.BATTLESHIP: 4, ShipType.DESTROYER: 3, ShipType.CRUISE: 2, ShipType.SUBMARINE: 1}
    MAX_SHIPS = {ShipType.BATTLESHIP: 1, ShipType.DESTROYER: 2, ShipType.CRUISE: 3, ShipType.SUBMARINE: 4}

    def _init_(self, name):
        self.name = name
        self.board = [[Coordinate(row, col) for col in range(Player.BOARDSIZE)] for row in range(Player.BOARDSIZE)]
        self.ships = []

    def add_ship(self, pos, type, orientation):
        # Comprueba el número máximo de barcos de ese tipo
        if sum(1 for ship in self.ships if ship.type == type) >= Player.MAX_SHIPS[type]:
            raise Exception("EXCEPTION_MAX_SHIP_TYPE")
        # Comprueba si el juego ya ha comenzado
        if any(coord.state != State.NONE for row in self.board for coord in row):
            raise Exception("EXCEPTION_GAME_STARTED")
        # Añade el barco comprobando las posiciones
        ship_size = Player.SHIP_SIZES[type]
        coordinates = []
        for offset in range(ship_size):
            coord = pos.add_offset(offset, orientation)
            if not (0 <= coord.row < Player.BOARDSIZE and 0 <= coord.col < Player.BOARDSIZE):
                raise Exception("EXCEPTION_OUTSIDE")
            if self.board[coord.row][coord.col].state != State.NONE:
                raise Exception("EXCEPTION_NONFREE_POSITION")
            coordinates.append(self.board[coord.row][coord.col])

        new_ship = Ship(type, ship_size)
        new_ship.coordinates = coordinates
        self.ships.append(new_ship)
        for coord in coordinates:
            coord.state = State.HIT  # Estado temporal para bloquear esta celda

    def attack(self, coord):
        for ship in self.ships:
            if coord in ship.coordinates:
                try:
                    ship.hit()
                    return True
                except Exception as e:
                    print(e, file=sys.stderr)
                    return False
        self.board[coord.row][coord.col].state = State.WATER
        return False

    def _str_(self):
        board_str = '\n'.join(' '.join(coord.state.name[0] for coord in row) for row in self.board)
        return f"Player {self.name}:\n{board_str}"

# Ejemplo de uso:
if _name_ == "_main_":
    player = Player("Alice")
    try:
        pos = Coordinate(0, 0)
        player.add_ship(pos, ShipType.DESTROYER, Orientation.EAST)
    except Exception as e:
        print(e)
    print(player)