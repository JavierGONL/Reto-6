import math
from .shape import Shape, ShapeError, GeometricCalculationError
from .point import Point, InvalidPointError
from .line import Line, InvalidLineError

class InvalidDimensionError(ShapeError):
    def __init__(self, dimension, valor):
        self.dimension = dimension
        self.valor = valor
        super().__init__(f"Dimensión inválida para {dimension}: {valor}. Debe ser un número positivo")

class InvalidRectangleError(ShapeError):
    def __init__(self, razon):
        self.razon = razon
        super().__init__(f"Rectángulo inválido: {razon}")

class Rectangle(Shape):
    def __init__(self, edges=None, width=None, height=None, bottom_left=None):
        try:
            super().__init__(edges)
            self.width = 0
            self.height = 0
            self.point_bottom_left = None
            self.point_bottom_right = None
            self.point_upper_left = None
            self.point_upper_right = None
            if edges is not None:
                self._process_edges()
            elif width is not None and height is not None:
                self._init_from_dimensions(width, height, bottom_left)
        except (InvalidDimensionError, InvalidRectangleError, ShapeError) as error:
            raise error
        except Exception as error:
            raise InvalidRectangleError(f"error en inicialización: {error}")

    def _validate_dimension(self, value, dimension_name):
        try:
            dim = float(value)
            if dim <= 0:
                raise InvalidDimensionError(dimension_name, dim)
            if math.isinf(dim) or math.isnan(dim):
                raise InvalidDimensionError(dimension_name, f"{dim} (infinito o NaN)")
            return dim
        except ValueError:
            raise InvalidDimensionError(dimension_name, f"{value} (no es un número)")
        except InvalidDimensionError as error:
            raise error
        except Exception as error:
            raise InvalidDimensionError(dimension_name, f"{value} (error: {error})")

    def _init_from_dimensions(self, width, height, bottom_left=None):
        try:
            self.width = self._validate_dimension(width, "width")
            self.height = self._validate_dimension(height, "height")
            if bottom_left is None:
                self.point_bottom_left = Point(0, 0)
            elif isinstance(bottom_left, Point):
                self.point_bottom_left = bottom_left
            else:
                raise InvalidRectangleError(f"bottom_left debe ser un Point, se recibió: {type(bottom_left).__name__}")
            self._create_edges_from_dimensions()
        except (InvalidDimensionError, InvalidRectangleError, InvalidPointError) as error:
            raise InvalidRectangleError(f"error inicializando desde dimensiones: {error}")

    def _create_edges_from_dimensions(self):
        try:
            if self.point_bottom_left is None:
                raise InvalidRectangleError("no se ha establecido el punto inferior izquierdo")
            self.point_bottom_right = Point(
                self.point_bottom_left.x + self.width, 
                self.point_bottom_left.y
            )
            self.point_upper_left = Point(
                self.point_bottom_left.x, 
                self.point_bottom_left.y + self.height
            )
            self.point_upper_right = Point(
                self.point_bottom_left.x + self.width, 
                self.point_bottom_left.y + self.height
            )
            edge1 = Line(self.point_bottom_left, self.point_bottom_right)
            edge2 = Line(self.point_bottom_right, self.point_upper_right)
            edge3 = Line(self.point_upper_right, self.point_upper_left)
            edge4 = Line(self.point_upper_left, self.point_bottom_left)
            self.edges = [edge1, edge2, edge3, edge4]
            for edge in self.edges:
                edge.compute_length()
        except (InvalidPointError, InvalidLineError) as error:
            raise InvalidRectangleError(f"error creando bordes: {error}")
        except Exception as error:
            raise InvalidRectangleError(f"error inesperado creando bordes: {error}")

    def _process_edges(self):
        try:
            if len(self.edges) != 4:
                raise InvalidRectangleError(f"un rectángulo debe tener 4 bordes, se recibieron {len(self.edges)}")
            for edge in self.edges:
                edge.compute_length()
            horizontal_edges = []
            vertical_edges = []
            for i, edge in enumerate(self.edges):
                if edge.is_horizontal():
                    horizontal_edges.append((i, edge))
                elif edge.is_vertical():
                    vertical_edges.append((i, edge))
                else:
                    raise InvalidRectangleError(f"borde {i} no es horizontal ni vertical")
            if len(horizontal_edges) != 2 or len(vertical_edges) != 2:
                raise InvalidRectangleError(
                    f"debe haber 2 bordes horizontales y 2 verticales, "
                    f"se encontraron {len(horizontal_edges)} horizontales y {len(vertical_edges)} verticales"
                )
            self.width = horizontal_edges[0][1].length
            self.height = vertical_edges[0][1].length
            if abs(horizontal_edges[0][1].length - horizontal_edges[1][1].length) > 1e-10:
                raise InvalidRectangleError("los bordes horizontales opuestos tienen longitudes diferentes")
            if abs(vertical_edges[0][1].length - vertical_edges[1][1].length) > 1e-10:
                raise InvalidRectangleError("los bordes verticales opuestos tienen longitudes diferentes")
            self._find_bottom_left_point()
        except InvalidRectangleError as error:
            raise error
        except Exception as error:
            raise InvalidRectangleError(f"error procesando bordes: {error}")

    def _find_bottom_left_point(self):
        try:
            points = set()
            for edge in self.edges:
                points.add((edge.inicio.x, edge.inicio.y))
                points.add((edge.final.x, edge.final.y))
            unique_points = [Point(x, y) for x, y in points]
            if len(unique_points) != 4:
                raise InvalidRectangleError(f"se esperaban 4 puntos únicos, se encontraron {len(unique_points)}")
            min_x = min(point.x for point in unique_points)
            min_y = min(point.y for point in unique_points)
            self.point_bottom_left = Point(min_x, min_y)
            self.point_bottom_right = Point(min_x + self.width, min_y)
            self.point_upper_left = Point(min_x, min_y + self.height)
            self.point_upper_right = Point(min_x + self.width, min_y + self.height)
        except Exception as error:
            raise InvalidRectangleError(f"error encontrando punto inferior izquierdo: {error}")

    def compute_area(self):
        try:
            self.validate_for_calculation("cálculo de área")
            if self.width <= 0 or self.height <= 0:
                raise GeometricCalculationError(
                    "cálculo de área", 
                    f"dimensiones inválidas: width={self.width}, height={self.height}"
                )
            area = self.width * self.height
            return area
        except GeometricCalculationError as error:
            raise error
        except Exception as error:
            raise GeometricCalculationError("cálculo de área", f"error: {error}")

    def compute_perimeter(self):
        try:
            self.validate_for_calculation("cálculo de perímetro")
            if self.width <= 0 or self.height <= 0:
                raise GeometricCalculationError(
                    "cálculo de perímetro", 
                    f"dimensiones inválidas: width={self.width}, height={self.height}"
                )
            perimeter = 2 * (self.width + self.height)
            return perimeter
        except GeometricCalculationError as error:
            raise error
        except Exception as error:
            raise GeometricCalculationError("cálculo de perímetro", f"error: {error}")

    def compute_inner_angles(self):
        self.inner_angles = [90, 90, 90, 90]
        return self.inner_angles

    def compute_center(self):
        try:
            if self.point_bottom_left is None:
                raise GeometricCalculationError(
                    "cálculo de centro", 
                    "no se ha establecido el punto inferior izquierdo"
                )
            center_x = self.point_bottom_left.x + self.width / 2
            center_y = self.point_bottom_left.y + self.height / 2
            return Point(center_x, center_y)
        except InvalidPointError as error:
            raise GeometricCalculationError("cálculo de centro", f"error creando punto: {error}")
        except Exception as error:
            raise GeometricCalculationError("cálculo de centro", f"error: {error}")

    def contains_point(self, point):
        try:
            if not isinstance(point, Point):
                raise TypeError(f"point debe ser un Point, se recibió: {type(point).__name__}")
            if self.point_bottom_left is None:
                raise GeometricCalculationError(
                    "verificación de contención", 
                    "rectángulo no inicializado correctamente"
                )
            within_x = (self.point_bottom_left.x <= point.x <= 
                       self.point_bottom_left.x + self.width)
            within_y = (self.point_bottom_left.y <= point.y <= 
                       self.point_bottom_left.y + self.height)
            return within_x and within_y
        except TypeError as error:
            raise error
        except Exception as error:
            raise GeometricCalculationError("verificación de contención", f"error: {error}")

    def intersects_with_rectangle(self, other_rectangle):
        try:
            if not isinstance(other_rectangle, Rectangle):
                raise TypeError(f"other_rectangle debe ser un Rectangle, se recibió: {type(other_rectangle).__name__}")
            if (self.point_bottom_left is None or 
                other_rectangle.point_bottom_left is None):
                raise GeometricCalculationError(
                    "verificación de intersección", 
                    "uno o ambos rectángulos no están inicializados correctamente"
                )
            x1_min = self.point_bottom_left.x
            y1_min = self.point_bottom_left.y
            x1_max = x1_min + self.width
            y1_max = y1_min + self.height
            x2_min = other_rectangle.point_bottom_left.x
            y2_min = other_rectangle.point_bottom_left.y
            x2_max = x2_min + other_rectangle.width
            y2_max = y2_min + other_rectangle.height
            no_intersect = (x1_max < x2_min or x2_max < x1_min or 
                           y1_max < y2_min or y2_max < y1_min)
            return not no_intersect
        except TypeError as error:
            raise error
        except Exception as error:
            raise GeometricCalculationError("verificación de intersección", f"error: {error}")

    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height}, bottom_left={self.point_bottom_left})"
    
    def __repr__(self):
        return self.__str__()
