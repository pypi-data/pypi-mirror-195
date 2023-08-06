import numpy as np

def saludar():
    print("Hola bebeee, te saludo desde mi casa ;)")
 
class Saludo:
    def __init__(self):
        print("hola te saludo desde __init__ (la clase)")

def generar_array(numeros):
    return np.arange(numeros)


def hambre(): 
    print("definitivamente yo tengo hambre todo el tiempo")
    print("esto es una prueba para la version 2.0")
 

if __name__ == '__main__': #son dos guiones bajos en cada caso
    #saludar()
    print(generar_array(5))
