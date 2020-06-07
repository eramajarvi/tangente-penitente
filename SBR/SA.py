# TANGENTE PENITENTE
# SA.py

"""
Maneja el almacenamiento, la actualización y la aplicación de la 
heurística de seguimiento de atributos y del feedback. Esta 
estrategia fue propuesta y publicada por Ryan Urbanowicz, 
Ambrose Granizo-Mackenzie y Jason Moore en "Instance-Linked 
Attribute Tracking and Feedback for Michigan-Style Supervised 
Learning Classifier Systems". [2012].
"""

from Constantes import *
import copy
import random

class SeguimientoAtributos:
    def __init__(self, hacerSeguimientoAtributos):
        """ Inicializar el objeto de Seguimiento de Atributos """

        self.porcentaje = 0.0

        if hacerSeguimientoAtributos:
            self.listaProbabilidad = []
            self.sumaPrecisionAtributos = [[0] * cons.amb.datosFormateados.numAtributos for i in range(cons.amb.datosFormateados.numInstanciasEntrenamiento)]

            if cons.hacerReinicioPoblacion:
                self.reiniciarSA()

    def actualizarPorcentaje(self, iterExplora):
        pass

    def actualizarSeguimientoAtributos(self, pob):
        pass

    def obtenerProbSeguimiento(self):
        pass

    def generarProbSeguimiento(self):
        pass

    def sumaSeguimientoAtributosGlobal(self):
        pass

    def reiniciarSA(self):
        pass