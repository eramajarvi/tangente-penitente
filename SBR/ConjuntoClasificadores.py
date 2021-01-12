# TANGENTE PENITENTE
# conjuntoclasificadores.py

"""
Este módulo maneja todos los conjuntos de clasificadores (población, conjunto de coincidencias, conjunto correcto) junto con los mecanismos 
y la heurística que actúan sobre estos conjuntos.
"""

from SBR.constantes import *
from SBR.clasificador import Clasificador

import random
import copy
import sys

class ConjuntoClasificadores:
    def __init__(self, a = None):
        """ Inicializacion sobrecargada: maneja la creacion de una nueva poblacion o de una poblacion reiniciada (esto es, una poblacion previamente guardada). """

        # Parametros principales --------------------------------

        # Lista de clasificadores / reglas
        self.conjuntoPob = []

        # Lista de referencias a reglas en la poblacion que coinciden
        self.conjuntoCoincidencia = []

        # Lista de referencias a reglas en la poblacion que coinciden y que tienen el fenotipo correcto
        self.conjuntoCorrectos = []

        # Sigue el tamano de la micropoblacion actual, esto es, el tamano de la poblacion que toma en cuenta la numerosidad de la regla
        self.tamanoMicropob = 0

        # Parametros de evaluacion --------------------------------
        self.GeneralidadProm = 0.0
        self.reglasExp = 0.0
        self.listaAtributosEspec = []
        self.listaAtributosPrec = []
        self.rangoPromFenotipo = 0.0

        # Constructores de los conjuntos --------------------------
        if a == None:

            # Inicializa una nueva poblacion
            self.crearPoblacion()

        elif isinstance(a, str):

            # Inicializa una nueva poblacion basada en una poblacion de reglas guardadas existente
            self.reiniciarPoblacion(a)

        else:
            print("ConjuntoClasificadores: Hubo un error al construir la poblacion.")

    # ------------------------------------------------------------
    # METODOS CONSTRUCTORES DE POBLACION
    # ------------------------------------------------------------
    def crearPoblacion(self):
        """ Inicializa la poblacion de reglas """
        self.conjuntoPob = []

    def reiniciarPoblacion(self, archivoReinicio):
        pass

    def hacerConjuntoCoincidencias(self, estadoFenotipo, iterExplor):
        pass

    def hacerConjuntoCorrectos(self, fenotipo):
        pass

    def hacerEvalConjuntoCoincidencias(self, estado):
        pass

    def eliminacion(self, iterExplor):
        pass

    def eliminarDePoblacion(self):
        pass

    def eliminarMacroClasificador(self, ref):
        pass

    def eliminarDelConjuntoCoincidencias(self, refEliminar):
        pass

    def eliminarDelConjuntoCorrectos(self, refEliminar):
        pass

    def ejecutarAG(self, iterExplor, estado, fenotipo):
        pass

    def seleccionarClasificadorRuleta(self):
        pass

    def seleccionarClasificadorT(self):
        pass

    def subsumirClasificador(self, cl = None, cl1P = None, cl2P = None):
        pass

    def subsumirClasificador2(self, cl):
        pass

    def hacerSubsuncionCorrecta(self):
        pass

    def agregarClasificadorAPoblacion(self, cl, covering):
        pass

    def insertarClasificadoresDescubiertos(self, cl1, cl2, clP1, clP2, iterExplor):
        pass

    def actualizarConjuntos(self, iterExplor):
        pass

    def ObtenerPromedioEstampaIter(self):
        pass

    def fijarEstampasIter(self, iterExplor):
        pass

    def obtenerSumaAptitud(self, listaConjuntos):
        pass

    def obtenerSumaAptitudPoblacion(self):
        pass

    def obtenerClasificadoresIdenticos(self, nuevoCl):
        pass

    def limpiarConjuntos(self):
        pass

    def ejecutarEvaluacionPoblacionPromedio(self, iterExplor):
        pass

    def ejecutarSumaGeneralidadAtrib(self):
        pass

    def recalcularSumaNumerosidad(self):
        pass

    def obtenerSeguimientoPob(self, precision, iterExplor, frecuenciaSeguimiento):
        pass

