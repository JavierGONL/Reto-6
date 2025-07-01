class ShapeError(Exception):
    pass

class InvalidEdgeError(ShapeError):
    pass

class InsufficientDataError(ShapeError):
    pass

class GeometricCalculationError(ShapeError):
    pass

class Shape:
    def __init__(self, edges: list = []):
        self.edges = edges
        self.inner_angles = []

    def compute_area(self):
        raise ShapeError("Metodo no implementado")

    def compute_perimeter(self):
        raise ShapeError("Metodo no implementado")

    def compute_inner_angles(self):
        raise ShapeError("Metodo no implementado")

    def __str__(self):
        return f"{self.__class__.__name__}(edges={len(self.edges)})"
