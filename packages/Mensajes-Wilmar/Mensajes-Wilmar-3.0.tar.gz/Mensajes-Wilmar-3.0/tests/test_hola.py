#import saludos

#saludos.saludar()

#from saludos import saludar #podemos usar este esquema para importar modulos especificos, esto en el caso 
                            #de que tuvieramos más declarados agregando una coma (saludar, adios, prender...)

#saludar()


#from mensajes.hola.saludos import * #de esta forma también podemos importar todo el contenido del módulo
#from mensajes.adios.despedidas import *

#saludar()
#Saludo()

#print()

#despedir()
#Chao()

#como estamos instalando los paquetes, cada paquete debe tener su test, para este caso 
#vamos a configurar una prueba unitaria para HOLA

import unittest
import numpy as np
from mensajes.hola.saludos import generar_array

class PruebasHola(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0, 1, 2, 3, 4, 5]),
            generar_array(6)
        ) 




