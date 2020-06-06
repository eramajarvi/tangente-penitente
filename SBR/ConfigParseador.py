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
        """ Parsear el archivo de configuracion """
        parametros = {}

        try:
            a = open(nombreArchivo, 'rU')

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('No se pudo abrir', nombreArchivo)
            raise
            
        else:
            for linea in a:
                # Primero eliminar los comentarios:
                if self.carComentario in linea:
                    # Separar el caracter de comentarios, guardar
                    # solo la parte de despues
                    linea, comentario = linea.split(self.carComentario, 1)

                # Segundo encontrar lineas con un parametro = valor
                if self.carParametro in linea:
                    # Separar el caracter de parametro:
                    parametro, valor = linea.split(self.carParametro, 1)

                    # Eliminar espacios:
                    parametro = parametro.strip()
                    valor = valor.strip()

                    # Guardar el diccionario:
                    parametros[parametro] = valor

            a.close()

        return parametros

    def PartVC(self):
        pass

    def hacerParticiones(self, listaVC, numParticiones, rutaArchivo, listaEncabezados):
        pass