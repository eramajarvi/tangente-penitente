# TANGENTE PENITENTE
# AmbienteOffline.py

"""
En el contexto de las tareas de extracción y clasificación de 
datos, el "entorno" de Tangente Penitente es un conjunto de datos 
con un número limitado de instancias con cierto número de 
atributos y un único endpoint (típicamente un fenotipo o clase 
discreta) de interés. Este módulo gestiona el paso de Tangente 
Penitente por las iteraciones de aprendizaje, y las instancias 
de datos respectivamente. Se incluyen métodos especiales para 
pasar del aprendizaje a la evaluación de un conjunto de datos de
entrenamiento.
"""

from Datos import GestionDatos
from Constantes import *
import sys

class AmbienteOffline:
    def __init__(self):
        pass

    def obtenerInstanciaEntrenamiento(self):
        pass

    def obtenerInstanciaPrueba(self):
        pass

    def nuevaInstancia(self, estaEntrenando):
        pass

    def resetearRefDatos(self, estaEntrenando):
        pass

    def iniciarModoEvaluacion(self):
        pass

    def detenerModoEvaluacion(self):
        pass