# Importa las clases desde sus respectivos archivos
from orientation import Orientation
from ship_type import ShipType
from coordinate import Coordinate
from ship import Ship
import sys

class Player:
    BOARDSIZE = 10

    def __init__(self, name):
        self.name = name
        self.board = [[CellState.NONE for col in range(Player.BOARDSIZE)] for row in range(Player.BOARDSIZE)]
        self.ships = []

    def get_name(self):
        return self.name

    def add_ship(self, pos, ship_type, orientation):
        max_ships = {
            ShipType.BATTLESHIP: 1,
            ShipType.DESTROYER: 2,
            ShipType.CRUISE: 3,
            ShipType.SUBMARINE: 4
        }
        if len(self.ships) >= max_ships[ship_type]:
            raise Exception("EXCEPTION_MAX_SHIP_TYPE")
        for pos_ in self.ships:
            if pos.row == pos_.positions[0].row and pos.col == pos_.positions[0].col:
                raise Exception("EXCEPTION_GAME_STARTED")
        if self.board[pos.row][pos.col] != CellState.NONE:
            raise Exception("EXCEPTION_NONFREE_POSITION")
        positions = []
        for i in range(Ship.ship_size(ship_type)):
            if orientation == Orientation.HORIZONTAL:
                positions.append(Coordinate(pos.row, pos.col + i))
            else:
                positions.append(Coordinate(pos.row + i, pos.col))
        for pos_ in positions:
            if not (0 <= pos_.row < Player.BOARDSIZE and 0 <= pos_.col < Player.BOARDSIZE):
                raise Exception("EXCEPTION_OUTSIDE")
            if self.board[pos_.row][pos_.col] != CellState.NONE:
                raise Exception("EXCEPTION_NONFREE_POSITION")
        self.ships.append(Ship(ship_type, positions))

    def add_ships(self, ships):
        for ship in ships.split():
            type_char = ship[0]
            if type_char == "B":
                ship_type = ShipType.BATTLESHIP
            elif type_char == "D":
                ship_type = ShipType.DESTROYER
            elif type_char == "C":
                ship_type = ShipType.CRUISE
            elif type_char == "S":
                ship_type = ShipType.SUBMARINE
            else:
                raise Exception("EXCEPTION_INVALID_SHIP_TYPE")
            pos = Coordinate(int(ship[1][0]) - 1, ord(ship[1][1]) - ord("A"))
            orientation = Orientation.HORIZONTAL
                          if len(ship) > 2 and ship[2] == "V":
                orientation = Orientation.VERTICAL
            if len(ship) > 3:
                col_offset = ord(ship[3]) - ord("A")
                if orientation == Orientation.HORIZONTAL:
                    pos.col += col_offset
                elif orientation == Orientation.VERTICAL:
                    pos.row += col_offset
            try:
                self.add_ship(pos, ship_type, orientation)
            except Exception as e:
                print(f"Error adding ship {ship}: {e}")

    def attack(self, coord):
        try:
            col = coord.col
            row = coord.row
            if self.board[row][col] == CellState.SHIP:
                for ship in self.ships:
                    for pos in ship.positions:
                        if pos.row == row and pos.col == col:
                            ship.hit()
                            self.board[row][col] = CellState.HIT
                            if ship.is_sunk():
                                self.ships.remove(ship)
                                if len(self.ships) == 0:
                                    raise Exception("EXCEPTION_GAME_OVER")
                            return True
            elif self.board[row][col] == CellState.NONE:
                self.board[row][col] = CellState.WATER
                return False
        except Exception as e:
            print(f"Error attacking coordinate {coord}: {e}")
            return False

    def attack(self, coord_str):
        try:
            c = Coordinate(int(coord_str[0]) - 1, ord(coord_str[1]) - ord("A"))
            return self.attack(c)
        except Exception as e:
            print(f"Error attacking coordinate {coord_str}: {e}")
            return False

    def __str__(self):
        result = f"{self.name}\n"
        for row in range(Player.BOARDSIZE):
            result += " |"
            for col in range(Player.BOARDSIZE):
                if self.board[row][col] == CellState.NONE:
                    result += " - |"
                elif self.board[row][col] == CellState.SHIP:
                    result += " S |"
                elif self.board[row][col] == CellState.HIT:
                    result += " X |"
                elif self.board[row][col] == CellState.WATER:
                    result += " W |"
                elif self.board[row][col] == CellState.SUNK:
                    result += " s |"
            result += "\n"
        for ship in self.ships:
            result += str(ship) + "\n"
        return result
