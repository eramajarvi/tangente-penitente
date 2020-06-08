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
        # Inicializar variables globales
        self.refDatos = 0
        self.guardarRefDatos = 0
        self.datosFormateados = GestionDatos(cons.archivoEntrenamiento, cons.archivoPrueba)

        self.estadoEntrenamientoActual = self.datosFormateados.entrenamientoFormateados[self.refDatos][0]
        self.fenotipoEntrenamientoActual = self.datosFormateados.entrenamientoFormateados[self.refDatos][1]

        if cons.archivoPrueba == 'None':
            pass

        else:
            self.estadoPruebaActual = self.datosFormateados.pruebaFormateados[self.refDatos][0]
            self.fenotipoPruebaActual = self.datosFormateados.pruebaFormateados[self.refDatos][1]

    def obtenerInstanciaEntrenamiento(self):
        """ Devuelve la instancia de entrenamiento actual """
        return [self.estadoEntrenamientoActual, self. fenotipoEntrenamientoActual]

    def obtenerInstanciaPrueba(self):
        """ Devuelve la instancia de prueba actual """
        return [self.estadoPruebaActual, self.fenotipoPruebaActual]

    def nuevaInstancia(self, estaEntrenando):
        """ Hace que el ambiente vaya a la siguiente instancia
        en los datos. """

        # Datos de entrenamiento
        if estaEntrenando:
            if self.refDatos < (self.datosFormateados.numInstanciasEntrenamiento - 1):
                self.refDatos += 1
                self.estadoEntrenamientoActual = self.datosFormateados.entrenamientoFormateados[self.refDatos][0]
                self.fenotipoEntrenamientoActual = self.datosFormateados.entrenamientoFormateados[self.refDatos][1]

            # Una vez el aprendizaje ha completado una epoca, empieza
            # de nueva en la primera instancia en los datos
            else:
                self.resetearRefDatos(estaEntrenando)

        # Datos de prueba
        else:
            if self.refDatos < (self.datosFormateados.numInstanciasPrueba - 1):
                self.refDatos += 1
                self.estadoPruebaActual = self.datosFormateados.pruebaFormateados[self.refDatos][0]
                self.fenotipoPruebaActual = self.datosFormateados.pruebaFormateados[self.refDatos][1]

    def resetearRefDatos(self, estaEntrenando):
        """ Resetea el conteo de iteraciones a traves del
        conjunto de datos actual. """
        self.refDatos = 0

        if estaEntrenando:
            self.estadoEntrenamientoActual = self.datosFormateados.entrenamientoFormateados[self.refDatos][0]
            self.fenotipoEntrenamientoActual = self.datosFormateados.entrenamientoFormateados[self.refDatos][1]

        else:
            self.estadoPruebaActual = self.datosFormateados.pruebaFormateados[self.refDatos][0]
            self.fenotipoPruebaActual = self.datosFormateados.pruebaFormateados[self.refDatos][1]

    def iniciarModoEvaluacion(self):
        pass

    def detenerModoEvaluacion(self):
        pass