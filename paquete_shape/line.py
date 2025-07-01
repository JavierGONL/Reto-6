import math
from .point import Point, InvalidPointError

class InvalidLineError(Exception):
    def __init__(self, line, razon):
        self.line_info = line
        self.razon = razon
        super().__init__(f"Línea inválida {line}: {razon}")

class GeometricCalculationError(Exception):
    def __init__(self, operacion, razon):
        self.operacion = operacion
        self.razon = razon
        super().__init__(f"Error en cálculo geométrico '{operacion}': {razon}")

class Line:
    def __init__(self, inicio, final):

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
                
        except TypeError as e:
            print(f"Error de tipo: {e}")
            raise
        except InvalidLineError as e:
            print(f"Error de validación: {e}")
            raise
        except Exception as e:
            print(f"Error inesperado: {e}")
            raise InvalidLineError(f"inicialización", f"error inesperado: {e}")
    
    def compute_length(self):
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
            print(f"Error con punto: {e}")
            raise GeometricCalculationError("cálculo de longitud", f"error con puntos: {e}")
        except GeometricCalculationError as e:
            print(f"Error de cálculo: {e}")
            raise
        except Exception as e:
            print(f"Error inesperado: {e}")
            raise GeometricCalculationError("cálculo de longitud", f"error: {e}")
    
    def slope(self):
        try:
            dx = self.final.x - self.inicio.x
            dy = self.final.y - self.inicio.y
            
            # Verificar si es línea vertical
            if abs(dx) < 1e-10:  # Prácticamente cero
                return None  # Línea vertical (pendiente infinita)
            
            return dy / dx
            
        except Exception as e:
            print(f"Error en cálculo de pendiente: {e}")
            raise GeometricCalculationError("cálculo de pendiente", f"error: {e}")
    
    def angle_with_x_axis(self):
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
            print(f"Error en cálculo de ángulo: {e}")
            raise GeometricCalculationError("cálculo de ángulo", f"error: {e}")
    
    def midpoint(self):
        try:
            mid_x = (self.inicio.x + self.final.x) / 2
            mid_y = (self.inicio.y + self.final.y) / 2
            
            return Point(mid_x, mid_y)
            
        except InvalidPointError as e:
            print(f"Error al crear punto medio: {e}")
            raise GeometricCalculationError("cálculo de punto medio", f"error creando punto: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
            raise GeometricCalculationError("cálculo de punto medio", f"error: {e}")
    
    def is_horizontal(self):
        return abs(self.inicio.y - self.final.y) < 1e-10
    
    def is_vertical(self):
        return abs(self.inicio.x - self.final.x) < 1e-10
    
    def range_of_the_line(self, num_points=10):

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
        return f"Line(from {self.inicio} to {self.final})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, Line):
            return False
        return ((self.inicio == other.inicio and self.final == other.final) or
                (self.inicio == other.final and self.final == other.inicio))
