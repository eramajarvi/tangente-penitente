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
        """ Determina la frecuencia en la que el feeback de atributos
        es aplicado dentro del AG. """
        self.porcentaje = iterExplora / float(cons.iteracionesAprendizajeMax)

    def actualizarSeguimientoAtributos(self, pob):
        """ Actualiza el seguimiento de los atributos """
        refDatos = cons.env.refDatos

        for ref in pob.conjuntoCorrecto:
            for each in pob.conjuntoPoblacion[ref].listaAtributosEspecificados:
                # Agregar precision de la regla
                self.sumaPrecisionAtributos[refDatos][each] += (pob.conjuntoPoblacion[ref].precision)

    def obtenerProbSeguimiento(self):
        """ Devuelve la lista de probabilidad de seguimiento """

        return self.listaProbabilidad

    def generarProbSeguimiento(self):
        """ Calcula y regresa las probabilidades del atributo
        basado en los puntajes del seguimiento de atributos """

        # Escoge un puntaje de seguimiento de atributos de una 
        # instancia de datos al azar
        instanciaActual = random.randint(0, cons.amb.datosFormateados.numInstanciasEntrenamiento - 1)

        # Obtiene una referencia al conjunto de datos
        listaSeguimiento = copy.deepcopy(self.sumaPrecisionAtributos[instanciaActual])

        valMin = min(listaSeguimiento)

        for i in range(len(listaSeguimiento)):
            listaSeguimiento[i] = listaSeguimiento[i] - valMin

        valMax = max(listaSeguimiento)

        listaProbabilidad = []

        for i in range(cons.amb.datosFormateados.numAtributos):
            if valMax == 0.0:
                listaProbabilidad.append(0.5)

            else:
                listaProbabilidad.append(listaSeguimiento[i] / float(valMax + valMax * 0.01))

        self.listaProbabilidad = listaProbabilidad

    def sumaSeguimientoAtributosGlobal(self):
        pass

    def reiniciarSA(self):
        pass