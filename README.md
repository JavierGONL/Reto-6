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

### Archivo de Demostración

- **`ejemplo_uso_paquete_mejorado.py`**: Demuestra el uso del paquete con casos válidos e inválidos

## Casos de Uso de Excepciones

### 1. Validación de Entrada de Usuario
- Números inválidos (letras, símbolos)
- Cadenas vacías
- Operaciones matemáticas incorrectas

### 2. Errores Matemáticos
- División por cero
- Raíces cuadradas de números negativos
- Coordenadas infinitas o NaN

### 3. Errores Geométricos
- Triángulos que no cumplen la desigualdad triangular
- Dimensiones negativas o cero
- Puntos coincidentes en líneas

### 4. Datos Insuficientes
- Listas vacías cuando se necesitan elementos
- Menos elementos de los requeridos para cálculos

## Características Implementadas

### Estilo de Código
- Clases de excepción simples y directas
- Mensajes de error claros en español
- Manejo de excepciones en bloques try-catch específicos
- Validación preventiva de datos

### Mejoras en Usabilidad
- Mensajes de error informativos
- Casos de prueba incluidos
- Ejemplos de uso con datos válidos e inválidos
- Documentación clara de cada excepción

### Robustez
- Validación de tipos de datos
- Manejo de casos extremos (infinito, NaN)
- Prevención de errores matemáticos
- Validación de propiedades geométricas

## Cómo Ejecutar

### Ejercicios Individuales
```bash
python Reto_1_Ejercicio_1_con_excepciones.py
python Reto_1_Ejercicio_2_con_excepciones.py
python Reto_1_Ejercicio_3_con_excepciones.py
python Reto_1_Ejercicio_4_con_excepciones.py
python Reto_1_Ejercicio_5_con_excepciones.py
```

### Demostración del Paquete Shape
```bash
python ejemplo_uso_paquete_mejorado.py
```

## Lecciones Aprendidas

1. **Excepciones Personalizadas**: Permiten crear mensajes de error específicos y manejar casos particulares del dominio.

2. **Validación Preventiva**: Es mejor validar datos antes de procesarlos que manejar errores después.

3. **Mensajes Claros**: Los mensajes de error deben ser informativos para ayudar al usuario a corregir el problema.

4. **Jerarquía de Excepciones**: Una excepción base permite manejar todos los errores relacionados de manera uniforme.

5. **Casos de Prueba**: Incluir casos que fallan ayuda a demostrar que el manejo de excepciones funciona correctamente.

## Beneficios del Manejo de Excepciones

- **Código más robusto**: No se crashea con entradas inesperadas
- **Mejor experiencia de usuario**: Mensajes de error claros
- **Debugging más fácil**: Errores específicos facilitan encontrar problemas
- **Validación centralizada**: Las excepciones permiten validar datos en un solo lugar
- **Código más limpio**: Separa la lógica normal del manejo de errores
