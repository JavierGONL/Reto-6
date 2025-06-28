class StringVacia(Exception):
    def __init__(self):
        super().__init__("cadena vacia")

class InputInvalido(Exception):
    def __init__(self, input):
        self.Input = input
        super().__init__(f"letra invalida detectado: '{input}'.")

def validar_entrada(palabra):

    if not palabra or palabra.isspace():
        raise StringVacia()
    
    # Verificar que solo contenga letras (permitir espacios para frases)
    for letra in palabra:
        if not letra.isalpha() and not letra.isspace():
            raise InputInvalido(letra)

def palindromo(palabra):
    try:
        # Validar tipo de entrada
        if not isinstance(palabra, str):
            raise TypeError(f"Se esperaba una cadena, se recibio: {type(palabra).__name__}")
        
        # Validar contenido de la entrada
        validar_entrada(palabra)
        
        # volver minuscula las palabras
        palabra_en_minuscula = palabra.replace(" ", "").lower()
        
        # Construir palabra invertida
        palabra_invertida = ""
        for i in range(len(palabra_en_minuscula)-1, -1, -1):
            palabra_invertida += palabra_en_minuscula[i]
        
        # Verificar si es palíndromo
        es_palindromo = (palabra_en_minuscula == palabra_invertida)
        
        return es_palindromo, palabra_invertida
        
    except (StringVacia, InputInvalido, TypeError) as error:
        print(f"Error de validacion: {error}")
        raise

def obtener_palabra():
    while True:
        try:
            palabra = input("Ingrese la palabra para verificar si es palindromo: ")
            
            # Intentar validar la palabra
            validar_entrada(palabra)
            return palabra
            
        except StringVacia:
            print("Error: No puede ingresar una cadena vacia.")
        except InputInvalido as error:
            print(f"Error: {error}")
            print("Solo se permiten letras y espacios.")
        except KeyboardInterrupt:
            print("Operacion cancelada por el usuario.")
            raise

if __name__ == "__main__":
    try:
        palabra = obtener_palabra()
        # Verificar si es palíndromo
        resultado, palabra_invertida = palindromo(palabra)
        
        if resultado:
            print(f"La palabra/frase '{palabra}' ES un palíndromo")
        else:
            print(f"La palabra/frase '{palabra}' NO es un palíndromo")
            print(f"Su inversa es: '{palabra_invertida}'")
            
    except Exception as error:
        print(f"Ocurrio un error: {error}")