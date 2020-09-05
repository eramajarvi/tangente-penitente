# TANGENTE PENITENTE
# CE.py

"""
Un paso de preprocesamiento cuando se activa en Tangente Penitente. Convierte las puntuaciones numéricas del conocimiento experto de cualquier fuente 
en probabilidades para orientar el mecanismo de covering en la determinación de los atributos que se especificarán y los que se generalizarán. Esta 
estrategia fue propuesta y publicada por Ryan Urbanowicz, Delaney Granizo-Mackenzie y Jason Moore en "Using Expert Knowledge to Guide Covering and 
Mutation in a Michigan Style Learning Classifier System to Detecting Epistasis and Heterogeneity". [2012].
"""

import os
import copy
import time
from RBA.multisurf import *
from RBA.relieff import *
from RBA.surf import *
from RBA.surfstar import *
from RBA.turf_envoltorio import *

class ConocimientoExperto:
    def __init__(self, cons):
        """ Inicializacion del Conocimiento Experto - Los puntajes se ordenan segun aparecen en el conjunto de datos """

        self.puntajes = None
        self.rangoCE - None

        if cons.GeneracionInternaCE or cons.soloPuntajesCE:
            print("ConocimientoExperto: Se inicio la generacion interna del CE")
            self.puntajes = self.ejecutarFiltros(cons)

        else:
            print("ConocimientoExperto: Cargando CE externo")
            self.puntajes = self.cargarCE(cons.fuenteCE, cons)

        # Nos aseguramos que los puntajes no sean negativos
        self.ajustarPuntajes(cons)

        # Nuevo protocolo de especificacion
        self.sumaCE = sum(self.puntajes)
        self.rangoCE = []

        CEtemp = copy.deepcopy(self.puntajes)

        for i in range(len(self.puntajes)):
            mejorCE = CEtemp[0]
            mejorC = 0

            for j in range(1, len(CEtemp)):
                if CEtemp[j] > mejorCE:
                    mejorCE = CEtemp[j]
                    mejorC = j

            self.rangoCE.append(mejorC)
            CEtemp[mejorC] = 0

        # Usado para seleccionar atributos para la especificacion en el covering (sin reemplazos)
        self.listaRef = []
        for i in range(len(self.puntajes)):
            self.listaRef.append(i)

        # Convertir la lista de puntajes ajustados en probabilidades
        valorMax = max(self.puntajes)
        listaProb = []

        for i in range(cons.amb.datosFormateados.numAtributos):
            if valorMax == 0.0:
                listaProb.append(0.5)

            else:
                listaProb.append(self.puntajes[i]/float(valorMax + valorMax * 0.01))

        self.listaProbabilidadCE = listaProb

    def ajustarPuntajes(self, cons):
        """ Se asegura que el valor del puntaje minimo sea cero """
        pass

    def ejecutarFiltros(self, cons):
        pass

    def cargarCE(self, nombreRuta, cons):
        pass
