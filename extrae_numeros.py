import sys

class numeros_naturales:
    def __init__(self):
        self.numeros = list(range(1, 101))  
        self.numero_extraido = None
    
    def extraer_numero(self, numero):
        self.numeros.remove(numero)

    def calcular_extraido(self):
        lista_original = sum(range(1, 101)) 
        lista_actual = sum(self.numeros)
        return lista_original - lista_actual


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python extrae_numeros.py <numero_a_extraer>")
        sys.exit(1)
   
    try: 
        numero = int(sys.argv[1])
        if not type(numero) is int:
            print("Debe ingresar numeros enteros")
            sys.exit(1)
        else: 
            if numero < 1 or numero > 100:
                print("Debe ingresar un numero mayor que 1 y menor que 100")
                sys.exit(1)
            else: 
                conjunto = numeros_naturales()
                conjunto.extraer_numero(numero)
                print("Se extrajo el numero: " + str(conjunto.calcular_extraido()))
    except ValueError as e:
        print("Error: " + str(e))


        

