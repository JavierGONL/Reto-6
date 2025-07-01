# Módulo Shape mejorado - Clase base para todas las figuras geométricas con manejo de excepciones
# Estudiante de POO - Reto 6

# Incluye validación de bordes y métodos base con manejo de errores.

from typing import List, Optional

class ShapeError(Exception):
    pass

class InvalidEdgeError(ShapeError):
    def __init__(self, edge_info, razon):
        self.edge_info = edge_info
        self.razon = razon
        super().__init__(f"Borde inválido {edge_info}: {razon}")

class InsufficientDataError(ShapeError):
    def __init__(self, necesarios, recibidos):
        self.necesarios = necesarios
        self.recibidos = recibidos
        super().__init__(f"Datos insuficientes: se necesitan {necesarios}, se recibieron {recibidos}")

class GeometricCalculationError(ShapeError):
    def __init__(self, operacion, razon):
        self.operacion = operacion
        self.razon = razon
        super().__init__(f"Error en cálculo geométrico '{operacion}': {razon}")

class Shape:
    def __init__(self, edges: Optional[List] = None):
        try:
            if edges is None:
                self.edges = []
            elif isinstance(edges, list):
                self.edges = self._validar_bordes(edges)
            else:
                raise TypeError(f"edges debe ser una lista o None, se recibió: {type(edges).__name__}")
            self.inner_angles = []
            self._area_calculated = False
            self._perimeter_calculated = False
            self._angles_calculated = False
        except (TypeError, InvalidEdgeError) as error:
            raise error
        except Exception as error:
            raise ShapeError(f"Error al inicializar figura: {error}")

    def _validar_bordes(self, edges):
        try:
            if not isinstance(edges, list):
                raise InvalidEdgeError("lista de bordes", "debe ser una lista")
            bordes_validados = []
            for i, edge in enumerate(edges):
                if not hasattr(edge, 'compute_length'):
                    raise InvalidEdgeError(f"borde {i}", "debe tener el método compute_length")
                if not (hasattr(edge, 'inicio') and hasattr(edge, 'final')):
                    raise InvalidEdgeError(f"borde {i}", "debe tener atributos 'inicio' y 'final'")
                bordes_validados.append(edge)
            return bordes_validados
        except InvalidEdgeError as error:
            raise error
        except Exception as error:
            raise InvalidEdgeError("validación de bordes", f"error inesperado: {error}")

    def add_edge(self, edge):
        try:
            bordes_validados = self._validar_bordes([edge])
            self.edges.append(bordes_validados[0])
            self._area_calculated = False
            self._perimeter_calculated = False
            self._angles_calculated = False
        except InvalidEdgeError as error:
            raise error
        except Exception as error:
            raise InvalidEdgeError("agregar borde", f"error: {error}")

    def get_edge_count(self):
        return len(self.edges)

    def is_valid_shape(self):
        return len(self.edges) >= 3

    def compute_area(self) -> float:
        pass

    def compute_perimeter(self) -> float:
        pass

    def compute_inner_angles(self) -> list:
        pass

    def validate_for_calculation(self, operation_name):
        try:
            if not self.edges:
                raise InsufficientDataError("al menos 1 borde", "0")
            if not self.is_valid_shape():
                raise GeometricCalculationError(
                    operation_name,
                    f"se necesitan al menos 3 bordes, se tienen {len(self.edges)}"
                )
            for i, edge in enumerate(self.edges):
                try:
                    if not hasattr(edge, 'length') or edge.length <= 0:
                        edge.compute_length()
                        if not hasattr(edge, 'length') or edge.length <= 0:
                            raise GeometricCalculationError(
                                operation_name,
                                f"borde {i} no tiene longitud válida"
                            )
                except Exception as error:
                    raise GeometricCalculationError(
                        operation_name,
                        f"error al calcular longitud del borde {i}: {error}"
                    )
        except (InsufficientDataError, GeometricCalculationError) as error:
            raise error
        except Exception as error:
            raise GeometricCalculationError(operation_name, f"error de validación: {error}")

    def __str__(self):
        return f"{self.__class__.__name__}(edges={len(self.edges)})"
