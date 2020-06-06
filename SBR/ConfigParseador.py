# TANGENTE PENITENTE
# ConfigParseador.py

"""
Maneja el archivo de configuración cargando, analizando y 
pasando sus valores a Constantes. También incluye un método para 
generar conjuntos de datos para la validación cruzada.
"""

from Constantes import *
import os
import copy
import random

class ConfigParseador:
    def __init__(self, nombreArchivo):
        
        # Siempre se usa la misma semilla aqui, de tal forma que
        # los mismos conjuntos de datos de VC seran generados si se
        # ejecuta de nuevo
        random.seed(1)

        self.carComentario = '#'
        self.carParametro = '='
        
        # Parsea el archivo de configuracion y obtiene todos los
        # parametros
        self.parametros = self.parsearConfiguracion(nombreArchivo)
        
        # Construye la clase Constantes usando los parametros del
        # archivo de configuracion
        cons.fijarConstantes(self.parametros)

        if cons.validacionCruzadaInterna == 0 or cons.validacionCruzadaInterna == 1:
            pass
        
        # Hacer VC interna
        else:
            self.PartVC()

    def parsearConfiguracion(self, nombreArchivo):
        pass

    def PartVC(self):
        pass

    def hacerParticiones(self, listaVC, numParticiones, rutaArchivo, listaEncabezados):
        pass