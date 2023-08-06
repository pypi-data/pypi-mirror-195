import numpy as np

def saludar():
    print("Hola te saludooo desde saludo.saludar()")
    

class Saludo():
    
    def __init__(self):
        print("Hola te saludooo desde saludo.init()")
        
def prueba():
    print("Prueba de la versión 6.0")
    
def generar_array(numero):
    return np.arange(numero)
    
     
if __name__ =="__main__":     # Esta linea nos dice si el archivo que lo ejecuta es igual al que lo contiene se ejecuten las demas lineas
    
    print(generar_array(5))