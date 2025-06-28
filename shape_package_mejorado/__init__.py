"""
Paquete de figuras geometricas mejorado con manejo de excepciones
Estudiante de POO - Reto 6

Este paquete incluye manejo robusto de excepciones para validar datos de entrada
y manejar casos especiales en calculos geometricos.
"""

# Excepciones personalizadas del paquete
class ShapeError(Exception):
    """Excepcion base para errores relacionados con figuras geometricas"""
    pass

class InvalidEdgeError(ShapeError):
    """Excepcion para bordes invalidos"""
    def __init__(self, edge_info, razon):
        self.edge_info = edge_info
        self.razon = razon
        super().__init__(f"Borde invalido {edge_info}: {razon}")

class InvalidPointError(ShapeError):
    """Excepcion para puntos invalidos"""
    def __init__(self, point_info, razon):
        self.point_info = point_info
        self.razon = razon
        super().__init__(f"Punto invalido {point_info}: {razon}")

class InvalidDimensionError(ShapeError):
    """Excepcion para dimensiones invalidas"""
    def __init__(self, dimension, valor):
        self.dimension = dimension
        self.valor = valor
        super().__init__(f"Dimension invalida para {dimension}: {valor}. Debe ser un numero positivo")

class InsufficientDataError(ShapeError):
    """Excepcion para datos insuficientes"""
    def __init__(self, necesarios, recibidos):
        self.necesarios = necesarios
        self.recibidos = recibidos
        super().__init__(f"Datos insuficientes: se necesitan {necesarios}, se recibieron {recibidos}")

class GeometricCalculationError(ShapeError):
    """Excepcion para errores en calculos geometricos"""
    def __init__(self, operacion, razon):
        self.operacion = operacion
        self.razon = razon
        super().__init__(f"Error en calculo geometrico '{operacion}': {razon}")

# Importar todos los modulos
from .point_module import Point
from .line_module import Line  
from .shape_module import Shape
from .rectangle_module import Rectangle
from .triangle_module import Triangle, Scalene, Isosceles, Equilateral

__all__ = [
    'Point', 'Line', 'Shape', 'Rectangle', 'Triangle', 
    'Scalene', 'Isosceles', 'Equilateral',
    'ShapeError', 'InvalidEdgeError', 'InvalidPointError', 
    'InvalidDimensionError', 'InsufficientDataError', 'GeometricCalculationError'
]
