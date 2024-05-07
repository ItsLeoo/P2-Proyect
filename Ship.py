from Shipstate import ShipState
from ShipType import ShipType

class Ship:
    def __init__(self, ttype, positions):
        self.type = ttype
        self.positions = []
        for p in positions:
            self.positions.append(p)
        self.state= ShipState.OK
        if Ship.ship_size(ttype) != len(positions):
            raise ValueError("Wrong count coordinates")

    @staticmethod
    def ship_size(ttype):
        if ttype == ShipType.BATTLESHIP:
            long = 4
        elif ttype == ShipType.CRUISE:
            long = 3
        elif ttype == ShipType.DESTROYER:
            long = 2
        elif ttype == ShipType.SUBMARINE:
            long = 1
        else:
            raise ValueError("ShipType error")

        return long

    @staticmethod
    def type_from_char(car):
        if car == "B":
            return ShipType.BATTLESHIP
        elif car == "C":
            return ShipType.CRUISE
        elif car== "D":
            return ShipType.DESTROYER
        elif car == "S":
            return ShipType.SUBMARINE
        else:
            raise ValueError("Car type error")

    def getPosition(self, pos):
        if pos >= 0 and pos < len(self.positions):
            return self.positions[pos]
        else:
            return None

    def get_type(self):
        return self.type

    def get_state(self):
        return self.state
