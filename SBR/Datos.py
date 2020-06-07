# TANGENTE PENITENTE
# Datos.py

"""
Carga el conjunto de datos, caracteriza y almacena las 
características críticas de los conjuntos de datos (incluyendo 
los atributos discretos frente a los continuos y el fenotipo), 
maneja los datos que faltan y, finalmente, da formato a los 
datos para que puedan ser convenientemente utilizados por 
Tangente Penitente.
"""

import math
import random
import sys
from Constantes import *

class GestionDatos:
    def __init__(self, archivoEntrenamiento, archivoPrueba, listaInfo = None):
        pass

    def cargarDatos(self, archivoDatos, hacerEntrenamiento):
        pass

    def caracterizarConjuntoDatos(self, datosEntrenamientoCrudos):
        pass

    def discriminarFenotipo(self, datosCrudos):
        pass

    def discriminarClases(self, datosCrudos):
        pass

    def compararConjuntoDatos(self, datosPruebaCrudos):
        pass

    def discriminarAtributos(self, datosCrudos):
        pass

    def caracterizarAtributos(self, datosCrudos):
        pass

    def calcularDE(self, listaFenotipos):
        pass

    def formatearDatos(self, datosCrudos, entrenamiento):
        pass

    def guardarDatosTurfTemp(self):
        pass

    def regresarDatosCompletos(self):
        pass

    def gestionDatosTurf(self, puntajesFiltro, porcentajeTurf):
        pass

    def hacerConjuntoDatosFiltrado(self, atributosEnDatos, nombreArchivo, puntajesFiltro):
        pass