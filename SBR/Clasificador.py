# TANGENTE PENITENTE
# Clasificador.py

"""
Este módulo define un clasificador individual dentro de la 
población de reglas, junto con todos los parámetros respectivos. 
Se incluyen los métodos al nivel de clasificador, incluyendo el 
emparejamiento de constructores (covering, copia, reinicio), la 
subsunción, el cruce y la mutación. También se incluyen métodos
de actualización de parámetros.
"""

from Constantes import *
import random
import copy
import math
import ast

class Clasificador:
    def __init__(self, a = None, b = None, c = None, d = None):
        pass

    def coveringClasificador(self, especificar):
        pass

    def copiarClasificador(self, clAntiguo, iterExploracion):
        pass

    def reiniciarClasicicador(self, listaClasificador):
        pass

    def coincidencia(self, estado):
        pass

    def cruzamientoUniforme(self, cl):
        pass

    def arregloLimiteEspec(self, cl):
        pass

    def mutacion(self, estado, fenotipo):
        pass

    def selecGeneralizarRW(self, conteo):
        pass

    def mutarAtributosContinuos(self, usarSA, j):
        pass

    def revisarRangos(self):
        pass

    def subsumir(self, cl):
        pass

    def esSubsumidor(self):
        pass

    def esMasGeneral(self, cl):
        pass

    def obtenerProbEliminacion(self, aptitudMedia):
        pass

    def construirCoincidencia(self, refAtt, estado):
        pass

    def equivalente(self, cl):
        pass

    def actualizarEstadoEpoca(self, iterExploracion):
        pass

    def actualizarAptitud(self):
        pass

    def actualizarExperiencia(self):
        pass

    def actualizarCorrectos(self):
        pass

    def actualizarNumerosidad(self):
        pass

    def actualizarTamanoConjuntoCoincidencia(self, tamanoConjuntoCoincidencia):
        pass

    def actualizarEstampaTiempo(self, ts):
        pass

    def actualizarPrecision(self):
        pass

    def fijarPrecision(self, precision):
        pass

    def fijarAptitud(self, apt):
        pass

    def imprimirClasificador(self):
        pass
