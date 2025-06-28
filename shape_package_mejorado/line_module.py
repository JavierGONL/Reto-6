"""
Módulo Line mejorado - Representa una línea entre dos puntos con manejo de excepciones
Estudiante de POO - Reto 6

Incluye validación de puntos y cálculos geométricos con manejo de errores.
"""

import math
from .point_module import Point, InvalidPointError

class InvalidLineError(Exception):
    """Excepción para líneas inválidas"""
    def __init__(self, line_info, razon):
        self.line_info = line_info
        self.razon = razon
        super().__init__(f"Línea inválida {line_info}: {razon}")

class GeometricCalculationError(Exception):
    """Excepción para errores en cálculos geométricos"""
    def __init__(self, operacion, razon):
        self.operacion = operacion
        self.razon = razon
        super().__init__(f"Error en cálculo geométrico '{operacion}': {razon}")

class Line:
    """Clase que representa una línea entre dos puntos con validación de excepciones"""
    
    def __init__(self, inicio, final):
        """
        Inicializa una línea con dos puntos
        
        Args:
            inicio: Punto de inicio de la línea
            final: Punto final de la línea
            
        Raises:
            InvalidLineError: Si los puntos no son válidos
            TypeError: Si los argumentos no son Points
        """
        try:
            # Validar que sean objetos Point
            if not isinstance(inicio, Point):
                raise TypeError(f"inicio debe ser un Point, se recibió: {type(inicio).__name__}")
            
            if not isinstance(final, Point):
                raise TypeError(f"final debe ser un Point, se recibió: {type(final).__name__}")
            
            self.inicio = inicio
            self.final = final
            self.length = None  # Se calculará cuando se necesite
            
            # Validar que no sean el mismo punto
            if self.inicio == self.final:
                raise InvalidLineError(
                    f"desde {inicio} hasta {final}", 
                    "los puntos de inicio y final no pueden ser iguales"
                )
                
        except (TypeError, InvalidLineError) as e:
            raise e
        except Exception as e:
            raise InvalidLineError(f"inicialización", f"error inesperado: {e}")
    
    def compute_length(self):
        """
        Calcula la longitud de la línea
        
        Returns:
            float: Longitud de la línea
            
        Raises:
            GeometricCalculationError: Si hay error en el cálculo
        """
        try:
            if self.length is None:
                # Usar el método distance_to del punto
                self.length = self.inicio.distance_to(self.final)
                
                # Validar que la longitud sea positiva
                if self.length <= 0:
                    raise GeometricCalculationError(
                        "cálculo de longitud",
                        f"longitud inválida: {self.length}"
                    )
            
            return self.length
            
        except InvalidPointError as e:
            raise GeometricCalculationError("cálculo de longitud", f"error con puntos: {e}")
        except Exception as e:
            raise GeometricCalculationError("cálculo de longitud", f"error: {e}")
    
    def slope(self):
        """
        Calcula la pendiente de la línea
        
        Returns:
            float: Pendiente de la línea (None si es vertical)
            
        Raises:
            GeometricCalculationError: Si hay error en el cálculo
        """
        try:
            dx = self.final.x - self.inicio.x
            dy = self.final.y - self.inicio.y
            
            # Verificar si es línea vertical
            if abs(dx) < 1e-10:  # Prácticamente cero
                return None  # Línea vertical (pendiente infinita)
            
            return dy / dx
            
        except Exception as e:
            raise GeometricCalculationError("cálculo de pendiente", f"error: {e}")
    
    def angle_with_x_axis(self):
        """
        Calcula el ángulo que forma la línea con el eje X
        
        Returns:
            float: Ángulo en grados
            
        Raises:
            GeometricCalculationError: Si hay error en el cálculo
        """
        try:
            dx = self.final.x - self.inicio.x
            dy = self.final.y - self.inicio.y
            
            # Usar atan2 para obtener el ángulo correcto en todos los cuadrantes
            angle_rad = math.atan2(dy, dx)
            angle_deg = math.degrees(angle_rad)
            
            # Normalizar el ángulo a [0, 360)
            if angle_deg < 0:
                angle_deg += 360
                
            return angle_deg
            
        except Exception as e:
            raise GeometricCalculationError("cálculo de ángulo", f"error: {e}")
    
    def midpoint(self):
        """
        Calcula el punto medio de la línea
        
        Returns:
            Point: Punto medio de la línea
            
        Raises:
            GeometricCalculationError: Si hay error en el cálculo
        """
        try:
            mid_x = (self.inicio.x + self.final.x) / 2
            mid_y = (self.inicio.y + self.final.y) / 2
            
            return Point(mid_x, mid_y)
            
        except InvalidPointError as e:
            raise GeometricCalculationError("cálculo de punto medio", f"error creando punto: {e}")
        except Exception as e:
            raise GeometricCalculationError("cálculo de punto medio", f"error: {e}")
    
    def is_horizontal(self):
        """
        Verifica si la línea es horizontal
        
        Returns:
            bool: True si es horizontal, False en caso contrario
        """
        return abs(self.inicio.y - self.final.y) < 1e-10
    
    def is_vertical(self):
        """
        Verifica si la línea es vertical
        
        Returns:
            bool: True si es vertical, False en caso contrario
        """
        return abs(self.inicio.x - self.final.x) < 1e-10
    
    def range_of_the_line(self, num_points=10):
        """
        Genera una serie de puntos a lo largo de la línea
        
        Args:
            num_points (int): Número de puntos a generar
            
        Returns:
            list: Lista de puntos a lo largo de la línea
            
        Raises:
            GeometricCalculationError: Si hay error en el cálculo
            ValueError: Si num_points no es válido
        """
        try:
            if not isinstance(num_points, int) or num_points < 2:
                raise ValueError(f"num_points debe ser un entero >= 2, se recibió: {num_points}")
            
            points = []
            
            # Calcular incrementos
            dx = (self.final.x - self.inicio.x) / (num_points - 1)
            dy = (self.final.y - self.inicio.y) / (num_points - 1)
            
            # Generar puntos
            for i in range(num_points):
                x = self.inicio.x + i * dx
                y = self.inicio.y + i * dy
                points.append(Point(x, y))
            
            return points
            
        except ValueError as e:
            raise e
        except InvalidPointError as e:
            raise GeometricCalculationError("generación de rango", f"error creando punto: {e}")
        except Exception as e:
            raise GeometricCalculationError("generación de rango", f"error: {e}")
    
    def distance_to_point(self, point):
        """
        Calcula la distancia perpendicular de un punto a la línea
        
        Args:
            point (Point): Punto del cual calcular la distancia
            
        Returns:
            float: Distancia perpendicular del punto a la línea
            
        Raises:
            GeometricCalculationError: Si hay error en el cálculo
            TypeError: Si point no es un Point
        """
        try:
            if not isinstance(point, Point):
                raise TypeError(f"point debe ser un Point, se recibió: {type(point).__name__}")
            
            # Fórmula de distancia punto-línea
            # d = |ax + by + c| / sqrt(a² + b²)
            # donde la línea está en forma ax + by + c = 0
            
            # Convertir la línea a forma ax + by + c = 0
            a = self.final.y - self.inicio.y
            b = self.inicio.x - self.final.x
            c = self.final.x * self.inicio.y - self.inicio.x * self.final.y
            
            # Calcular distancia
            numerator = abs(a * point.x + b * point.y + c)
            denominator = math.sqrt(a**2 + b**2)
            
            if denominator == 0:
                # Los puntos de inicio y final son iguales (no debería pasar por validación)
                raise GeometricCalculationError(
                    "distancia punto-línea", 
                    "línea degenerada (puntos iguales)"
                )
            
            return numerator / denominator
            
        except TypeError as e:
            raise e
        except Exception as e:
            raise GeometricCalculationError("distancia punto-línea", f"error: {e}")
    
    def __str__(self):
        """Representación en cadena de la línea"""
        return f"Line(from {self.inicio} to {self.final})"
    
    def __repr__(self):
        """Representación técnica de la línea"""
        return self.__str__()
    
    def __eq__(self, other):
        """Compara si dos líneas son iguales"""
        if not isinstance(other, Line):
            return False
        return ((self.inicio == other.inicio and self.final == other.final) or
                (self.inicio == other.final and self.final == other.inicio))
