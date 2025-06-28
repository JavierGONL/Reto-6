"""
Módulo Rectangle mejorado - Implementa la clase Rectangle con manejo de excepciones
Estudiante de POO - Reto 6

Incluye validación de dimensiones y cálculos geométricos con manejo robusto de errores.
"""

import math
from .shape_module import Shape, ShapeError, InvalidEdgeError, InsufficientDataError, GeometricCalculationError
from .point_module import Point, InvalidPointError
from .line_module import Line, InvalidLineError

class InvalidDimensionError(ShapeError):
    """Excepción para dimensiones inválidas"""
    def __init__(self, dimension, valor):
        self.dimension = dimension
        self.valor = valor
        super().__init__(f"Dimensión inválida para {dimension}: {valor}. Debe ser un número positivo")

class InvalidRectangleError(ShapeError):
    """Excepción para rectángulos inválidos"""
    def __init__(self, razon):
        self.razon = razon
        super().__init__(f"Rectángulo inválido: {razon}")

class Rectangle(Shape):
    """Clase que representa un rectángulo con manejo de excepciones"""
    
    def __init__(self, edges=None, width=None, height=None, bottom_left=None):
        """
        Inicializa un rectángulo
        
        Args:
            edges (list, optional): Lista de bordes del rectángulo
            width (float, optional): Ancho del rectángulo
            height (float, optional): Alto del rectángulo
            bottom_left (Point, optional): Punto inferior izquierdo
            
        Raises:
            InvalidDimensionError: Si las dimensiones no son válidas
            InvalidRectangleError: Si la configuración del rectángulo no es válida
        """
        try:
            # Inicializar la clase padre
            super().__init__(edges)
            
            # Inicializar atributos
            self.width = 0
            self.height = 0
            self.point_bottom_left = None
            self.point_bottom_right = None
            self.point_upper_left = None
            self.point_upper_right = None
            
            # Procesar inicialización según los parámetros dados
            if edges is not None:
                self._process_edges()
            elif width is not None and height is not None:
                self._init_from_dimensions(width, height, bottom_left)
            
        except (InvalidDimensionError, InvalidRectangleError, ShapeError) as e:
            raise e
        except Exception as e:
            raise InvalidRectangleError(f"error en inicialización: {e}")
    
    def _validate_dimension(self, value, dimension_name):
        """
        Valida una dimensión
        
        Args:
            value: Valor a validar
            dimension_name (str): Nombre de la dimensión
            
        Returns:
            float: Dimensión validada
            
        Raises:
            InvalidDimensionError: Si la dimensión no es válida
        """
        try:
            dim = float(value)
            
            if dim <= 0:
                raise InvalidDimensionError(dimension_name, dim)
            
            if math.isinf(dim) or math.isnan(dim):
                raise InvalidDimensionError(dimension_name, f"{dim} (infinito o NaN)")
            
            return dim
            
        except ValueError:
            raise InvalidDimensionError(dimension_name, f"{value} (no es un número)")
        except InvalidDimensionError as e:
            raise e
        except Exception as e:
            raise InvalidDimensionError(dimension_name, f"{value} (error: {e})")
    
    def _init_from_dimensions(self, width, height, bottom_left=None):
        """
        Inicializa el rectángulo desde dimensiones
        
        Args:
            width: Ancho del rectángulo
            height: Alto del rectángulo
            bottom_left (Point, optional): Punto inferior izquierdo
        """
        try:
            # Validar dimensiones
            self.width = self._validate_dimension(width, "width")
            self.height = self._validate_dimension(height, "height")
            
            # Establecer punto base
            if bottom_left is None:
                self.point_bottom_left = Point(0, 0)
            elif isinstance(bottom_left, Point):
                self.point_bottom_left = bottom_left
            else:
                raise InvalidRectangleError(f"bottom_left debe ser un Point, se recibió: {type(bottom_left).__name__}")
            
            # Crear los bordes
            self._create_edges_from_dimensions()
            
        except (InvalidDimensionError, InvalidRectangleError, InvalidPointError) as e:
            raise InvalidRectangleError(f"error inicializando desde dimensiones: {e}")
    
    def _create_edges_from_dimensions(self):
        """Crea los bordes del rectángulo a partir de las dimensiones"""
        try:
            if self.point_bottom_left is None:
                raise InvalidRectangleError("no se ha establecido el punto inferior izquierdo")
            
            # Calcular los otros puntos
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
            
            # Crear los bordes
            edge1 = Line(self.point_bottom_left, self.point_bottom_right)  # Inferior
            edge2 = Line(self.point_bottom_right, self.point_upper_right)  # Derecho
            edge3 = Line(self.point_upper_right, self.point_upper_left)    # Superior
            edge4 = Line(self.point_upper_left, self.point_bottom_left)    # Izquierdo
            
            self.edges = [edge1, edge2, edge3, edge4]
            
            # Calcular longitudes
            for edge in self.edges:
                edge.compute_length()
                
        except (InvalidPointError, InvalidLineError) as e:
            raise InvalidRectangleError(f"error creando bordes: {e}")
        except Exception as e:
            raise InvalidRectangleError(f"error inesperado creando bordes: {e}")
    
    def _process_edges(self):
        """Procesa los bordes para determinar dimensiones y punto base"""
        try:
            if len(self.edges) != 4:
                raise InvalidRectangleError(f"un rectángulo debe tener 4 bordes, se recibieron {len(self.edges)}")
            
            # Calcular longitudes de los bordes
            for edge in self.edges:
                edge.compute_length()
            
            # Identificar bordes horizontales y verticales
            horizontal_edges = []
            vertical_edges = []
            
            for i, edge in enumerate(self.edges):
                if edge.is_horizontal():
                    horizontal_edges.append((i, edge))
                elif edge.is_vertical():
                    vertical_edges.append((i, edge))
                else:
                    raise InvalidRectangleError(f"borde {i} no es horizontal ni vertical")
            
            # Validar que haya exactamente 2 bordes horizontales y 2 verticales
            if len(horizontal_edges) != 2 or len(vertical_edges) != 2:
                raise InvalidRectangleError(
                    f"debe haber 2 bordes horizontales y 2 verticales, "
                    f"se encontraron {len(horizontal_edges)} horizontales y {len(vertical_edges)} verticales"
                )
            
            # Obtener dimensiones
            self.width = horizontal_edges[0][1].length
            self.height = vertical_edges[0][1].length
            
            # Validar que los bordes opuestos tengan la misma longitud
            if abs(horizontal_edges[0][1].length - horizontal_edges[1][1].length) > 1e-10:
                raise InvalidRectangleError("los bordes horizontales opuestos tienen longitudes diferentes")
            
            if abs(vertical_edges[0][1].length - vertical_edges[1][1].length) > 1e-10:
                raise InvalidRectangleError("los bordes verticales opuestos tienen longitudes diferentes")
            
            # Encontrar el punto inferior izquierdo
            self._find_bottom_left_point()
            
        except InvalidRectangleError as e:
            raise e
        except Exception as e:
            raise InvalidRectangleError(f"error procesando bordes: {e}")
    
    def _find_bottom_left_point(self):
        """Encuentra el punto inferior izquierdo del rectángulo"""
        try:
            # Recopilar todos los puntos únicos
            points = set()
            for edge in self.edges:
                points.add((edge.inicio.x, edge.inicio.y))
                points.add((edge.final.x, edge.final.y))
            
            # Convertir a lista de puntos
            unique_points = [Point(x, y) for x, y in points]
            
            if len(unique_points) != 4:
                raise InvalidRectangleError(f"se esperaban 4 puntos únicos, se encontraron {len(unique_points)}")
            
            # Encontrar el punto con menor x y menor y
            min_x = min(point.x for point in unique_points)
            min_y = min(point.y for point in unique_points)
            
            self.point_bottom_left = Point(min_x, min_y)
            
            # Calcular los otros puntos
            self.point_bottom_right = Point(min_x + self.width, min_y)
            self.point_upper_left = Point(min_x, min_y + self.height)
            self.point_upper_right = Point(min_x + self.width, min_y + self.height)
            
        except Exception as e:
            raise InvalidRectangleError(f"error encontrando punto inferior izquierdo: {e}")
    
    def compute_area(self):
        """
        Calcula el área del rectángulo
        
        Returns:
            float: Área del rectángulo
            
        Raises:
            GeometricCalculationError: Si hay error en el cálculo
        """
        try:
            self.validate_for_calculation("cálculo de área")
            
            if self.width <= 0 or self.height <= 0:
                raise GeometricCalculationError(
                    "cálculo de área", 
                    f"dimensiones inválidas: width={self.width}, height={self.height}"
                )
            
            area = self.width * self.height
            return area
            
        except GeometricCalculationError as e:
            raise e
        except Exception as e:
            raise GeometricCalculationError("cálculo de área", f"error: {e}")
    
    def compute_perimeter(self):
        """
        Calcula el perímetro del rectángulo
        
        Returns:
            float: Perímetro del rectángulo
            
        Raises:
            GeometricCalculationError: Si hay error en el cálculo
        """
        try:
            self.validate_for_calculation("cálculo de perímetro")
            
            if self.width <= 0 or self.height <= 0:
                raise GeometricCalculationError(
                    "cálculo de perímetro", 
                    f"dimensiones inválidas: width={self.width}, height={self.height}"
                )
            
            perimeter = 2 * (self.width + self.height)
            return perimeter
            
        except GeometricCalculationError as e:
            raise e
        except Exception as e:
            raise GeometricCalculationError("cálculo de perímetro", f"error: {e}")
    
    def compute_inner_angles(self):
        """
        Calcula los ángulos internos del rectángulo
        
        Returns:
            list: Lista de ángulos internos (siempre [90, 90, 90, 90])
        """
        self.inner_angles = [90, 90, 90, 90]
        return self.inner_angles
    
    def compute_center(self):
        """
        Calcula el centro del rectángulo
        
        Returns:
            Point: Centro del rectángulo
            
        Raises:
            GeometricCalculationError: Si hay error en el cálculo
        """
        try:
            if self.point_bottom_left is None:
                raise GeometricCalculationError(
                    "cálculo de centro", 
                    "no se ha establecido el punto inferior izquierdo"
                )
            
            center_x = self.point_bottom_left.x + self.width / 2
            center_y = self.point_bottom_left.y + self.height / 2
            
            return Point(center_x, center_y)
            
        except InvalidPointError as e:
            raise GeometricCalculationError("cálculo de centro", f"error creando punto: {e}")
        except Exception as e:
            raise GeometricCalculationError("cálculo de centro", f"error: {e}")
    
    def contains_point(self, point):
        """
        Verifica si un punto está dentro del rectángulo
        
        Args:
            point (Point): Punto a verificar
            
        Returns:
            bool: True si el punto está dentro, False en caso contrario
            
        Raises:
            TypeError: Si point no es un Point
            GeometricCalculationError: Si hay error en el cálculo
        """
        try:
            if not isinstance(point, Point):
                raise TypeError(f"point debe ser un Point, se recibió: {type(point).__name__}")
            
            if self.point_bottom_left is None:
                raise GeometricCalculationError(
                    "verificación de contención", 
                    "rectángulo no inicializado correctamente"
                )
            
            # Verificar si está dentro de los límites
            within_x = (self.point_bottom_left.x <= point.x <= 
                       self.point_bottom_left.x + self.width)
            within_y = (self.point_bottom_left.y <= point.y <= 
                       self.point_bottom_left.y + self.height)
            
            return within_x and within_y
            
        except TypeError as e:
            raise e
        except Exception as e:
            raise GeometricCalculationError("verificación de contención", f"error: {e}")
    
    def intersects_with_rectangle(self, other_rectangle):
        """
        Verifica si este rectángulo se intersecta con otro
        
        Args:
            other_rectangle (Rectangle): Otro rectángulo
            
        Returns:
            bool: True si se intersectan, False en caso contrario
            
        Raises:
            TypeError: Si other_rectangle no es un Rectangle
            GeometricCalculationError: Si hay error en el cálculo
        """
        try:
            if not isinstance(other_rectangle, Rectangle):
                raise TypeError(f"other_rectangle debe ser un Rectangle, se recibió: {type(other_rectangle).__name__}")
            
            # Verificar que ambos rectángulos estén inicializados
            if (self.point_bottom_left is None or 
                other_rectangle.point_bottom_left is None):
                raise GeometricCalculationError(
                    "verificación de intersección", 
                    "uno o ambos rectángulos no están inicializados correctamente"
                )
            
            # Coordenadas de este rectángulo
            x1_min = self.point_bottom_left.x
            y1_min = self.point_bottom_left.y
            x1_max = x1_min + self.width
            y1_max = y1_min + self.height
            
            # Coordenadas del otro rectángulo
            x2_min = other_rectangle.point_bottom_left.x
            y2_min = other_rectangle.point_bottom_left.y
            x2_max = x2_min + other_rectangle.width
            y2_max = y2_min + other_rectangle.height
            
            # Verificar intersección
            no_intersect = (x1_max < x2_min or x2_max < x1_min or 
                           y1_max < y2_min or y2_max < y1_min)
            
            return not no_intersect
            
        except TypeError as e:
            raise e
        except Exception as e:
            raise GeometricCalculationError("verificación de intersección", f"error: {e}")
    
    def __str__(self):
        """Representación en cadena del rectángulo"""
        return f"Rectangle(width={self.width}, height={self.height}, bottom_left={self.point_bottom_left})"
    
    def __repr__(self):
        """Representación técnica del rectángulo"""
        return self.__str__()
