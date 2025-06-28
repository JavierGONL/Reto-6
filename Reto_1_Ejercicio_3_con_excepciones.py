
class ListaVaciaError(Exception):
    def __init__(self):
        super().__init__("No se puede procesar una lista vacia")

class NumeroInvalidoError(Exception):
    def __init__(self, valor):
        self.valor = valor
        super().__init__(f"Valor invalido: {valor}.")

def validar_lista_numeros(lista):
    if not isinstance(lista, list):
        raise TypeError(f"no se ingreso una lista, se ingreso: {type(lista).__name__}")
    
    if not lista:
        raise ListaVaciaError()
    
    for i, elemento in enumerate(lista):
        try:
            #convertir a entero
            numero = int(elemento)
            lista[i] = numero
            
            # Verificar que no sea negativo
            if numero < 0:
                raise NumeroInvalidoError(numero)
                
        except (ValueError, TypeError):
            raise NumeroInvalidoError(elemento)

def es_primo(numero):
    try:
        # Casos especiales
        if numero < 2:
            return False
        if numero == 2:
            return True
        if numero % 2 == 0:
            return False

        for i in range(3, int(numero**0.5) + 1, 2):
            if numero % i == 0:
                return False
        return True
    except Exception as e:
        raise NumeroInvalidoError(f"Error al verificar primalidad de {numero}: {e}")

def devolver_primos(lista):
    try:
        # Crear una copia para no modificar la lista original
        lista_copia = lista.copy()
        
        # Validar la lista
        validar_lista_numeros(lista_copia)
        
        # Encontrar números primos
        primos = []
        numeros_procesados = set()  # Para evitar duplicados
        
        for numero in lista_copia:
            # Evitar procesar el mismo número múltiples veces
            if numero in numeros_procesados:
                continue
                
            numeros_procesados.add(numero)
            
            try:
                if es_primo(numero):
                    primos.append(numero)
            except NumeroInvalidoError as e:
                print(f"Advertencia: {e}")
                continue
        
        # Ordenar los primos encontrados
        primos.sort()
        return primos
        
    except (TypeError, ListaVaciaError, NumeroInvalidoError, NumeroInvalidoError) as e:
        print(f"Error de validación: {e}")
        raise
    except Exception as e:
        print(f"Error inesperado al procesar la lista: {e}")
        raise

def obtener_lista_usuario():
    while True:
        try:
            entrada = input("Ingrese números separados por comas (ej: 1,2,3,4,5): ")
            
            if not entrada.strip():
                raise ListaVaciaError()
            
            # Convertir entrada a lista
            numeros_str = [num.strip() for num in entrada.split(',')]
            numeros = []
            
            for num_str in numeros_str:
                try:
                    numero = int(num_str)
                    numeros.append(numero)
                except ValueError:
                    raise NumeroInvalidoError(num_str)
            
            return numeros
            
        except ListaVaciaError:
            print("Error: No puede ingresar una lista vacia.")
        except NumeroInvalidoError as error:
            print(f"Error: {error}")



if __name__ == "__main__":
    try:
        print("Ingrese una lista de números para encontrar los primos:")
        numeros = obtener_lista_usuario()
        
        resultado_primos = devolver_primos(numeros)
        
        if resultado_primos:
            print(f"Numeros primos encontrados: {resultado_primos}")
        else:
            print("No se encontraron numeros primos en la lista.")
            
    except Exception as error:
        print(f"Ocurrio un error inesperado: {error}")