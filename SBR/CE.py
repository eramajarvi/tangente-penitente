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
        pass

    def ajustarPuntajes(self, cons):
        pass

    def ejecutarFiltros(self, cons):
        pass

    def cargarCE(self, nombreRuta, cons):
        pass
