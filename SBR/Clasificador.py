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
        """ Muta la condicion del clasificador. Tambien maneja 
        mutacion del fenotipo. Esto es una mutacion de niche, lo
        que significa que el clasificador resultante todavia
        coincidira con la instancia actual. """

        # Probabilidad de que si el CE es activado, entonces
        # sea aplicado
        probPresion = 0.5
        usarSA = False

        if cons.hacerFeedbackAtributos and random.random() < cons.SA.porcentaje:
            usarSA = True

        cambio = False

        # -----------------------------------------------------
        # CONDICION DE MUTACION
        # Ratio de mutacion (upsilon) usado para probabilisticamente
        # determinar el numero de atributos que deberan ser mutados
        # en el clasificador
        # -----------------------------------------------------

        pasos = 0
        continuar = True

        while continuar:
            if random.random() < cons.upsilon:
                pasos += 1

            else:
                continuar = False

        # Definir limites de especificacion
        if (len(self.listaAtributosEspecificados) - pasos) <= 1:
            limiteBajo = 1

        else:
            limiteBajo = len(self.listaAtributosEspecificados) - pasos

        if (len(self.listaAtributosEspecificados) + pasos) >= cons.amb.datosFormateados.limiteEspec:
            limiteAlto = cons.amb.datosFormateados.limiteEspec

        else:
            limiteAlto = len(self.listaAtributosEspecificados) + pasos

        if len(self.listaAtributosEspecificados) == 0:
            limiteAlto = 1

        # Obtener una nueva especificacion de regla
        nuevaEspecRegla = random.randint(limiteBajo, limiteAlto)

        # -----------------------------------------------------
        # MANTENER ESPECIFICACION
        # -----------------------------------------------------
        # Selecciona una tributo para generlizar y otro para
        # especificar. Mantiene la especificacion de las reglas iguales
        if nuevaEspecRegla == len(self.listaAtributosEspecificados) and random.random() < (1 - cons.upsilon):
            # Identificar objetivo generalizante
            if not cons.usarConocimientoExperto or random.random() > probPresion:
                objetivoGen = random.sample(self.listaAtributosEspecificados, 1)

            else:
                objetivoGen = self.selecGeneralizarRW(1)

            infoAtributo = cons.amb.datosFormateados.infoAtributo[objetivoGen[0]]

            if not infoAtributo[0] or random.random() > 0.5:
                # Generalizar objetivo
                if not usarSA or random.random() > cons.SA.obtenerProbSeguimiento()[objetivoGen[0]]:
                    # Referencia a la posicion del atributo en la representacion de reglas
                    i = self.listaAtributosEspecificados.index(objetivoGen[0])
                    self.listaAtributosEspecificados.remove(objetivoGen[0])
                    # constuirCoincidencia maneja atributos discretos y continuos
                    self.condicion.pop(i)
                    cambio = True

            else:
                self.mutarAtributosContinuos(usarSA, objetivoGen[0])

            # Identificar objetivo especificador
            # Revision para conjuntos de datos pequenos, si todos
            # los atributos han sido especificados en este punto
            if len(self.listaAtributosEspecificados) >= len(estado):
                pass

            else:
                if not cons.usarConocimientoExperto or random.random() > probPresion:
                    listaOpciones = list(range(cons.amb.datosFormateados.numAtributos))

                    # Hace una lista con todos los atributos no especificados
                    for i in self.listaAtributosEspecificados:
                        listaOpciones.remove(i)

                    objetivoEspec = random.sample(listaOpciones, 1)

                else:
                    objetivoEspec = self.selecGeneralizarRW(1)

                if estado[objetivoEspec[0]] != cons.etiquetaDatosFaltantes and (not usarSA or random.random() < cons.SA.obtenerProbSeguimiento()[objetivoEspec[0]]):
                    # Objetivo especificacion
                    self.listaAtributosEspecificados.append(objetivoEspec[0])
                    self.condicion.append(self.construirCoincidencia(objetivoEspec[0], estado))
                    cambio = True

                if len(self.listaAtributosEspecificados) > cons.amb.datosFormateados.limiteEspec:
                    self.arregloLimiteEspec(self)

        # -----------------------------------------------------
        # INCREMENTA ESPECIFICACION
        # -----------------------------------------------------
        elif nuevaEspecRegla > len(self.listaAtributosEspecificados):
            # Especifica mas atributos
            cambio = nuevaEspecRegla - len(self.listaAtributosEspecificados)
            
            if not cons.usarConocimientoExperto or random.random() > probPresion:
                listaOpciones = list(range(cons.amb.datosFormateados.numAtributos))

                for i in self.listaAtributosEspecificados:
                    # Hacer lista con todos los atributos no especificados
                    listaOpciones.remove(i)

                objetivoEspec = random.sample(listaOpciones, cambio)

            else:
                objetivoEspec = self.selecGeneralizarRW(cambio)

            for j in objetivoEspec:
                if estado[j] != cons.etiquetaDatosFaltantes and (not usarSA or random.random() < cons.SA.obtenerProbSeguimiento()[j]):
                    self.listaAtributosEspecificados.append(j)
                    self.condicion.append(self.construirCoincidencia(j, estado))
                    cambio = True

        # -----------------------------------------------------
        # DECREMENTA ESPECIFICACION
        # -----------------------------------------------------
        elif nuevaEspecRegla < len(self.listaAtributosEspecificados):
            cambio = len(self.listaAtributosEspecificados) - nuevaEspecRegla

            if not cons.usarConocimientoExperto or random.random() > probPresion:
                objetivoGen = random.sample(self.listaAtributosEspecificados, cambio)

            else:
                objetivoGen = self.selecGeneralizarRW(cambio)

            # -----------------------------------------------------
            # ATRIBUTO CONTINUO O DISCRETO
            # Elimina la especificacion del atributo con un 50% de
            # probabilidad si tenemos atributos continuos o 100%
            # si es un atributo discreto
            # -----------------------------------------------------
            for j in objetivoGen:
                infoAtributo = cons.amb.datosFormateados.infoAtributo[j]

                if not infoAtributo[0] or random.random() > 0.5:
                    if not usarSA or random.random() > cons.SA.obtenerProbSeguimiento()[j]:
                        i = self.listaAtributosEspecificados.index(j)
                        self.listaAtributosEspecificados.remove(j)
                        self.condicion.pop(i)
                        cambio = True

                else:
                    self.mutarAtributosContinuos(usarSA, j)
        
        else:
            # No especificar ni generalizar
            pass

        # -----------------------------------------------------
        # MUTAR FENOTIPO
        # -----------------------------------------------------
        if cons.amb.datosFormateados.fenotipoDiscreto:
            pass

        else:
            print("Clasificador - Error: Tangente Penitente no puede manejar endpoints continuos")

        if cambio:
            return True

    def selecGeneralizarRW(self, conteo):
        """ CE es aplicado a la seleccion de un atributo
        para generalizar la mutacion """
        sumaPuntajeCE = 0
        listaSeleccion = []
        conteoActual = 0
        listaAtributosEspecificados = copy.deepcopy(self.listaAtributosEspecificados)

        for i in self.listaAtributosEspecificados:
            # Cuando se generaliza, el CE es inversamente proporcional
            # a la probabilidad de seleccion 
            sumaPuntajeCE += 1 / float(cons.CE.puntajes[i] + 1)

        while conteoActual < conteo:
            puntoOpcion = random.random() * sumaPuntajeCE
            i = 0
            sumaPuntaje = 1 / float(cons.CE.puntajes[listaAtributosEspecificados[i]] + 1)

            while puntoOpcion > sumaPuntaje:
                i = i + 1
                sumaPuntaje += 1 / float(cons.CE.puntajes[listaAtributosEspecificados[i]] + 1)
            
            listaSeleccion.append(listaAtributosEspecificados[i])
            sumaPuntajeCE -= 1 / float(cons.CE.puntajes[listaAtributosEspecificados[i]] + 1)
            listaAtributosEspecificados.pop(i)
            conteoActual += 1

        return listaSeleccion

    def selectEspecificoRW(self, conteo):
        """ CE aplicado a la seleccion de un atributo
        para especificar para mutacion. """

        listaOpciones = list(range(cons.amb.datosFormateados.numAtributos))

        # Hacer lista con atributos no especificados
        for i in self.listaAtributosEspecificados:
            listaOpciones.remove(i)

        sumaPuntajesCE = 0
        listaSeleccion = []
        conteoActual = 0

        for i in listaOpciones:
            sumaPuntajesCE += cons.CE.puntajes[i]

        while conteoActual < conteo:
            puntoOpcion = random.random() * sumaPuntajesCE
            i = 0
            sumaPuntaje = cons.CE.puntajes[listaOpciones[i]]

            while puntoOpcion > sumaPuntaje:
                i = i + 1
                sumaPuntaje += cons.CE.puntajes[listaOpciones[i]]

            listaSeleccion.append(listaOpciones[i])
            sumaPuntajesCE -= cons.CE.puntajes[listaOpciones[i]]
            listaOpciones.pop(i)
            conteoActual += 1

        return listaSeleccion

    def mutarAtributosContinuos(self, usarSA, j):
        # -----------------------------------------------------
        # MUTAR ATRIBUTOS CONTINUOS
        # -----------------------------------------------------

        if usarSA:
            # Alta probabilidad de seguimiento de atributos lleva a una
            # alta probabilidad de mutacion
            if random.random() < cons.SA.obtenerProbSeguimiento()[j]:
                rangoAtt = float(cons.amb.datosFormateados.infoAtributo[j][1][1]) - float(cons.amb.datosFormateados.infoAtributo[j][1][0])
                # Referencia a la posicion del atributo en la representacion de reglas
                i = self.listaAtributosEspecificados.index(j)

                rangoMutacion = random.random() * 0.5 * rangoAtt

                # Mutacion minima
                if random.random() > 0.5:
                    # Sumar
                    if random.random() > 0.5:
                        self.condicion[i][0] += rangoMutacion

                    # Restar
                    else:
                        self.condicion[i][0] -= rangoMutacion

                # Mutacion maxima
                else:
                    # Sumar
                    if random.random() > 0.5:
                        self.condicion[i][1] += rangoMutacion

                    # Restar
                    else:
                        self.condicion[i][1] -= rangoMutacion

                # Reparar rango de tal forma que primero viene el minimo
                # especificado y el maximo despues
                self.condicion[i].sort()
                cambio = True
        
        elif random.random() > 0.5:
            # Mutar rango continuo
            # Basado en Bacardit 2009 - Selecciona un limite con probabilidad
            # uniforme y suma o resta un offset generado aleatoriamente al limite
            # de un tamano entre 0 al 50% del dominio del atributo
            rangoAtt = float(cons.amb.datosFormateados.infoAtributo[j][1][1]) - float(cons.amb.datosFormateados.infoAtributo[j][1][0])
            i = self.listaAtributosEspecificados.index(j)
            rangoMutacion = random.random() * 0.5 * rangoAtt

            # Maxima mutacion
            if random.random() > 0.5:
                # Sumar
                if random.random() > 0.5:
                    self.condicion[i][0] += rangoMutacion

                # Restar
                else:
                    self.condicion[i][0] -= rangoMutacion

            # Minima mutacion
            else:
                # Sumar
                if random.random() > 0.5:
                    self.condicion[i][1] += rangoMutacion

                # Restar
                else:
                    self.condicion[i][1] -= rangoMutacion

            self.condicion[i].sort()
            cambio = True

        else:
            pass

    def revisarRangos(self):
        """Revisa y previene el escenario donde atributos continuos
        especificados en una regla tengan un rango tal que encierren
        completamente el conjunto de entrenamiento para ese atributo
        """

        for refAtt in self.listaAtributosEspecificados:
            if cons.amb.datosFormateados.infoAtributo[refAtt][0]:
                verdaderoMin = cons.amb.datosFormateados.infoAtributo[refAtt][1][0]
                verdaderoMax = cons.amb.datosFormateados.infoAtributo[refAtt][1][1]

                i = self.listaAtributosEspecificados.index(refAtt)

                valorBuffer = (verdaderoMax - verdaderoMin) * 0.1

                # El rango de la regla encierra el rango entero de entrenamiento
                if self.condicion[i][0] <= verdaderoMin and self.condicion[i][1] >= verdaderoMax:
                    self.listaAtributosEspecificados.remove(refAtt)
                    self.condicion.pop(i)
                    return

                elif self.condicion[i][0] + valorBuffer < verdaderoMin:
                    self.condicion[i][0] = verdaderoMin - valorBuffer

                elif self.condicion[i][1] - valorBuffer > verdaderoMax:
                    self.condicion[i][1] = verdaderoMin + valorBuffer

                else:
                    pass

    # -----------------------------------------------------
    # METODOS DE SUBSUNCION
    # -----------------------------------------------------
    def subsumir(self, cl):
        """ Devuelve si el clasificador (self) subsume a cl """
        # -----------------------------------------------------
        # FENOTIPO DISCRETO
        # -----------------------------------------------------
        if cons.amb.datosFormateados.fenotipoDiscreto:
            if cl.fenotipo == self.fenotipo:
                if self.esSubsumidor() and self.esMasGeneral(cl):
                    return True
            
            return False

        # -----------------------------------------------------
        # FENOTIPO CONTINUO
        # -----------------------------------------------------
        else:
            print("Clasificador - Error: Tangente Penitente no puede manejar endpoints continuos.")

    def esSubsumidor(self):
        """ Devuelve si el clasificador (self) es un posible
        subsumidor. Un clasificador debe tener suficiente experiencia
        (una epoca) y tambien debe ser igual o mas preciso que el 
        clasificador que esta tratando de subsumir. """
        if self.conteoCoincidencia > cons.theta_sub and self.precision > cons.acc_sub:
            return True

        return False

    def esMasGeneral(self, cl):
        """ Devuelve si es clasificador (self) es mas general que
        cl. Revisa que todos los atributos especificados en self
        tambien esten especificados en cl. """
        if len(self.listaAtributosEspecificados) >= len(cl.listaAtributosEspecificados):
            return False

        # Revisar cada atributo especificado en self.condicion
        for i in range(len(self.listaAtributosEspecificados)):
            infoAtributo = cons.amb.datosFormateados.infoAtributo[self.listaAtributosEspecificados[i]]

            if self.listaAtributosEspecificados[i] not in cl.listaAtributosEspecificados:
                return False

            # -----------------------------------------------------
            # ATRIBUTO CONTINUO
            # -----------------------------------------------------
            if infoAtributo[0]:
                otraRef = cl.listaAtributosEspecificados.index(self.listaAtributosEspecificados[i])
                # Si self tiene un rango mas angosto que los valores que trata de subsumir
                if self.condicion[i][0] < cl.condicion[otraRef][0]:
                    return False

                if self.condicion[i][1] > cl.condicion[otraRef][1]:
                    return False

        return True

    # -----------------------------------------------------
    # METODO DE ELIMINACION
    # -----------------------------------------------------
    def obtenerProbEliminacion(self, aptitudMedia):
        """Devuelve el voto de eliminacion de un clasificador """

        if self.aptitud/self.numerosidad >= cons.delta * aptitudMedia or self.conteoCoincidencia < cons.theta_del:
            self.votoEliminacion = self.tamanoPromedioConjuntoCoincidencia * self.numerosidad

        elif self.aptitud == 0.0:
            self.votoEliminacion = self.tamanoPromedioConjuntoCoincidencia * self.numerosidad * aptitudMedia / (cons.aptitudInicial/self.numerosidad)

        else:
            self.votoEliminacion = self.tamanoPromedioConjuntoCoincidencia * self.numerosidad * aptitudMedia / (self.aptitud/self.numerosidad)

        return self.votoEliminacion

    # -----------------------------------------------------
    # OTROS METODOS
    # -----------------------------------------------------
    def construirCoincidencia(self, refAtt, estado):
        """ Cosntruye un elemento de condicion de coincidencia
        dado un atributo para ser especificado para el metodo 
        coveringClasificador"""

        infoAtributo = cons.amb.datosFormateados.infoAtributo[refAtt]

        # -----------------------------------------------------
        # ATRIBUTO CONTINUO
        # -----------------------------------------------------
        if infoAtributo[0]:
            rangoAtt = infoAtributo[1][1] - infoAtributo[1][0]
            # Inicializacion continua del radio del dominio
            radioRango = random.randint(25, 75) * 0.01 * rangoAtt / 2.0

            bajo = estado[refAtt] - radioRango
            alto = estado[refAtt] + radioRango

            # Representacion ALKR
            # Inicializacion centrada en una instancia de entrenamiento
            # con un rango entre 25% y 75% del tamano del dominio
            listaCondicion = [bajo, alto]

        # -----------------------------------------------------
        # ATRIBUTO DISCRETO
        # -----------------------------------------------------
        else:
            # El estado ya esta formateado como GABIL en GestionDatos
            listaCondicion = estado[refAtt]

        return listaCondicion

    def equivalente(self, cl):
        """ Devuelve si dos clasificadores son identicos en
        condicion y fenotipo. Esto funciona para atributos o fenotipos
        discretos y continuos. 
        """

        # ¿Son los fenotipos los mismos y tienen el mismo numero de
        # atributos especificados? - revision rapida
        if cl.fenotipo == self.fenotipo and len(cl.listaAtributosEspecificados) == len(self.listaAtributosEspecificados):
            refsCl = sorted(cl.listaAtributosEspecificados)
            refsSelf = sorted(self.listaAtributosEspecificados)

            if refsCl == refsSelf:
                for i in range(len(cl.listaAtributosEspecificados)):
                    indiceTemp = self.listaAtributosEspecificados.index(cl.listaAtributosEspecificados[i])

                    if cl.condicion[i] == self.condicion[indiceTemp]:
                        pass

                    else:
                        return False
                
                return True
            
        return False

    # -----------------------------------------------------
    # ACTUALIZACION DE PARAMETROS
    # -----------------------------------------------------
    def actualizarEstadoEpoca(self, iterExploracion):
        """ Determina cuando una epoca de aprendizaje ha
        sido completada (un ciclo a travez de los datos de
        entrenamiento). """

        if not self.epocaCompletada and (iterExploracion - self.estampaTiempoInic - 1) >= cons.amb.datosFormateados.numInstanciasEntrenamiento and cons.datosOffline:
            self.epocaCompletada = True

    def actualizarAptitud(self):
        """ Actualiza el parametro de aptitud """

        if cons.amb.datosFormateados.fenotipoDiscreto or (self.fenotipo[1] - self.fenotipo[0])/cons.amb.datosFormateados.rangoFenotipo < 0.5:
            self.aptitud = pow(self.precision, cons.nu)

        else:
            print("Clasificador - Error: Tangente Penitente no puede manejar endpoints continuos.")

    def actualizarExperiencia(self):
        """ Incrementa la experiencia de un clasificador en uno.
        Una vez se completa una epoca, la precision de la regla
        no puede cambiar. """
        self.conteoCoincidencia += 1

        # Al completar una epica, el numero de coincidencias
        # de una regla unica no cambiara, asi que se repite
        # el calculo
        if self.epocaCompletada:
            pass

        else:
            self.cubrimientoCoincidencia += 1

    def actualizarCorrectos(self):
        """ Incrementa el seguimiento de fenotipo correcto en uno.
        Al completar una epoca, la precision de la regla no puede cambiar. """

        self.conteoCorrecto += 1

        if self.epocaCompletada:
            pass

        else:
            self.cubrimientoCorrecto += 1

    def actualizarNumerosidad(self, num):
        """ Altera el numero de numerosidad de un clasificador.
        La numerosidad no puede ser negativa"""
        self.numerosidad += num

    def actualizarTamanoConjuntoCoincidencia(self, tamanoConjuntoCoincidencia):
        """ Actualiza el tamano del conjunto de coincidencias promedio """
        if self.conteoCoincidencia < 1.0 / cons.beta:
            self.tamanoPromedioConjuntoCoincidencia = (self.tamanoPromedioConjuntoCoincidencia * (self.conteoCoincidencia - 1) + tamanoConjuntoCoincidencia) / float(self.conteoCoincidencia)

        else:
            self.tamanoPromedioConjuntoCoincidencia = self.tamanoPromedioConjuntoCoincidencia + cons.beta * (tamanoConjuntoCoincidencia - self.tamanoPromedioConjuntoCoincidencia)

    def actualizarEstampaTiempo(self, ts):
        """ Fija la estampa de tiempo del clasificador """
        self.estampaTiempoAG = ts

    def actualizarPrecision(self):
        """ Actualiza el seguimiento de la precision """
        self.precision = self.conteoCorrecto / float(self.conteoCoincidencia)

    def fijarPrecision(self, precision):
        pass

    def fijarAptitud(self, apt):
        pass

    def imprimirClasificador(self):
        pass
