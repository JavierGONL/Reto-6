"""
Ejemplo de uso del paquete shape_package_mejorado con manejo de excepciones
Estudiante de POO - Reto 6

Demuestra como las excepciones ayudan a validar datos y manejar errores.
"""

from shape_package_mejorado import Point, Line, Rectangle, Triangle, ShapeError

def ejemplo_punto():
    print("=== EJEMPLO: PUNTO CON MANEJO DE EXCEPCIONES ===")
    
    # Casos validos
    try:
        p1 = Point(3, 4)
        p2 = Point(-2, 5.5)
        print(f"Puntos creados: {p1}, {p2}")
        print(f"Distancia entre puntos: {p1.distance_to(p2):.2f}")
    except ShapeError as error:
        print(f"Error con puntos: {error}")
    
    # Casos invalidos
    casos_invalidos = [
        ("abc", 4),      # Coordenada no numerica
        (3, float('inf')), # Coordenada infinita
        (2, float('nan')), # Coordenada NaN
    ]
    
    for x, y in casos_invalidos:
        try:
            p = Point(x, y)
            print(f"Punto creado: {p}")
        except ShapeError as error:
            print(f"Error esperado con ({x}, {y}): {error}")

def ejemplo_linea():
    print("\n=== EJEMPLO: LINEA CON MANEJO DE EXCEPCIONES ===")
    
    try:
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        linea = Line(p1, p2)
        print(f"Linea creada: {linea}")
        print(f"Longitud: {linea.compute_length():.2f}")
        print(f"Punto medio: {linea.midpoint()}")
    except ShapeError as error:
        print(f"Error con linea: {error}")
    
    # Caso invalido: mismos puntos
    try:
        p_same = Point(1, 1)
        linea_invalida = Line(p_same, p_same)
    except ShapeError as error:
        print(f"Error esperado con puntos iguales: {error}")

def ejemplo_rectangulo():
    print("\n=== EJEMPLO: RECTANGULO CON MANEJO DE EXCEPCIONES ===")
    
    # Rectangulo valido
    try:
        rect = Rectangle(width=5, height=3, bottom_left=Point(0, 0))
        print(f"Rectangulo creado: {rect}")
        print(f"Area: {rect.compute_area()}")
        print(f"Perimetro: {rect.compute_perimeter()}")
        print(f"Centro: {rect.compute_center()}")
    except ShapeError as error:
        print(f"Error con rectangulo: {error}")
    
    # Casos invalidos
    casos_invalidos = [
        (-5, 3),    # Ancho negativo
        (5, 0),     # Alto cero
        ("abc", 3), # Ancho no numerico
    ]
    
    for width, height in casos_invalidos:
        try:
            rect = Rectangle(width=width, height=height)
            print(f"Rectangulo creado: {rect}")
        except ShapeError as error:
            print(f"Error esperado con width={width}, height={height}: {error}")

def ejemplo_triangulo():
    print("\n=== EJEMPLO: TRIANGULO CON MANEJO DE EXCEPCIONES ===")
    
    try:
        # Crear puntos del triangulo
        p1 = Point(0, 0)
        p2 = Point(3, 0) 
        p3 = Point(1.5, 2.6)  # Triangulo aproximadamente equilatero
        
        # Crear bordes
        edge1 = Line(p1, p2)
        edge2 = Line(p2, p3)
        edge3 = Line(p3, p1)
        
        triangulo = Triangle([edge1, edge2, edge3])
        print(f"Triangulo creado con {len(triangulo.edges)} bordes")
        print(f"Perimetro: {triangulo.compute_perimeter():.2f}")
        print(f"Area: {triangulo.compute_area():.2f}")
        print(f"Angulos internos: {triangulo.compute_inner_angles()}")
        
    except ShapeError as error:
        print(f"Error con triangulo: {error}")
    
    # Triangulo invalido (no cumple desigualdad triangular)
    try:
        p1 = Point(0, 0)
        p2 = Point(1, 0)
        p3 = Point(10, 0)  # Puntos colineales
        
        edge1 = Line(p1, p2)
        edge2 = Line(p2, p3)
        edge3 = Line(p3, p1)
        
        triangulo_invalido = Triangle([edge1, edge2, edge3])
        area = triangulo_invalido.compute_area()
        print(f"Area: {area}")
        
    except ShapeError as error:
        print(f"Error esperado con triangulo degenerado: {error}")

def ejemplo_interseccion_rectangulos():
    print("\n=== EJEMPLO: INTERSECCION DE RECTANGULOS ===")
    
    try:
        rect1 = Rectangle(width=4, height=3, bottom_left=Point(0, 0))
        rect2 = Rectangle(width=3, height=4, bottom_left=Point(2, 1))
        
        print(f"Rectangulo 1: {rect1}")
        print(f"Rectangulo 2: {rect2}")
        
        if rect1.intersects_with_rectangle(rect2):
            print("✅ Los rectangulos se intersectan")
        else:
            print("❌ Los rectangulos NO se intersectan")
            
    except ShapeError as error:
        print(f"Error en interseccion: {error}")

if __name__ == "__main__":
    print("DEMOSTRACION DEL PAQUETE SHAPE CON MANEJO DE EXCEPCIONES")
    print("=" * 60)
    
    try:
        ejemplo_punto()
        ejemplo_linea()
        ejemplo_rectangulo()
        ejemplo_triangulo() 
        ejemplo_interseccion_rectangulos()
        
        print("\n" + "=" * 60)
        print("✅ Demostracion completada exitosamente")
        
    except Exception as error:
        print(f"\n❌ Error general en la demostracion: {error}")
        print("El manejo de excepciones permite detectar y manejar errores de forma controlada")
