import math

class InvalidPointError(Exception):
    def __init__(self, point_info, razon):
        self.point_info = point_info
        self.razon = razon
        super().__init__(f"Punto invalido {point_info}: {razon}")

class CoordenadaInvalidaError(Exception):
    def __init__(self, valor, nombre_coord):
        self.valor = valor
        self.nombre_coord = nombre_coord
        super().__init__(f"Coordenada {nombre_coord} invalida: {valor}")

class OperacionInvalidaError(Exception):
    def __init__(self, operacion, razon):
        self.operacion = operacion
        self.razon = razon
        super().__init__(f"Operacion invalida '{operacion}': {razon}")

def validar_coordenada(valor, nombre_coord):
    try:
        # Verificar que no sea None
        if valor is None:
            raise CoordenadaInvalidaError(valor, nombre_coord)
        
        # Intentar convertir a número
        coordenada = float(valor)
        
        # Verificar que no sea infinito o NaN
        if math.isinf(coordenada):
            raise CoordenadaInvalidaError(valor, f"{nombre_coord} (infinito)")
        
        if math.isnan(coordenada):
            raise CoordenadaInvalidaError(valor, f"{nombre_coord} (NaN)")
        
        return coordenada
        
    except ValueError:
        raise CoordenadaInvalidaError(valor, nombre_coord)
    except TypeError:
        raise CoordenadaInvalidaError(valor, f"{nombre_coord} (tipo: {type(valor).__name__})")

class Point:
    def __init__(self, x, y):
        try:
            # Validar y convertir coordenadas
            self.x = validar_coordenada(x, "x")
            self.y = validar_coordenada(y, "y")
            
        except CoordenadaInvalidaError as e:
            print(f"Error de validacion: {e}")
            raise InvalidPointError(f"({x}, {y})", str(e))
        except Exception as e:
            print(f"Error inesperado: {e}")
            raise InvalidPointError(f"({x}, {y})", f"error al inicializar: {e}")
    
    def another_point(self, new_x, new_y):
        try:
            return Point(new_x, new_y)
        except InvalidPointError as e:
            print(f"Error de validacion: {e}")
            raise
        except Exception as e:
            raise InvalidPointError(f"nuevo punto ({new_x}, {new_y})", f"error inesperado: {e}")
    
    def distance_to(self, other_point):
        try:
            if not isinstance(other_point, Point):
                raise OperacionInvalidaError(
                    "calculo de distancia", 
                    f"se esperaba Point, se recibio: {type(other_point).__name__}"
                )
            dx = self.x - other_point.x
            dy = self.y - other_point.y
            distance = math.sqrt(dx**2 + dy**2)
            return distance
            
        except OperacionInvalidaError as e:
            print(f"Error de validacion: {e}")
            raise
        except Exception as e:
            raise OperacionInvalidaError(
                "calculo de distancia", 
                f"error inesperado: {e}"
            )
    
    def move(self, dx, dy):
        try:
            # Validar desplazamientos
            delta_x = validar_coordenada(dx, "dx")
            delta_y = validar_coordenada(dy, "dy")
            
            # Calcular nuevas coordenadas
            new_x = self.x + delta_x
            new_y = self.y + delta_y
            
            # Validar que las nuevas coordenadas sean válidas
            self.x = validar_coordenada(new_x, "x")
            self.y = validar_coordenada(new_y, "y")
            
        except CoordenadaInvalidaError as e:
            print(f"Error de validacion: {e}")
            raise InvalidPointError(f"movimiento ({dx}, {dy})", str(e))
        except Exception as e:
            raise InvalidPointError(f"movimiento del punto {self}", f"error inesperado: {e}")
    
    def is_origin(self):
        return self.x == 0 and self.y == 0
    
    def quadrant(self):
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
        return f"Point({self.x}, {self.y})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return abs(self.x - other.x) < 1e-10 and abs(self.y - other.y) < 1e-10
    
    def __hash__(self):
        return hash((round(self.x, 10), round(self.y, 10)))

def obtener_punto_usuario():
    while True:
        try:
            entrada = input("Ingrese las coordenadas del punto (x,y): ")
            
            if not entrada.strip():
                raise InvalidPointError("entrada vacia", "debe ingresar coordenadas")
            
            # Separar coordenadas
            coordenadas = entrada.split(',')
            if len(coordenadas) != 2:
                raise InvalidPointError(entrada, "formato invalido, use: x,y")
            
            x_str, y_str = coordenadas
            return Point(x_str.strip(), y_str.strip())
            
        except InvalidPointError as error:
            print(f"Error: {error}")
            print("Use el formato: x,y (ejemplo: 3.5,-2)")
        except KeyboardInterrupt:
            print("\nOperacion cancelada por el usuario.")
            raise