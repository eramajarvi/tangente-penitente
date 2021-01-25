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
        """ Construye un conjunto correcto a partir del conjunto de coincidencias dado. """

        for i in range(len(self.conjuntoCoincidencia)):
            ref = self.conjuntoCoincidencia[i]

            # ---------------------------------------------------
            # FENOTIPO DISCRETO
            # ---------------------------------------------------
            if cons.amb.datosFormateados.fenotipoDiscreto:
                if self.conjuntoPob[ref].fenotipo == fenotipo:
                    self.conjuntoCorrectos.append(ref)

            # ---------------------------------------------------
            # FENOTIPO CONTINUO
            # ---------------------------------------------------
            else:
                print("ConjuntoClasificadores - Error: Tangente Penitente no puede manipular fenotipos continuos.")

    def hacerEvalConjuntoCoincidencias(self, estado):
        """ Construye un conjunto de coincidencias con fines de evaluacion en el cual no se activa el covering ni la eliminacion. """

        # Se pasa a traves de toda la poblacion
        for i in range(len(self.conjuntoPob)):
            
            # Se toma un solo clasificador
            cl = self.conjuntoPob[i]

            # Se revisa si hay coincidencia
            if cl.coincidencia(estado):
                
                # Se agrega el clasificador al conjunto de coincidencias
                self.conjuntoCoincidencia.append(i)

    # -----------------------------------------------------------
    # METODOS DE ELIMINACION DE CLASIFICADORES
    # -----------------------------------------------------------
    def eliminacion(self, iterExplor):
        """ Cambia el tamano de la poblacion al tamano maximo establecido por el usuario al eliminar reglas. """

        cons.cronometro.iniciarTiempoEliminacion()

        while self.tamanoMicropob > cons.N:
            self.eliminarDePoblacion()

        cons.timer.detenerTiempoEliminacion()

    def eliminarDePoblacion(self):
        """ Elimina un clasificador en la poblacion. El clasificador que sera eliminado es escogido por seleccion de la ruleta considerando el voto de eliminacion. Devuelve el macroclasificador que fue decrementado por un microclasificador. """

        aptitudMedia = self.obtenerSumaAptitudPoblacion()/float(self.tamanoMicropob)
        
        # Calcular tamano total de la ruleta --------------------
        sumaCl = 0.0
        listaVotos = []

        for cl in self.conjuntoPob:
            voto = cl.obtenerProbEliminacion(aptitudMedia)
            sumaCl += voto
            listaVotos.append(voto)

        # -------------------------------------------------------

        # Determina el punto de eleccion
        puntoEleccion = sumaCl * random.random()

        nuevaSuma = 0.0

        for i in range(len(listaVotos)):
            cl = self.conjuntoPob[i]
            nuevaSuma = nuevaSuma + listaVotos[i]

            # Seleccionar el clasificador para eliminar
            if nuevaSuma > puntoEleccion:
                
                # Elimina el clasificador
                cl.actualizarNumerosidad(-1)

                # Esto se da cuando todos los microclasificadores para un clasificador dado se han agotado
                if cl.numerosidad < 1:
                    self.eliminarMacroClasificador(i)
                    self.eliminarDelConjuntoCoincidencias(i)
                    self.eliminarDelConjuntoCorrectos(i)

                return

        print("ConjuntoClasificadores: No se encontraron reglas elegibles para ser eliminadas de la poblacion.")

        return

    def eliminarMacroClasificador(self, ref):
        """ Elimina el macroclasificador o el clasificador especificado de la poblacion """

        self.conjuntoPob.pop(ref)

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

