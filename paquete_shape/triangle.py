from math import acos, degrees
from .shape import Shape, ShapeError, GeometricCalculationError
from .line import Line

class InvalidTriangleError(Exception):
    pass

class Triangle(Shape):
    def __init__(self, edges: list = []):
        super().__init__()
        self.edges = edges
        self.perimeter = 0
        self.__area = 0
        self.angulos = []
    def compute_perimeter(self):
        if self.perimeter == 0:
            for i in range(len(self.edges)):
                self.edges[i].compute_length()
                self.perimeter += self.edges[i].length
            self.perimeter
    def compute_area(self):
        if self.perimeter == 0:
            self.compute_perimeter()
        if len(self.edges) != 3:
            raise InvalidTriangleError("Un triangulo debe tener 3 lados")
        semiperimetro = self.perimeter/2
        self.area = round((semiperimetro*(semiperimetro-self.edges[0].length)*(semiperimetro-self.edges[1].length)*(semiperimetro-self.edges[2].length))**(1/2),3)
    def compute_inner_angles(self):
        if len(self.edges) != 3:
            raise InvalidTriangleError("Un triangulo debe tener 3 lados")
        angulos = []
        for i in range(len(self.edges)):
            self.edges[i].compute_length()
        for i in range(len(self.edges)):
            a = self.edges[i].length
            b = self.edges[i-1].length
            c = self.edges[i-2].length
            cos_i = ((a**2 - b**2 - c**2) / (-2 * b * c))
            angulo = round(degrees(acos(cos_i)))
            angulos.append(angulo)
        self.angulos = angulos

class Isosceles(Triangle):
    definition = "Triangulo con 2 lados y angulos iguales"
    def __init__(self, edges = []):
        super().__init__(edges)

class Equilateral(Triangle):
    definition = "Triangulo con 3 lados y angulos iguales"
    def __init__(self, edges = []):
        super().__init__(edges)

class Scalene(Triangle):
    definition = "Triangulo con lados y angulos diferentes"
    def __init__(self, edges = []):
        super().__init__(edges)

class TriRectangle(Triangle):
    definition = "Triangulo con un angulo recto"
    def __init__(self, edges = []):
        super().__init__(edges)
