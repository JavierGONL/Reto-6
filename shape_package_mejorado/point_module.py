"""
Módulo Point mejorado - Representa un punto en un plano cartesiano con manejo de excepciones
Estudiante de POO - Reto 6

Incluye validación de coordenadas y manejo de casos especiales.
"""

import math

class InvalidPointError(Exception):
    """Excepción para puntos inválidos"""
    def __init__(self, point_info, razon):
        self.point_info = point_info
        self.razon = razon
        super().__init__(f"Punto inválido {point_info}: {razon}")

class Point:
    """Clase que representa un punto en un plano cartesiano con validación de excepciones"""
    
    def __init__(self, x, y):
        """
        Inicializa un punto con coordenadas x e y
        
        Args:
            x: Coordenada x del punto
            y: Coordenada y del punto
            
        Raises:
            InvalidPointError: Si las coordenadas no son números válidos
            TypeError: Si las coordenadas no son del tipo correcto
        """
        try:
            # Validar y convertir coordenadas
            self.x = self._validar_coordenada(x, "x")
            self.y = self._validar_coordenada(y, "y")
            
        except Exception as e:
            if isinstance(e, InvalidPointError):
                raise
            raise InvalidPointError(f"({x}, {y})", f"error al inicializar: {e}")
    
    def _validar_coordenada(self, valor, nombre_coord):
        """
        Valida una coordenada individual
        
        Args:
            valor: Valor de la coordenada
            nombre_coord (str): Nombre de la coordenada (x o y)
            
        Returns:
            float: Coordenada válida
            
        Raises:
            InvalidPointError: Si la coordenada no es válida
        """
        try:
            # Intentar convertir a número
            coordenada = float(valor)
            
            # Verificar que no sea infinito o NaN
            if math.isinf(coordenada):
                raise InvalidPointError(
                    f"coordenada {nombre_coord}={valor}", 
                    "no puede ser infinito"
                )
            
            if math.isnan(coordenada):
                raise InvalidPointError(
                    f"coordenada {nombre_coord}={valor}", 
                    "no puede ser NaN (Not a Number)"
                )
            
            return coordenada
            
        except ValueError:
            raise InvalidPointError(
                f"coordenada {nombre_coord}={valor}", 
                "debe ser un número válido"
            )
        except TypeError:
            raise InvalidPointError(
                f"coordenada {nombre_coord}={valor}", 
                f"tipo inválido: {type(valor).__name__}"
            )

    def another_point(self, new_x, new_y):
        """
        Método para crear un nuevo punto a partir de coordenadas dadas
        
        Args:
            new_x: Nueva coordenada x
            new_y: Nueva coordenada y
            
        Returns:
            Point: Nuevo punto con las coordenadas especificadas
            
        Raises:
            InvalidPointError: Si las nuevas coordenadas no son válidas
        """
        try:
            return Point(new_x, new_y)
        except InvalidPointError as e:
            raise InvalidPointError(
                f"nuevo punto ({new_x}, {new_y})", 
                f"error al crear: {e.razon}"
            )
    
    def distance_to(self, other_point):
        """
        Calcula la distancia euclidiana a otro punto
        
        Args:
            other_point (Point): Otro punto
            
        Returns:
            float: Distancia entre los puntos
            
        Raises:
            InvalidPointError: Si el otro punto no es válido
            TypeError: Si other_point no es un Point
        """
        try:
            if not isinstance(other_point, Point):
                raise TypeError(f"Se esperaba un Point, se recibió: {type(other_point).__name__}")
            
            dx = self.x - other_point.x
            dy = self.y - other_point.y
            distance = math.sqrt(dx**2 + dy**2)
            
            return distance
            
        except TypeError as e:
            raise e
        except Exception as e:
            raise InvalidPointError(
                f"cálculo de distancia entre {self} y {other_point}", 
                f"error: {e}"
            )
    
    def move(self, dx, dy):
        """
        Mueve el punto por un desplazamiento dado
        
        Args:
            dx: Desplazamiento en x
            dy: Desplazamiento en y
            
        Raises:
            InvalidPointError: Si los desplazamientos no son válidos
        """
        try:
            new_x = self.x + float(dx)
            new_y = self.y + float(dy)
            
            # Validar las nuevas coordenadas
            self.x = self._validar_coordenada(new_x, "x")
            self.y = self._validar_coordenada(new_y, "y")
            
        except ValueError:
            raise InvalidPointError(
                f"desplazamiento ({dx}, {dy})", 
                "los desplazamientos deben ser números válidos"
            )
        except InvalidPointError as e:
            raise e
        except Exception as e:
            raise InvalidPointError(
                f"movimiento del punto {self}", 
                f"error: {e}"
            )
    
    def is_origin(self):
        """
        Verifica si el punto es el origen (0, 0)
        
        Returns:
            bool: True si es el origen, False en caso contrario
        """
        return self.x == 0 and self.y == 0
    
    def quadrant(self):
        """
        Determina el cuadrante en el que se encuentra el punto
        
        Returns:
            int: Número del cuadrante (1-4) o 0 si está en los ejes
        """
        if self.x > 0 and self.y > 0:
            return 1
        elif self.x < 0 and self.y > 0:
            return 2
        elif self.x < 0 and self.y < 0:
            return 3
        elif self.x > 0 and self.y < 0:
            return 4
        else:
            return 0  # En los ejes o en el origen
    
    def __str__(self):
        """Representación en cadena del punto"""
        return f"Point({self.x}, {self.y})"
    
    def __repr__(self):
        """Representación técnica del punto"""
        return self.__str__()
    
    def __eq__(self, other):
        """Compara si dos puntos son iguales"""
        if not isinstance(other, Point):
            return False
        return abs(self.x - other.x) < 1e-10 and abs(self.y - other.y) < 1e-10
    
    def __hash__(self):
        """Hash del punto para usar en sets y diccionarios"""
        return hash((round(self.x, 10), round(self.y, 10)))
