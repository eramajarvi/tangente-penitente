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
        """ Reconstruye un clasificador guardado como parte
        de un reinicio de la poblacion"""

        self.listaAtributosEspecificados = ast.literal_eval(listaClasificador[0])
        self.condicion = ast.literal_eval(listaClasificador[1])

        # -----------------------------------------------------
        # FENOTIPO DISCRETO
        # -----------------------------------------------------
        if cons.amb.datosFormateados.fenotipoDiscreto:
            self.fenotipo = str(listaClasificador[2])

        # -----------------------------------------------------
        # FENOTIPO CONTINUO
        # -----------------------------------------------------
        else:
            print("Clasificador - Error: Tangente Penitente no puede manejar endpoints continuos")

        self.aptitud = float(listaClasificador[3])
        self.precision = float(listaClasificador[4])
        self.numerosidad = int(listaClasificador[5])
        self.tamanoPromedioConjuntoCoincidencia = float(listaClasificador[6])
        self.estampaTiempoAG = int(listaClasificador[7])
        self.estampaTiempoInic = int(listaClasificador[8])

        if str(listaClasificador[10]) == 'None':
            self.votoEliminacion = None

        else:
            self.votoEliminacion = float(listaClasificador[10])

        self.conteoCorrecto = int(listaClasificador[11])
        self.conteoCoincidencia = int(listaClasificador[12])
        self.cubrimientoCorrecto = int(listaClasificador[13])
        self.cubrimientoCoincidencia = int(listaClasificador[14])
        self.epocaCompletada = bool(listaClasificador[15])

    # -----------------------------------------------------
    # CUBRIMIENTO / MATCHING
    # -----------------------------------------------------

    def coincidencia(self, estado):
        """ Devuelve si el clasificador coincide con la situacion
        actual """

        for i in range(len(self.condicion)):
            infoAtributo = cons.amb.datosFormateados.infoAtributo[self.listaAtributosEspecificados[i]]

            # -----------------------------------------------------
            # ATRIBUTO CONTINUO
            # -----------------------------------------------------
            if infoAtributo[0]:
                valorInstancia = estado[self.listaAtributosEspecificados[i]]

                if self.condicion[i][0] < valorInstancia < self.condicion[i][1] or valorInstancia == cons.etiquetaDatosFaltantes:
                    pass

                else:
                    return False

            # -----------------------------------------------------
            # ATRIBUTO DISCRETO
            # -----------------------------------------------------
            else:
                estadoRep = estado[self.listaAtributosEspecificados[i]]

                if estadoRep == self.condicion[i] or estadoRep == cons.etiquetaDatosFaltantes:
                    pass
                else:
                    return False

        return True

    # -----------------------------------------------------
    # MECANISMOS DE ALGORITMOS GENETICOS
    # -----------------------------------------------------
    
    def cruzamientoUniforme(self, cl):
        """ Aplica cruzamiento uniforme y devuelve si el 
        clasificador ha cambiado. Maneja atributos discretos
        y continuos.
        #SWARTZ: self. Es donde para los mejores atributos son mas
        probables de ser especificados
        #DEVITO: cl. Es donde los atributos menos utiles son mas
        propensos a ser especificados 
        """

        # Siempre es una condicion de cruzamiento si es fenotipo es discreto
        # (si el fenotipo es continuo, la mitad del tiempo el cruzamiento
        # del fenotipo se lleva a cabo)
        if cons.amb.datosFormateados.fenotipoDiscreto or random.random() < 0.5:
            p_self_listaAtributosEspecificados = copy.deepcopy(self.listaAtributosEspecificados)
            p_cl_listaAtributosEspecificados = copy.deepcopy(cl.listaAtributosEspecificados)

            usarSA = False

            if cons.hacerFeedbackAtributos and random.random() < cons.SA.porcentaje:
                usarSA = True

            # Hacer que la lista de referencias de atributos 
            # aparezca en al menos uno de los padres
            listaAtributosCombo = []

            for i in p_self_listaAtributosEspecificados:
                listaAtributosCombo.append(i)

            for i in p_cl_listaAtributosEspecificados:
                if i not in listaAtributosCombo:
                    listaAtributosCombo.append(i)

                # El atributo esta especificado en ambos padres y
                # el atributo es discreto (no hay razon para hacer
                # cruzamiento)
                elif not cons.amb.datosFormateados.infoAtributo[i][0]:
                    listaAtributosCombo.remove(i)

            listaAtributosCombo.sort()
            # -----------------------------------------------------
            cambio = False

            for refAtt in listaAtributosCombo:
                infoAtributo = cons.amb.datosFormateados.infoAtributo[refAtt]

                # -----------------------------------------------------
                # PROBABILIDAD DE CRUZAMIENTO DEL ATRIBUTO
                # Feedback del atributo
                # -----------------------------------------------------
                if usarSA:
                    probabilidad = cons.SA.obtenerProbSeguimiento()[refAtt]

                # -----------------------------------------------------
                # PROBABILIDAD DE CRUZAMIENTO DEL ATRIBUTO
                # Cruzamiento normal
                # -----------------------------------------------------
                else:
                    # Probabilidad igual para alelos de atributos
                    # que se intercambiaran
                    probabilidad = 0.5

                # -----------------------------------------------------
                ref = 0

                if refAtt in p_self_listaAtributosEspecificados:
                    ref += 1

                if refAtt in p_cl_listaAtributosEspecificados:
                    ref += 1

                if ref == 0:
                    # Esto nunca deberia pasar: todos los atributos en 
                    # listaAtributosCombo deberian ser especificados en
                    # al menos un clasificador.
                    print("Error: CruzamientoUniforme")
                    pass

                # -----------------------------------------------------
                # CRUZAMIENTO
                # -----------------------------------------------------
                elif ref == 1:
                    # El atributo se ha especificado en una sola condicion
                    # Se hace un cambio probabilistico de todo el estado
                    # del atributo (El tipo del atributo no hace la diferencia)
                    if refAtt in p_self_listaAtributosEspecificados and random.random() > probabilidad:
                        # Si el atributo se ha especificado en SWARTZ y hay alta 
                        # probabilidad de que sea valioso, entonces es menos probable
                        # que se haga intercambio.
                        
                        # Referencia a la posicion del atributo en la representacion de reglas
                        i = self.listaAtributosEspecificados.index(refAtt)
                        # Toma el atributo desde self y lo agrega al cl
                        cl.condicion.append(self.condicion.pop(i))
                        cl.listaAtributosEspecificados.append(refAtt)
                        self.listaAtributosEspecificados.remove(refAtt)
                        # Elimina el atributo de self y lo agrega a cl
                        cambio = True

                    if refAtt in p_cl_listaAtributosEspecificados and random.random() < probabilidad:
                        # Si el atributo se ha especificado en DEVITO y hay alta
                        # probabilidad de que sea valioso, entonces es mas probable
                        # que se haga intercamio
                        
                        # Referencia a la posicion del atributo en la representacion de reglas
                        i = cl.listaAtributosEspecificados.index(refAtt)
                        # Toma el atributo de cl y lo agrega al self
                        self.condicion.append(cl.condicion.pop(i))
                        self.listaAtributosEspecificados.append(refAtt)
                        cl.listaAtributosEspecificados.remove(refAtt)
                        # Elimina el atributo de cl y lo agrega a self
                        cambio = True

                else:
                    # El atributo se ha especificado en ambas condiciones
                    # se hace cruzamiento aleatorio entre alelos de estados
                    # Importante: El feedback de atributos no se debe usar
                    # para juntar alelos con un estado de atributo
                    
                    # El mismo atributo debe ser especificado en diferentes
                    # posiciones dentro de cualquier clasificador
                    # -----------------------------------------------------
                    # ATRIBUTO CONTINUO
                    # -----------------------------------------------------
                    if infoAtributo[0]:
                        # Empareja con self (clasificador 1)
                        i_cl1 = self.listaAtributosEspecificados.index(refAtt)
                        # Empereja con cl (clasificador 2)
                        i_cl2 = cl.listaAtributosEspecificados.index(refAtt)
                        # Se hace una seleccion aleatoria entre 4 escenarios,
                        # cambiar maximos, cambiar minimos, self absorbe cl
                        # o cl absorbe self
                        llaveTemp = random.randint(0, 3)

                        if llaveTemp == 0:
                            # Cambiar minimos
                            temp = self.condicion[i_cl1][0]
                            self.condicion[i_cl1][0] = cl.condicion[i_cl2][0]
                            cl.condicion[i_cl2][0] = temp

                        elif llaveTemp == 1:
                            # Cambiar maximos
                            temp = self.condicion[i_cl1][1]
                            self.condicion[i_cl1][1] = cl.condicion[i_cl2][1]
                            cl.condicion[i_cl2][1] = temp

                        else:
                            # Se realiza la absorcion
                            todasListas = self.condicion[i_cl1] + cl.condicion[i_cl2]
                            nuevoMin = min(todasListas)
                            nuevoMax = max(todasListas)

                            # self absorbe cl
                            if llaveTemp == 2:
                                self.condicion[i_cl1] = [nuevoMin, nuevoMax]
                                # eliminar cl
                                cl.condicion.pop(i_cl2)
                                cl.listaAtributosEspecificados.remove(refAtt)

                            # cl absorve self
                            else:
                                cl.condicion[i_cl2] = [nuevoMin, nuevoMax]
                                # eliminar self
                                self.condicion.pop(i_cl1)
                                self.listaAtributosEspecificados.remove(refAtt)

                    # -----------------------------------------------------
                    # ATRIBUTO DISCRETO
                    # -----------------------------------------------------
                    else:
                        pass

            # -----------------------------------------------------
            # REVISAR EL LIMITE DE ESPECIFICACION
            # Devuelve la especificacion al limite. Notar que esto es
            # posible para reglas completamente generales que resultan
            # del cruzamiento (la mutacion se asegura que algunos
            # atributos se vuelvan especificados)
            # -----------------------------------------------------
            if len(self.listaAtributosEspecificados) > cons.amb.datosFormateados.limiteEspec:
                self.arregloLimiteEspec(self)

            if len(cl.listaAtributosEspecificados) > cons.amb.datosFormateados.limiteEspec:
                self.arregloLimiteEspec(cl)

            listaTemp1 = copy.deepcopy(p_self_listaAtributosEspecificados)
            listaTemp2 = copy.deepcopy(cl.listaAtributosEspecificados)
            listaTemp1.sort()
            listaTemp2.sort()

            if cambio and (listaTemp1 == listaTemp2):
                cambio = False

            return cambio
        # -----------------------------------------------------
        # CRUZAMIENTO DE FENTOIPO CONTINUO
        # -----------------------------------------------------
        else:
            print("Clasificador - Error: Tangente Penitente no puede manejar endpoints continuos.")

    def arregloLimiteEspec(self, cl):
        """ 
        Baja la especificacion del clasificador al limite de especificacion 
        """
        # Identifica atributos a 'eliminar' con los puntajes de SA
        # mas bajos
        if cons.hacerFeedbackAtributos:
            while len(cl.listaAtributosEspecificados) > cons.amb.datosFormateados.limiteEspec:
                valorMin = cons.SA.obtenerProbSeguimiento()[cl.listaAtributosEspecificados[0]]
                atributoMin = cl.listaAtributosEspecificados[0]

                for j in cl.listaAtributosEspecificados:
                    if cons.SA.obtenerProbSeguimiento()[j] < valorMin:
                        valorMin = cons.SA.obtenerProbSeguimiento()[j]
                        atributoMin = j

                # Referencia a la posicion del atributo en la
                # representacion de reglas
                i = cl.listaAtributosEspecificados.index(atributoMin)
                cl.listaAtributosEspecificados.remove(atributoMin)
                # construirCoincidencia maneja atributos continuos y discretos
                cl.condicion.pop(i)

        # Aleatoriamente selecciona atributos a 'eliminar'
        # para que sean generalizados
        else:
            eliminar = len(cl.listaAtributosEspecificados) - cons.amb.datosFormateados.limiteEspec
            objetivoGen = random.sample(cl.listaAtributosEspecificados, eliminar)

            for j in objetivoGen:
                # Referencia a la posicion del atributo en la
                # representacion de reglas
                i = cl.listaAtributosEspecificados.index(j)
                cl.listaAtributosEspecificados.remove(j)
                # construirCoincidencia maneja atributos continuos y discretos
                cl.condicion.pop(i)

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
