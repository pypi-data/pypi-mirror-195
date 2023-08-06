import unittest
from mensajes.hola.saludos import generar_array

class PruebasHola(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6)

        )

#import saludos        #importo todo el modulo
from mensajes.hola.saludos import *  # trae todas las funciones
#from saludos import saludar  #importo solo la funcion saludar  si tengo mas puedo poner , y agregar

saludar()
Saludo()

prueba()