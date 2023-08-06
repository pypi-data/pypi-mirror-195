# Se pueden importar otros archivos que tengan lineas especificas para tener nuestro trabajo ordenada
import numpy as np
import unittest
from mensajes.hola.saludos import generar_array


class PruebasHola(unittest.TestCase):
    
    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6)
        )

