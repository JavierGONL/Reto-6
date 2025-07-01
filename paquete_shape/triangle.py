import math
from .shape import Shape, ShapeError, GeometricCalculationError
from .line import Line

class TrianguloInvalidoError(ShapeError):
    def __init__(self, razon):
        self.razon = razon
        super().__init__(f"Triangulo invalido: {razon}")

class Triangle(Shape): 
    def __init__(self, edges=None):
        super().__init__(edges)
        self.edges = edges if edges is not None else []
        self.perimeter = 0
        self._area = 0
        self.angulos = []
    
    def compute_perimeter(self):
        try:
            if self.perimeter == 0:
                for i in range(len(self.edges)):
                    self.edges[i].compute_length()
                    self.perimeter += self.edges[i].length
            return self.perimeter
        except Exception as error:
            raise GeometricCalculationError("calculo de perimetro", f"error: {error}")

    def compute_area(self):
        try:
            if len(self.edges) != 3:
                raise TrianguloInvalidoError("debe tener exactamente 3 lados")
                
            if self.perimeter == 0:
                self.compute_perimeter()
            
            semiperimetro = self.perimeter/2
            a = self.edges[0].length
            b = self.edges[1].length  
            c = self.edges[2].length
            
            # Verificar desigualdad triangular
            if (a + b <= c) or (a + c <= b) or (b + c <= a):
                raise TrianguloInvalidoError("no cumple la desigualdad triangular")
            
            # Formula de Heron
            area_squared = semiperimetro * (semiperimetro-a) * (semiperimetro-b) * (semiperimetro-c)
            if area_squared < 0:
                raise TrianguloInvalidoError("area negativa en formula de Heron")
                
            self.area = round(math.sqrt(area_squared), 3)
            return self.area
            
        except TrianguloInvalidoError as error:
            raise error
        except Exception as error:
            raise GeometricCalculationError("calculo de area", f"error: {error}")

    def compute_inner_angles(self):
        try:
            if len(self.edges) != 3:
                raise TrianguloInvalidoError("debe tener exactamente 3 lados")
                
            angulos = []
            for i in range(len(self.edges)):
                self.edges[i].compute_length() 
            
            # Ley de cosenos para cada angulo
            for i in range(len(self.edges)):
                a = self.edges[i].length  # Lado opuesto al angulo
                b = self.edges[i-1].length  # Lado adyacente 1
                c = self.edges[i-2].length  # Lado adyacente 2
                
                # cos(angulo) = (b² + c² - a²) / (2bc)
                cos_angulo = (b**2 + c**2 - a**2) / (2 * b * c)
                
                # Asegurar rango valido para acos
                cos_angulo = max(-1, min(1, cos_angulo))
                
                angulo_rad = math.acos(cos_angulo)
                angulo_deg = math.degrees(angulo_rad)
                angulos.append(round(angulo_deg, 2))
            
            self.inner_angles = angulos
            return self.inner_angles
            
        except TrianguloInvalidoError as error:
            raise error
        except Exception as error:
            raise GeometricCalculationError("calculo de angulos internos", f"error: {error}")

class Scalene(Triangle):
    def __init__(self, edges=None):
        super().__init__(edges)
    
    def is_scalene(self):
        try:
            if len(self.edges) != 3:
                return False
                
            for edge in self.edges:
                edge.compute_length()
            
            a, b, c = [edge.length for edge in self.edges]
            return a != b and b != c and a != c
            
        except Exception:
            return False

class Isosceles(Triangle):
    def __init__(self, edges=None):
        super().__init__(edges)
    
    def is_isosceles(self):
        try:
            if len(self.edges) != 3:
                return False
                
            for edge in self.edges:
                edge.compute_length()
            
            a, b, c = [edge.length for edge in self.edges]
            return (a == b and a != c) or (b == c and b != a) or (a == c and a != b)
            
        except Exception:
            return False

class Equilateral(Triangle):
    def __init__(self, edges=None):
        super().__init__(edges)
    
    def is_equilateral(self):
        try:
            if len(self.edges) != 3:
                return False
                
            for edge in self.edges:
                edge.compute_length()
            
            a, b, c = [edge.length for edge in self.edges]
            tolerance = 1e-10
            return abs(a - b) < tolerance and abs(b - c) < tolerance
            
        except Exception:
            return False
