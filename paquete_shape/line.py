import math

class InvalidPointError(Exception):
    pass

class InvalidLineError(Exception):
    pass

class GeometricCalculationError(Exception):
    pass

class Point:
    def __init__(self, x, y):
        try:
            self.x = float(x)
            self.y = float(y)
        except Exception:
            raise InvalidPointError("Coordenadas invalidas")
    def distance_to(self, other):
        if not isinstance(other, Point):
            raise InvalidPointError("Se esperaba Point")
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)
    def __str__(self):
        return f"Point({self.x}, {self.y})"
    def __eq__(self, other):
        return isinstance(other, Point) and abs(self.x - other.x) < 1e-10 and abs(self.y - other.y) < 1e-10

class Line:
    def __init__(self, inicio: "Point" = Point(0, 0), final: "Point" = Point(0, 0)):
        if not isinstance(inicio, Point) or not isinstance(final, Point):
            raise InvalidLineError("Los extremos deben ser Point")
        if inicio == final:
            raise InvalidLineError("Los puntos de inicio y final no pueden ser iguales")
        self.inicio = inicio
        self.final = final
        self.length = None
        self.slope = None
        self.range = None
    def compute_length(self):
        self.length = self.inicio.distance_to(self.final)
        if self.length <= 0:
            raise GeometricCalculationError("Longitud no valida")
        return self.length
    def compute_slope(self):
        dx = self.final.x - self.inicio.x
        if abs(dx) < 1e-10:
            raise GeometricCalculationError("Pendiente indefinida (linea vertical)")
        self.slope = (self.final.y - self.inicio.y) / dx
        return self.slope
    def range_of_the_line(self):
        if self.slope is None:
            raise GeometricCalculationError("Debes calcular la pendiente primero")
        self.range = []
        x0 = int(round(self.inicio.x))
        x1 = int(round(self.final.x))
        for i in range(x0, x1):
            self.range.append(Point(i, self.slope * i))
        return self.range
    def horizontal_cross(self):
        if self.range is None or len(self.range) < 2:
            raise GeometricCalculationError("Debes calcular el rango primero")
        for i in range(len(self.range) - 1):
            if self.range[i].x < 0 and self.range[i + 1].x > 0:
                print(f"Cross the x-axis between {self.range[i]} and {self.range[i+1]}")
                return
        print(f"don't Cross the x-axis")
    def vertical_cross(self):
        if self.range is None or len(self.range) < 2:
            raise GeometricCalculationError("Debes calcular el rango primero")
        for i in range(len(self.range) - 1):
            if self.range[i].y < 0 and self.range[i + 1].y > 0:
                print(f"Cross the y-axis between {self.range[i]} and {self.range[i+1]}")
                return
        print(f"don't Cross the y-axis")
