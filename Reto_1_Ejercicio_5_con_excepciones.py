class ListaVaciaError(Exception):
    def __init__(self):
        super().__init__("No se puede procesar una lista vacia")

class PalabraInvalidaError(Exception):
    def __init__(self, palabra, razon):
        self.palabra = palabra
        self.razon = razon
        super().__init__(f"Palabra invalida '{palabra}': {razon}")

class StringVaciaError(Exception):
    def __init__(self):
        super().__init__("No se permiten palabras vacias")

def validar_palabra(palabra):
    if not isinstance(palabra, str):
        raise TypeError(f"Se esperaba una cadena, se recibio: {type(palabra).__name__}")
    
    if not palabra or palabra.isspace():
        raise StringVaciaError()
    
    # Permitir solo letras y espacios
    for letra in palabra:
        if not letra.isalpha() and not letra.isspace():
            raise PalabraInvalidaError(palabra, f"contiene el caracter invalido '{letra}'")
    
    # Verificar que no sea solo espacios después de strip
    if not palabra.strip():
        raise StringVaciaError()

def validar_lista_palabras(lista_palabras):
    if not isinstance(lista_palabras, list):
        raise TypeError(f"Se esperaba una lista, se recibio: {type(lista_palabras).__name__}")
    
    if not lista_palabras:
        raise ListaVaciaError()
    
    # Validar cada palabra en la lista
    for i, palabra in enumerate(lista_palabras):
        try:
            validar_palabra(palabra)
        except (TypeError, StringVaciaError, PalabraInvalidaError) as error:
            raise PalabraInvalidaError(f"elemento {i}", str(error))

def normalizar_palabra(palabra):
    return palabra.replace(" ", "").lower().strip()

def tienen_mismos_caracteres(palabra1, palabra2):
    try:
        # Normalizar ambas palabras
        norm1 = normalizar_palabra(palabra1)
        norm2 = normalizar_palabra(palabra2)
        
        # Verificar que no sean la misma palabra
        if norm1 == norm2:
            return False
        
        # Comparar caracteres ordenados (esto detecta anagramas)
        return sorted(norm1) == sorted(norm2)
        
    except Exception as error:
        raise PalabraInvalidaError(f"{palabra1}, {palabra2}", f"error al comparar: {error}")

def mismos_caracteres(lista_palabras):
    try:
        # Validar la lista de entrada
        validar_lista_palabras(lista_palabras)
        
        # Limpiar y normalizar la lista
        palabras_validas = []
        palabras_procesadas = set()
        
        for palabra in lista_palabras:
            try:
                validar_palabra(palabra)
                palabra_normalizada = normalizar_palabra(palabra)
                
                # Evitar duplicados exactos
                if palabra_normalizada not in palabras_procesadas:
                    palabras_validas.append(palabra.strip())
                    palabras_procesadas.add(palabra_normalizada)
                    
            except (StringVaciaError, PalabraInvalidaError) as error:
                print(f"Advertencia: Palabra '{palabra}' ignorada - {error}")
                continue
        
        if not palabras_validas:
            raise ListaVaciaError()
        
        # Encontrar anagramas
        palabras_con_anagramas = []
        palabras_ya_procesadas = set()
        
        for i in range(len(palabras_validas)):
            if palabras_validas[i] in palabras_ya_procesadas:
                continue
                
            # Buscar anagramas de esta palabra
            for j in range(i + 1, len(palabras_validas)):
                if palabras_validas[j] in palabras_ya_procesadas:
                    continue
                    
                try:
                    if tienen_mismos_caracteres(palabras_validas[i], palabras_validas[j]):
                        # Agregar ambas palabras si no están ya en la lista
                        if palabras_validas[i] not in palabras_con_anagramas:
                            palabras_con_anagramas.append(palabras_validas[i])
                        if palabras_validas[j] not in palabras_con_anagramas:
                            palabras_con_anagramas.append(palabras_validas[j])
                        
                        palabras_ya_procesadas.add(palabras_validas[i])
                        palabras_ya_procesadas.add(palabras_validas[j])
                        
                except PalabraInvalidaError as error:
                    print(f"Advertencia: Error al comparar palabras - {error}")
                    continue
        
        return palabras_con_anagramas
        
    except (TypeError, ListaVaciaError, PalabraInvalidaError) as error:
        print(f"Error de validacion: {error}")
        raise

if __name__ == '__main__':
    try:
        # Lista de demostración
        lista_palabras = ['hola', 'arroz', 'zorra', 'pasos', 
                         'mundo', 'aloh', 'reconocer', 'reconocer',
                         'amor', 'roma', 'mora', 'moneda', 'deamon']
        print(f"Lista de palabras: {lista_palabras}")
        
        resultado = mismos_caracteres(lista_palabras)
        if resultado:
            print(f"Palabras con anagramas encontradas: {resultado}")
        else:
            print("No se encontraron anagramas")
            
    except Exception as error:
        print(f"Ocurrio un error: {error}")
