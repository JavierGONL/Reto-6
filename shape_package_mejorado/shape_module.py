"""
Módulo Shape mejorado - Clase base para todas las figuras geométricas con manejo de excepciones
Estudiante de POO - Reto 6

Incluye validación de bordes y métodos base con manejo de errores.
"""

import abc
from typing import List, Optional

class ShapeError(Exception):
    """Excepción base para errores relacionados con figuras geométricas"""
    pass

class InvalidEdgeError(ShapeError):
    """Excepción para bordes inválidos"""
    def __init__(self, edge_info, razon):
        self.edge_info = edge_info
        self.razon = razon
        super().__init__(f"Borde inválido {edge_info}: {razon}")

class InsufficientDataError(ShapeError):
    """Excepción para datos insuficientes"""
    def __init__(self, necesarios, recibidos):
        self.necesarios = necesarios
        self.recibidos = recibidos
        super().__init__(f"Datos insuficientes: se necesitan {necesarios}, se recibieron {recibidos}")

class GeometricCalculationError(ShapeError):
    """Excepción para errores en cálculos geométricos"""
    def __init__(self, operacion, razon):
        self.operacion = operacion
        self.razon = razon
        super().__init__(f"Error en cálculo geométrico '{operacion}': {razon}")

class Shape(abc.ABC):
    """Clase base abstracta para todas las figuras geométricas con manejo de excepciones"""
    
    def __init__(self, edges: Optional[List] = None):
        """
        Inicializa una figura geométrica
        
        Args:
            edges (list, optional): Lista de bordes de la figura
            
        Raises:
            TypeError: Si edges no es una lista o None
            InvalidEdgeError: Si algún borde no es válido
        """
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
            
        except (TypeError, InvalidEdgeError) as e:
            raise e
        except Exception as e:
            raise ShapeError(f"Error al inicializar figura: {e}")
    
    def _validar_bordes(self, edges):
        """
        Valida una lista de bordes
        
        Args:
            edges (list): Lista de bordes a validar
            
        Returns:
            list: Lista de bordes validados
            
        Raises:
            InvalidEdgeError: Si algún borde no es válido
        """
        try:
            if not isinstance(edges, list):
                raise InvalidEdgeError("lista de bordes", "debe ser una lista")
            
            bordes_validados = []
            
            for i, edge in enumerate(edges):
                # Verificar que el borde tenga los métodos necesarios
                if not hasattr(edge, 'compute_length'):
                    raise InvalidEdgeError(
                        f"borde {i}", 
                        "debe tener el método compute_length"
                    )
                
                # Verificar que el borde tenga puntos de inicio y fin
                if not (hasattr(edge, 'inicio') and hasattr(edge, 'final')):
                    raise InvalidEdgeError(
                        f"borde {i}", 
                        "debe tener atributos 'inicio' y 'final'"
                    )
                
                bordes_validados.append(edge)
            
            return bordes_validados
            
        except InvalidEdgeError as e:
            raise e
        except Exception as e:
            raise InvalidEdgeError("validación de bordes", f"error inesperado: {e}")
    
    def add_edge(self, edge):
        """
        Agrega un borde a la figura
        
        Args:
            edge: Borde a agregar
            
        Raises:
            InvalidEdgeError: Si el borde no es válido
        """
        try:
            # Validar el borde individual
            bordes_validados = self._validar_bordes([edge])
            self.edges.append(bordes_validados[0])
            
            # Resetear flags de cálculos
            self._area_calculated = False
            self._perimeter_calculated = False
            self._angles_calculated = False
            
        except InvalidEdgeError as e:
            raise e
        except Exception as e:
            raise InvalidEdgeError("agregar borde", f"error: {e}")
    
    def get_edge_count(self):
        """
        Obtiene el número de bordes de la figura
        
        Returns:
            int: Número de bordes
        """
        return len(self.edges)
    
    def is_valid_shape(self):
        """
        Verifica si la figura tiene suficientes bordes para ser válida
        
        Returns:
            bool: True si es válida, False en caso contrario
        """
        return len(self.edges) >= 3  # Mínimo para un polígono
    
    @abc.abstractmethod
    def compute_area(self) -> float:
        """
        Método abstracto para calcular el área
        Debe ser implementado por las subclases
        
        Returns:
            float: Área de la figura
        
        Raises:
            NotImplementedError: Si no es implementado por la subclase
        """
        pass

    @abc.abstractmethod
    def compute_perimeter(self) -> float:
        """
        Método abstracto para calcular el perímetro
        Debe ser implementado por las subclases
        
        Returns:
            float: Perímetro de la figura
        
        Raises:
            NotImplementedError: Si no es implementado por la subclase
        """
        pass

    @abc.abstractmethod
    def compute_inner_angles(self) -> list:
        """
        Método abstracto para calcular los ángulos internos
        Debe ser implementado por las subclases
        
        Returns:
            list: Lista de ángulos internos
        
        Raises:
            NotImplementedError: Si no es implementado por la subclase
        """
        pass
    
    def validate_for_calculation(self, operation_name):
        """
        Valida que la figura esté lista para cálculos geométricos
        
        Args:
            operation_name (str): Nombre de la operación a realizar
            
        Raises:
            InsufficientDataError: Si no hay suficientes datos
            GeometricCalculationError: Si la figura no es válida para cálculos
        """
        try:
            if not self.edges:
                raise InsufficientDataError("al menos 1 borde", "0")
            
            if not self.is_valid_shape():
                raise GeometricCalculationError(
                    operation_name, 
                    f"se necesitan al menos 3 bordes, se tienen {len(self.edges)}"
                )
            
            # Validar que todos los bordes tengan longitud calculada
            for i, edge in enumerate(self.edges):
                try:
                    if not hasattr(edge, 'length') or edge.length <= 0:
                        edge.compute_length()
                        if not hasattr(edge, 'length') or edge.length <= 0:
                            raise GeometricCalculationError(
                                operation_name,
                                f"borde {i} no tiene longitud válida"
                            )
                except Exception as e:
                    raise GeometricCalculationError(
                        operation_name,
                        f"error al calcular longitud del borde {i}: {e}"
                    )
            
        except (InsufficientDataError, GeometricCalculationError) as e:
            raise e
        except Exception as e:
            raise GeometricCalculationError(operation_name, f"error de validación: {e}")
    
    def __str__(self):
        """Representación en cadena de la figura"""
        return f"{self.__class__.__name__}(edges={len(self.edges)})"
    
    def __repr__(self):
        """Representación técnica de la figura"""
        return self.__str__()
