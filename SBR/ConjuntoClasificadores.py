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

    # -----------------------------------------------------------
    # METODOS CONSTRUCTORES DE POBLACION
    # -----------------------------------------------------------
    def crearPoblacion(self):
        """ Inicializa la poblacion de reglas """
        self.conjuntoPob = []

    def reiniciarPoblacion(self, archivoReinicio):
        """ Rehace una poblacion previamente evolucionada de un archivo de texto guardado. """

        print("Reiniciando la siguiente poblacion: " + str(archivoReinicio) + "_PoblacionReglas.txt")

        # Manipulacion inicial del archivo
        listaConjuntoDatos = []

        try:
            f = open(archivoReinicio + "_PoblacionReglas.txt", 'rU')

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('No se pudo abrir', archivoReinicio + "_PoblacionReglas.txt")
            raise

        else:
            
            # Elimina la primera linea
            self.listaEncabezados = f.readline().rstrip('\n').split('\t')

            for line in f:
                listaLinea = line.strip('\n').split('\t')
                listaConjuntoDatos.append(listaLinea)

            f.close()

        # -------------------------------------------------------
        for each in listaConjuntoDatos:
            cl = Clasificador(each)

            # Agrega el clasificador a la poblacion
            self.conjuntoPob.append(cl)

            # Ubicacion de la numerosidad variables en el archivo de poblacion
            refNumerosidad = 5

            self.tamanoMicropob += int(each[refNumerosidad])

    # -----------------------------------------------------------
    # METODOS CONSTRUCTORES DE CONJUNTOS DE CLASIFICADORES
    # -----------------------------------------------------------
    def hacerConjuntoCoincidencias(self, estadoFenotipo, iterExplor):
        """ Construye un conjunto de coincidencias desde la poblacion. El covering es iniciado si el conjunto de coincidencias esta vacio o una regla con el fenotipo correcto actual esta ausente. """

        # Valores iniciales -------------------------------------
        estado = estadoFenotipo[0]
        fenotipo = estadoFenotipo[1]

        # Revision del covering: se hace dos veces que haya al menos una coincidencia presente y que al menos una coincidencia dicte el fenotipo correcto
        hacerCovering = True

        fijarSumaNumerosidad = 0

        # -------------------------------------------------------
        # COINCIDENCIAS
        # -------------------------------------------------------
        cons.cronometro.iniciarTiempoCoincidencias()

        # Pasar a traves de la poblacion
        for i in range(len(self.conjuntoPob)):
            
            cl = self.conjuntoPob[i]

            # Un clasificador a la vez
            cl.actualizarEstadoEpoca(iterExplor)
            # Se sabe si el clasificador ha sido visto en este punto en todos los datos de entrenamiento.

            # Revisa si hay coincidencia
            if cl.coincidencia(estado):

                # Si hay coincidencia, se agrega el clasificador al conjunto de coincidencias
                self.conjuntoCoincidencia.append(i)

                # Se incrementa la suma de numerosidad del conjunto
                fijarSumaNumerosidad += cl.numerosidad

                # Revision del covering -------------------------
                # Si el fenotipo es discreto
                if cons.amb.datosFormateados.fenotipoDiscreto:
                    
                    # Se revisa el cubrimiento del fenotipo
                    if cl.fenotipo == fenotipo:
                        hacerCovering = False

                # Fenotipo continuo
                else:
                    print("ConjuntoClasificadores - Error: Tangente Penitente no puede manipular datos continuos.")

        cons.cronometro.detenerTiempoCoincidencias()

        # -------------------------------------------------------
        # COVERING
        # -------------------------------------------------------
        while hacerCovering:
            cons.cronometro.iniciarTiempoCovering()

            nuevoCl = Clasificador(fijarSumaNumerosidad + 1, iterExplor, estado, fenotipo)
            self.agregarClasificadorAPoblacion(nuevoCl, True)
            
            # Se agrega el clasificador cubierto al conjunto de coincidencias
            self.conjuntoCoincidencia.append(len(self.conjuntoPob) - 1)

            hacerCovering = False

            cons.cronometro.detenerTiempoCovering()

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

