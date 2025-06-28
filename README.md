# Reto 6: Manejo de Excepciones en POO

**Estudiante de POO**

## Descripción

Este reto implementa manejo robusto de excepciones en los ejercicios del Reto 1 y mejora el paquete Shape del Reto 5. Se enfoca en validar entradas de usuario, manejar errores matemáticos y crear código más confiable.

## Archivos Incluidos

### Ejercicios del Reto 1 Mejorados

1. **`Reto_1_Ejercicio_1_con_excepciones.py`**
   - Calculadora básica con manejo de excepciones
   - Valida operaciones matemáticas y división por cero
   - Excepciones: `OperacionInvalida`, `ZeroDivisionError`

2. **`Reto_1_Ejercicio_2_con_excepciones.py`**
   - Verificador de palíndromo con validación
   - Maneja caracteres inválidos y cadenas vacías
   - Excepciones: `StringVacia`, `InputInvalido`

3. **`Reto_1_Ejercicio_3_con_excepciones.py`**
   - Generador de números primos con validación
   - Verifica listas vacías y números inválidos
   - Excepciones: `ListaVaciaError`, `NumeroInvalidoError`

4. **`Reto_1_Ejercicio_4_con_excepciones.py`**
   - Suma mayor de números consecutivos
   - Valida entrada de usuario y elementos insuficientes
   - Excepciones: `ListaVaciaError`, `ElementosInsuficientesError`, `NumeroInvalidoError`

5. **`Reto_1_Ejercicio_5_con_excepciones.py`**
   - Detector de anagramas con validación
   - Maneja palabras inválidas y listas vacías
   - Excepciones: `ListaVaciaError`, `PalabraInvalidaError`, `StringVaciaError`

### Paquete Shape Mejorado

#### `shape_package_mejorado/`

- **`__init__.py`**: Punto de entrada del paquete con todas las excepciones
- **`point_module.py`**: Clase Point con validación de coordenadas
- **`line_module.py`**: Clase Line con validación de puntos y cálculos
- **`shape_module.py`**: Clase base Shape abstracta con validación
- **`rectangle_module.py`**: Clase Rectangle con validación de dimensiones
- **`triangle_module.py`**: Clases Triangle y sus subtipos con validación geométrica

#### Excepciones del Paquete

- `ShapeError`: Excepción base para todas las figuras
- `InvalidPointError`: Para coordenadas inválidas
- `InvalidEdgeError`: Para bordes inválidos
- `InvalidDimensionError`: Para dimensiones incorrectas
- `GeometricCalculationError`: Para errores en cálculos matemáticos
- `TrianguloInvalidoError`: Para triángulos que no cumplen propiedades geométricas

