class ListaVaciaError(Exception):
    def __init__(self):
        super().__init__("No se puede procesar una lista vacia")

class ElementosInsuficientesError(Exception):
    def __init__(self, cantidad):
        self.cantidad = cantidad
        super().__init__(f"Se necesitan al menos 2 elementos. Se recibieron: {cantidad}")

class NumeroInvalidoError(Exception):
    def __init__(self, valor):
        self.valor = valor
        super().__init__(f"Valor invalido: '{valor}'. Solo se permiten numeros")

class SalidaUsuarioError(Exception):
    def __init__(self):
        super().__init__("Usuario decidio salir del programa")

def validar_numero(entrada):
    try:
        # Verificar comando de salida
        if entrada == "0":
            raise SalidaUsuarioError()
        
        # Verificar entrada vacía
        if not entrada or entrada.isspace():
            raise NumeroInvalidoError("entrada vacia")
        
        # Intentar convertir a número
        numero = float(entrada)
        return numero
        
    except ValueError:
        raise NumeroInvalidoError(entrada)

def obtener_numeros_usuario():
    lista = []
    print("Ingrese numeros uno por uno (digite 0 para terminar):")
    
    while True:
        try:
            entrada = input("Digite un numero: ")
            numero = validar_numero(entrada)
            lista.append(numero)
            print(f"Numero {numero} agregado. Total: {len(lista)} numeros")
            
        except SalidaUsuarioError:
            if not lista:
                raise ListaVaciaError()
            print(f"Entrada terminada. Se ingresaron {len(lista)} numeros.")
            break
            
        except NumeroInvalidoError as error:
            print(f"Error: {error}")
            print("Por favor, ingrese un numero valido o 0 para salir.")

    return lista

def suma_mayor_dos_numeros_consecutivos(lista=None):
    try:
        # Si no se proporciona lista, obtenerla del usuario
        if lista is None:
            lista = obtener_numeros_usuario()
        
        # Validar tipo de entrada
        if not isinstance(lista, list):
            raise TypeError(f"Se esperaba una lista, se recibio: {type(lista).__name__}")
        
        # Validar que no esté vacía
        if not lista:
            raise ListaVaciaError()
        
        # Validar que tenga al menos 2 elementos
        if len(lista) < 2:
            raise ElementosInsuficientesError(len(lista))
        
        # Validar que todos los elementos sean números
        for i, elemento in enumerate(lista):
            try:
                lista[i] = float(elemento)
            except (ValueError, TypeError):
                raise NumeroInvalidoError(elemento)
        
        # Encontrar la suma mayor entre números consecutivos
        suma_mayor = float('-inf')
        mejor_indice = 0
        
        for i in range(len(lista) - 1):
            suma_actual = lista[i] + lista[i + 1]
            if suma_actual > suma_mayor:
                suma_mayor = suma_actual
                mejor_indice = i
        
        return suma_mayor, mejor_indice, lista[mejor_indice], lista[mejor_indice + 1]
        
    except (TypeError, ListaVaciaError, ElementosInsuficientesError, NumeroInvalidoError) as error:
        print(f"Error de validacion: {error}")
        raise

if __name__ == "__main__":
    try:
        # Ejemplo con lista predefinida
        lista_demo = [1, -5, 8, 3, -2, 10, 4, -1, 6]
        print(f"Lista de prueba: {lista_demo}")
        
        suma, indice, num1, num2 = suma_mayor_dos_numeros_consecutivos(lista_demo)
        print(f"Suma mayor: {suma}")
        print(f"Numeros consecutivos: {num1} + {num2} (posiciones {indice} y {indice+1})")
        
    except Exception as error:
        print(f"Ocurrio un error: {error}")
