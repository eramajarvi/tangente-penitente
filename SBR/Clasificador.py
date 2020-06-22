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
        # Parametros principales ------------------------------
        
        # Atributo especificado en clasificador: similar a 
        # Bacardit 2009 - ALKR y GABIL, representacion de 
        # reglas discretas y continuas
        self.listaAtributosEspecificados = []
        # Estados de atributos especificados en el clasificador:
        # similar a Bacardit 2009 - ALKR y GABIL, representacion
        # de reglas discretas y continuas
        self.condicion = []
        # Clase si el fenotipo es discreto o continuo
        self.fenotipo = None

        # Aptitud del clasificador - inicializado a un valor de
        # aptitud inicial constante
        self.aptitud = cons.aptitudInicial
        # Precision del clasificador - Precision calculada usando
        # solo instancias en el conjunto de datos que la regla
        # coincide
        self.precision = 0.0
        # Numero de copias de las reglas almacenadas en la poblacion
        # (Guardado indirectamente como numerosidad incrementada)
        self.numerosidad = 1
        # Un parametro usado en eliminacion que refleja el tamano del
        # conjunto de coincidencias dentro en el que esta regla ha sido
        # incluida
        self.tamanoPromedioConjuntoCoincidencia = None
        # El peso de eliminacion actual del clasificador
        self.votoEliminacion = None

        # Gestion de la experiencia ----------------------------
        
        # Tiempo que dura la regla en el conjunto correcto
        self.estampaTiempoAG = None
        # Iteracion en que la regla aparecio primero
        self.estampaTiempoInic = None
        # Ha existido esta regla por una epoca completa (esto es,
        # un ciclo a traves de un conjunto de entrenamiento)
        self.epocaCompletada = False

        # Seguimiento de precision del clasificador ------------
        
        # Conocido en varias implementaciones de LCS como experiencia
        # esto es, el numero total de veces que un clasificador estuvo
        # en un conjunto de coincidencia
        self.conteoCoincidencia = 0
        # El numero total de veces que este clasificador estuvo en un
        # conjunto correcto
        self.conteoCorrecto = 0
        # El numero total de veces que este clasificador estuvo en un
        # conjunto de coincidencia dentro de una sola epoca.
        self.cubrimientoCoincidencia = 0
        # El numero total de veces que este clasificador estuvo en un
        # conjunto correcto dentro de una sola epica.
        self.cubrimientoCorrecto = 0

        if isinstance(c, list):
            self.coveringClasificador(a, b, c, d)

        elif isinstance(a, Clasificador):
            self.copiarClasificador(a, b)

        elif isinstance(a, list) and b == None:
            self.reiniciarClasicicador(a)

        else:
            print("Clasificador: Error constuyendo el clasificador.")

    # --------------------------------------------------------
    # METODOS DE CONSTRUCCION DEL CLASIFICADOR
    # --------------------------------------------------------
    def coveringClasificador(self, tamanoConjunto, iterExploracion, estado, fenotipo):
        """ Hace un nuevo clasificador cuando es disparado el
        mecanismo de covering/cubrimiento. El nuevo clasificador
        coincidira con la instancia de entrenamiento actual. El 
        covering NO producira una regla por defecto (esto es, una regla
        con una condicion completamente general). """

        # Inicializa los parametros del nuevo clasificador
        self.estampaTiempoAG = iterExploracion
        self.estampaTiempoInic = iterExploracion
        self.tamanoPromedioConjuntoCoincidencia = tamanoConjunto
        infoDatos = cons.amb.datosFormateados

        # -----------------------------------------------------
        # FENOTIPO DISCRETO
        # -----------------------------------------------------
        if infoDatos.fenotipoDiscreto:
            self.fenotipo = fenotipo

        # -----------------------------------------------------
        # FENOTIPO CONTINUO
        # -----------------------------------------------------
        else:
            print("Clasificador - Error: Tangente Penitente no puede manjar endpoints continuos.")

        # -----------------------------------------------------
        # GENERAR CONDICION DE COINCIDENCIA
        # Con pesos del Conocimiento Experto
        # -----------------------------------------------------
        # ESTRATEGIA DETERMINISTA
        if cons.usarConocimientoExperto:
            # Selecciona el numero de atributos a especificar
            especificar = random.randint(1, infoDatos.limiteEspec)
            i = 0

            while len(self.listaAtributosEspecificados) < especificar:
                objetivo = cons.CE.RankCE[i]

                if estado[objetivo] != cons.etiquetaDatosFaltantes:
                    self.listaAtributosEspecificados.append(objetivo)
                    self.condicion.append(self.construirCoincidencia(objetivo, estado))

                i += 1

        # -----------------------------------------------------
        # GENERAR CONDICION DE COINCIDENCIA
        # Sin pesos del Conocimiento Experto
        # -----------------------------------------------------
        else:
            # Selecciona el numero de atributos a especificar
            especificar = random.randint(1, infoDatos.limiteEspec)
            # Lista de posibles atributos especificados
            potencialEspec = random.sample(range(infoDatos.numAtributos), especificar)

            for refAtt in potencialEspec:
                if estado[refAtt] != cons.etiquetaDatosFaltantes:
                    self.listaAtributosEspecificados.append(refAtt)
                    self.condicion.append(self.construirCoincidencia(refAtt, estado))

    def seleccionarAtributoRW(self, especificar):
        """ Selecciona atributos a ser especificados en el covering
        del clasificador usando pesos del conocimiento experto y
        seleccion de ruleta (Roulette Wheel). """
        # Conjunto correcto es una lista de IDs de referencia
        listaPuntajesRef = copy.deepcopy(cons.CE.listaRef)
        listaSeleccion = []
        conteoActual = 0
        sumaTotal = copy.deepcopy(cons.CE.SumaCE)

        while conteoActual < especificar:
            puntoOpcion = random.random() * sumaTotal
            i = 0
            puntajeSuma = cons.CE.puntajes[listaPuntajesRef[i]]

            while puntoOpcion > puntajeSuma:
                i = i + 1
                puntajeSuma += cons.CE.puntajes[listaPuntajesRef[i]]

            listaSeleccion.append(listaPuntajesRef[i])
            sumaTotal -= cons.EK.puntajes[listaPuntajesRef[i]]
            listaPuntajesRef.remove(listaPuntajesRef[i])
            conteoActual -= 1

        return listaSeleccion

    def copiarClasificador(self, clAntiguo, iterExploracion):
        """ Construye un clasificador identico. Sin embargo, la
        experiencia de la copia se fija en 0 y la numerosidad se
        fija en 1 dado que es un nuevo individuo en la poblacion.
        Usado por el algoritmo genetico para generar descendencia
        basada en clasificadores padres """

        self.listaAtributosEspecificados = copy.deepcopy(clAntiguo.listaAtributosEspecificados)
        self.condicion = copy.deepcopy(clAntiguo.condicion)
        self.fenotipo = copy.deepcopy(clAntiguo.fenotipo)
        self.estampaTiempoAG = iterExploracion
        self.estampaTiempoInic = iterExploracion
        self.tamanoPromedioConjuntoCoincidencia = copy.deepcopy(clAntiguo.tamanoPromedioConjuntoCoincidencia)
        self.aptitud = clAntiguo.aptitud
        self.precision = clAntiguo.precision

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
