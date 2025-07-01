import math

class InvalidPointError(Exception):
    pass

class Point:
    def __init__(self, x, y):
        try:
            self.x = float(x)
            self.y = float(y)
        except Exception:
            raise InvalidPointError("Coordenadas invalidas")
    def another_point(self, new_x, new_y):
        return Point(new_x, new_y)
    def distance_to(self, other):
        if not isinstance(other, Point):
            raise InvalidPointError("Se esperaba Point")
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2) ** 0.5
    def __str__(self):
        return f"Point({self.x}, {self.y})"
    def __eq__(self, other):
        return isinstance(other, Point) and abs(self.x - other.x) < 1e-10 and abs(self.y - other.y) < 1e-10