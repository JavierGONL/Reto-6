import math
from .shape import Shape, ShapeError, GeometricCalculationError
from .line import Line, InvalidLineError
from .point import Point, InvalidPointError

class InvalidDimensionError(ShapeError):
    pass

class InvalidRectangleError(Exception):
    pass

class Rectangle(Shape):
    def __init__(self, edges = []):
        self.edges = edges
        for i in range(len(edges)-1):
            self.edges[i].compute_length()
            if (edges[i+1].inicio.x > edges[i].inicio.x and edges[i+1].inicio.y > edges[i].inicio.y):
                point_bottom_left = i
            if edges[i].inicio.y == edges[i].final.y:
                self.width = edges[i].length
            if edges[i].inicio.x == edges[i].final.x:
                self.height = edges[i].length
        self.point_bottom_left = point_bottom_left
        self.inner_angles = []
        self.point_bottom_right = None
        self.point_upper_left = None
        self.point_upper_right = None
    def init_bottom_left(self):
        if not hasattr(self, 'width') or not hasattr(self, 'height'):
            raise InvalidRectangleError("Faltan dimensiones para inicializar esquinas")
        self.point_bottom_right = self.point_bottom_left.another_point(self.point_bottom_left.x + self.width, self.point_bottom_left.y)
        self.point_upper_left = self.point_bottom_left.another_point(self.point_bottom_left.x, self.point_bottom_left.y + self.height)
        self.point_upper_right = self.point_bottom_left.another_point(self.point_bottom_left.x + self.width, self.point_bottom_left.y + self.height)
        return [self.point_bottom_left, self.point_bottom_right, self.point_upper_left, self.point_upper_right]
    def compute_center(self):
        if not hasattr(self, 'width') or not hasattr(self, 'height'):
            raise InvalidRectangleError("Faltan dimensiones para calcular el centro")
        return Point(self.point_bottom_left.x + self.width / 2, self.point_bottom_left.y + self.height / 2)
    def compute_area(self):
        if not hasattr(self, 'width') or not hasattr(self, 'height'):
            raise InvalidRectangleError("Faltan dimensiones para calcular el area")
        return self.width * self.height
    def compute_perimeter(self):
        if not hasattr(self, 'width') or not hasattr(self, 'height'):
            raise InvalidRectangleError("Faltan dimensiones para calcular el perimetro")
        return 2 * self.width + 2 * self.height
    def compute_inner_angles(self):
        self.inner_angles = [90, 90, 90, 90]
    def compute_interference_between_2_rectangles(self, square_2: "Rectangle"):
        if not hasattr(self, 'center') or not hasattr(square_2, 'center'):
            raise InvalidRectangleError("Faltan centros para calcular interferencia")
        centro_1 = self.center
        centro_2 = square_2.center
        distancia = ((centro_2.x - centro_1.x)**2 +(centro_2.y - centro_1.y)**2)**0.5
        cateto_opuesto = centro_2.y - centro_1.y
        coseno = cateto_opuesto / distancia
        hipotenusa_square_1 = abs(coseno * (self.width / 2))
        hipotenusa_square_2 = abs((coseno * (square_2.width / 2)))
        if distancia <= hipotenusa_square_1 + hipotenusa_square_2:
            print(f"interfieren")
        else:
            print(f"no interfieren")
    def compute_interferece_between_rectangle_and_point(self, point: "Point"):
        if not hasattr(self, 'center'):
            raise InvalidRectangleError("Falta centro para calcular interferencia")
        centro_1 = self.center
        centro_2 = point
        distancia = ((centro_2.x - centro_1.x)**2 +(centro_2.y - centro_1.y)**2)**0.5
        cateto_opuesto = centro_2.y - centro_1.y
        coseno = cateto_opuesto / distancia
        hipotenusa_square_1 = abs(coseno * (self.width / 2))
        if distancia <= hipotenusa_square_1:
            print(f"interfieren")
        else:
            print(f"no interfieren")
    def compute_interference_between_rectangle_and_line(self, line: "Line"):
        if not hasattr(self, 'center'):
            raise InvalidRectangleError("Falta centro para calcular interferencia")
        centro_1 = self.center
        line = line.range_of_the_line()
        interfieren = False
        for i in range(len(line)):
            distancia = (((line[i].x - centro_1.x))**2 +(line[i].y - centro_1.y)**2)**0.5
            cateto_opuesto = line[i].y - centro_1.y
            coseno = cateto_opuesto / distancia
            if coseno == 0:
                hipotenusa_square_1 = self.width / 2
            else:
                hipotenusa_square_1 = abs(cateto_opuesto / coseno)
            if distancia <= hipotenusa_square_1:
                interfieren = True
                break
        return interfieren
