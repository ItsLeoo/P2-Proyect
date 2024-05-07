from Cellstate import Cellstate
from Orientation import Orientation

class Coordinate:
    def __init__(self, row= -1, column= -1, state = None):
        self.column = column
        self.row= row
        self.state= state

    def set_coordinate(self, cadena):
        letra= cadena[0]
        numero= int(cadena[1])
        self.row =int(numero)-1

    def set_state(self, state):
        self.state=state

    def get_state(self):
        return self.state

    def set_column(self, column):
        self.column = column
    def get_column(self ):
        return self.column

    def set_row(self, row):
        self.row = row
    def get_row(self):
        return self.row

    def get_state_char(self):
        if self.state== Cellstate.NONE:
            return "N"
        elif self.state== Cellstate.SHIP:
            return "S"
        elif self.state== Cellstate.WATER:
            return "W"
        elif self.state== Cellstate.HIT:
            return "H"

    def __eq__(self, o):
        return self.row == o.row and self.column == o

    def add_offset(self, offset, orientation):
        resultado= Coordinate(self.row, self.column)
        if orientation == Orientation.NORTH:
            resultado.row -= offset
        elif orientation == Orientation.SOUTH:
            resultado.row += offset
        elif orientation == Orientation.EAST:
            resultado.column += offset
        else:
            resultado.column -= offset
        return resultado

    def __str__(self):
        letra= chr(self.row + ord("A"))
        numero= str(self.column +1)
        return letra + numero + self.get_state_char()

    @staticmethod
    def orientation_from_char(orientation):
        if orientation == "S":
            return Orientation.SOUTH
        elif orientation == "N":
            return Orientation.NORTH
        elif orientation == "E":
            return Orientation.EAST
        elif orientation == "W":
            return Orientation.WEST
        else:
            raise ValueError("Error en orientación" + orientation)

c= Coordinate()
print(c)
c= Coordinate(2,3, Cellstate.WATER)
print(c)


