class OperacionInvalida(Exception):
    def __init__(self, operacion):
        self.operacion = operacion
        super().__init__(f"'{operacion}' no es una operación válida. Use +, -, *, /")

def operaciones(entrada_1, entrada_2, operacion):
    try:
        if operacion == "+":
            return entrada_1 + entrada_2
        elif operacion == "-":
            return entrada_1 - entrada_2
        elif operacion == "*":
            return entrada_1 * entrada_2
        elif operacion == "/":
            # Validación explícita de división por cero
            if entrada_2 == 0:
                raise ZeroDivisionError("No se puede dividir por cero")
            return entrada_1 / entrada_2
        else:
            raise OperacionInvalida(operacion)
        
    except ZeroDivisionError as error:
        print(f"Error matemático: {error}")
        raise

    except OperacionInvalida as error:
        print(f"Error de operación: {error}")
        raise

def obtener_numero_y_operacioon(numero_operaciones):
    operaciones_validas = ['+', '-', '*', '/']
    lista_numeros = []
    while True:
        try:
            for _ in range(numero_operaciones-1):
                lista_numeros.append(float(input(f"ingrese un numero pls: ")))
            operacion = input("Ingrese la operación que desea realizar (+, -, *, /): ").strip()
            if operacion in operaciones_validas:
                return lista_numeros, operacion 
            else:
                raise OperacionInvalida(operacion)
        except OperacionInvalida:
            print("Error: Debe ingresar una operacion válido. Intente nuevamente.")

if __name__ == "__main__":
    try:
        # Obtener datos del usuario con validación
        entrada = obtener_numero_y_operacioon(2)

        
        # Realizar operación
        resultado = operaciones(*entrada[0], )
        print(f"Resultado: {entrada[0][0]} {entrada[1]} {entrada[0][1]} = {resultado}")

    except Exception as error:
        print(f"Ocurrio un error: {error}")

