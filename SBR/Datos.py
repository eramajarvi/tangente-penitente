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
        # Fijar la semilla aleatoria si se especifica
        if cons.usarSemilla:
            random.seed(cons.semillaAleatoria)

        else:
            random.seed(None)

        if cons.datosOffline:
            # Inicializar variables globales
            self.numAtributos = None
            self.sonIDsIntancia = False
            self.refIDInstancia = None
            self.refFenotipo = None
            self.fenotipoDiscreto = True

            # Se guarda discreto (0) vs. continuo (1)
            self.infoAtributos = []
            # Se guarda valores del fenotipo discreto O para fenotipos continuos, valores max y min
            self.listaFenotipos = []
            # Se usa para aproximar la seleccion de la precision de un fenotipo aleatorio
            self.seleccionAleatoriaFenotipo = None
            self.rangoFenotipo = None
            self.DEFenotipo = None
            self.etiquetaDatosFaltantes = cons.etiquetaDatosFaltantes
            self.listaEndpointsFaltantes = []

            # Especifico para prueba / entrenamiento
            self.listaEncabezadoEntrenamiento = []
            self.listaEncabezadoPrueba = []
            self.numInstanciasEntrenamiento = None
            self.numInstanciasPrueba = None
            self.conteoEstadosPromedio = None

            self.conteoDiscreto = 0
            self.conteoContinuo = 0
            self.conteoClases = {}
            self.pesosPrediccionClases = {}

            # Detectar caracteristicas de los datos de entrenamiento
            print("-----------------------------------------------------")
            print("Ambiente: Formateando datos...")

            # Carga los datos crudos
            datosEntrenamientoCrudos = self.cargarDatos(archivoEntrenamiento + '.txt', True)

            # Detecta el numero de atributos, instancias y ubicaciones de referencia
            self.caracterizarConjuntoDatos(datosEntrenamientoCrudos)

            # Si no hay datos de prueba disponibles, el formateo recae
            # solamente en los datos de entrenamiento
            if cons.archivoPrueba == 'None':
                datosParaFormatear = datosEntrenamientoCrudos

            else:
                # Carga los datos crudos
                datosPruebaCrudos = self.cargarDatos(archivoPrueba + '.txt', False)
                # Se asegura que las caracteristicas principales
                # entre entre los datos de entrenamiento y de 
                # prueba sean las mismas
                self.compararConjuntoDatos(datosPruebaCrudos)

            # Determina si el fenotipo es discreto o continuo
            self.discriminarFenotipo(datosEntrenamientoCrudos)

            if self.fenotipoDiscreto:
                # Detecta el numero de identificadores unicos
                # del fenotipo
                self.discriminarClases(datosEntrenamientoCrudos)

            else:
                print("GestionDatos - Error: Tangente Penitente no puede manejar endpoints continuos")

            # Detecta si los atributos son discretos o continuos
            self.discriminarAtributos(datosEntrenamientoCrudos)
            # Detecta estados o rangos potenciales de los atributos
            self.caracterizarAtributos(datosEntrenamientoCrudos)

            # Limite Especificacion de Reglas (RSL/LER)
            if cons.RSL_Override > 0:
                self.limiteEspec = cons.RSL_Override

            else:
                # Calcula el LER
                print("GestionDatos: Estimando el limite de especificacion de los clasificadores...")

                i = 1
                combinacionesUnicas = math.pow(self.conteoEstadosPromedio, i)

                while combinacionesUnicas < self.numInstanciasEntrenamiento:
                    i += 1
                    combinacionesUnicas = math.pow(self.conteoEstadosPromedio, i)

                self.limiteEspec = i

                # No permitir nunca que el limite de especifiaccion sea mas grande
                # que el numero de atributos en el conjunto de datos
                if self.numAtributos < self.limiteEspec:
                    self.limiteEspec = self.numAtributos

            print("GestionDatos: Limite de Especificacion = " + str(self.limiteEspec))

            # Formatear y barajear el conjunto de datos
            if cons.archivoPrueba != 'None':
                # Se guarda el conjunto de datos de prueba formateado
                # usado en todo el algoritmo
                self.pruebaFormateados = self.formatearDatos(datosPruebaCrudos, False)
                
            # Se guarda el conjunto de datos de entrenamiento formateado
            # usado en todo el algoritmo
            self.entrenamientoFormateados = self.formatearDatos(datosEntrenamientoCrudos, True)

            print("-----------------------------------------------------")

        else:
            # Inicializar variables globales
            self.numAtributos = listaInfo[0]
            self.sonIDsIntancia = False
            self.refIDInstancia = None
            self.refFenotipo = None
            self.fenotipoDiscreto = listaInfo[1]
            self.infoAtributos = listaInfo[2] # Guarda discretos (0) vs continuos (1)
            self.listaFenotipos = listaInfo[3] # Guarda valores del fenotipo discreto O para fenotipos continuos, valores max y min
            self.rangoFenotipo = listaInfo[4]
            self.listaEncabezadoEntrenamiento = listaInfo[5]
            self.numInstanciasEntrenamiento = listaInfo[6]
            self.limiteEspec = 7

    def cargarDatos(self, archivoDatos, hacerEntrenamiento):
        """ Carga el archivo de datos. """

        print("GestionDatos: Cargando datos... " + str(archivoDatos))
        listaConjuntoDatos = []

        try:
            a = open(archivoDatos, 'rU')

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('No se pudo abrir', archivoDatos)

            raise

        else:
            if hacerEntrenamiento:
                self.listaEncabezadoEntrenamiento = a.readline().rstrip('\n').split(' ')

            else:
                self.listaEncabezadoPrueba = a.readline().rstrip('\n').split(' ')

            for linea in a:
                listaLineas = linea.strip('\n').split(' ')
                listaConjuntoDatos.append(listaLineas)

            a.close()

        return listaConjuntoDatos

    def caracterizarConjuntoDatos(self, datosEntrenamientoCrudos):
        """ Detecta parametros basicos del conjunto de datos"""

        # Detecta IDs de instancias y guarda su ubicacion si existen
        if cons.etiquetaIDInstancia in self.listaEncabezadoEntrenamiento:
            self.sonIDsIntancia = True
            self.refIDInstancia = self.listaEncabezadoEntrenamiento.index(cons.etiquetaIDInstancia)
            print("GestionDatos: Ubicacion de la columna de IDs de instancia = " + str(self.refIDInstancia))

            # Una columna para IDs de instancia y otra para el fenotipo
            self.numAtributos = len(self.listaEncabezadoEntrenamiento) - 2

        else:
            self.numAtributos = len(self.listaEncabezadoEntrenamiento) - 1

        if cons.etiquetaFenotipo in self.listaEncabezadoEntrenamiento:
            self.refFenotipo = self.listaEncabezadoEntrenamiento.index(cons.etiquetaFenotipo)

            print("GestionDatos: Ubicacion de la columna del fenotipo = " + str(self.refFenotipo))

        else:
            print("GesitonDatos - Error: No se encontro la columna del fenotipo. Revisa el conjunto de datos para asegurarse que exista una etiqueta de columna de fenotipo correcta.")

        if self.sonIDsIntancia:
            if self.refFenotipo > self.refIDInstancia:
                self.listaEncabezadoEntrenamiento.pop(self.refFenotipo)
                self.listaEncabezadoEntrenamiento.pop(self.refIDInstancia)

            else:
                self.listaEncabezadoEntrenamiento.pop(self.refIDInstancia)
                self.listaEncabezadoEntrenamiento.pop(self.refFenotipo)

        else:
            self.listaEncabezadoEntrenamiento.pop(self.refFenotipo)

        self.numInstanciasEntrenamiento = len(datosEntrenamientoCrudos)

        print("GestionDatos: Numero de atributos = " + str(self.numAtributos))
        print("GestionDatos: Numero de instancias = " + str(self.numInstanciasEntrenamiento))

    def discriminarFenotipo(self, datosCrudos):
        """ Determina si el fenotipo es discreto o continuo """

        print("GestionDatos: Analizando fenotipo...")
        inst = 0
        diccionarioClases = {}

        # Revisa que discrimina entre atirbutos discretos y continuos
        while len(list(diccionarioClases.keys())) <= cons.limiteAtributoDiscreto and inst < self.numInstanciasEntrenamiento:
            objetivo = datosCrudos[inst][self.refFenotipo]

            # Revisa si este estado del atributo se ha visto antes
            if objetivo in list(diccionarioClases.keys()):
                diccionarioClases[objetivo] += 1

            elif objetivo == cons.etiquetaDatosFaltantes:
                self.listaEndpointsFaltantes.append(inst)

            else:
                diccionarioClases[objetivo] = 1

            inst += 1

        if len(list(diccionarioClases.keys())) > cons.limiteAtributoDiscreto:
            self.fenotipoDiscreto = False
            self.listaFenotipos = [float(objetivo), float(objetivo)]
            print("GestionDatos: Fenotipo detectado como continuo.")

        else:
            print("GestionDatos: Fenotipo detectado como discreto")    

    def discriminarClases(self, datosCrudos):
        """ Determina el numero de clases y sus identificadores. Solo
        se usa si el fenotipo es discreto. Requiere el conjunto de datos
        de prueba y de entrenamiento para poder estandarizar el formateo
        en ambos. """

        print("GestionDatos: Detectando clases...")
        inst = 0

        while inst < self.numInstanciasEntrenamiento:
            objetivo = datosCrudos[inst][self.refFenotipo]

            if objetivo in self.listaFenotipos:
                self.conteoClases[objetivo] += 1
                self.pesosPrediccionClases[objetivo] += 1

            elif objetivo == cons.etiquetaDatosFaltantes:
                pass

            else:
                self.listaFenotipos.append(objetivo)
                self.conteoClases[objetivo] = 1
                self.pesosPrediccionClases[objetivo] = 1

            inst +=1 

        print("GestionDatos: Se detectaron las siguientes clases:")
        print(self.listaFenotipos)
        total = 0

        for each in list(self.conteoClases.keys()):
            total += self.conteoClases[each]
            print("Clase: " + str(each) + " conteo = " + str(self.conteoClases[each]))

        for each in list(self.conteoClases.keys()):
            self.pesosPrediccionClases[each] = 1 - (self.pesosPrediccionClases[each] / float(total))

        print(self.pesosPrediccionClases)

        # Determinacion de la seleccion aleatoria
        # No esta especificamente adaptado para clases desbalanceadas
        self.seleccionAleatoriaFenotipo = 1 / float(len(self.listaFenotipos))

    def compararConjuntoDatos(self, datosPruebaCrudos):
        """ Se asegura que los parametros principales del conjunto
        de datos son los mismos para los conjuntos de datos de
        entrenamiento y de prueba"""
        
        if self.sonIDsIntancia:
            if self.refFenotipo > self.refIDInstancia:
                self.listaEncabezadoPrueba.pop(self.refFenotipo)
                self.listaEncabezadoPrueba.pop(self.refIDInstancia)

            else:
                self.listaEncabezadoPrueba.pop(self.refIDInstancia)
                self.listaEncabezadoPrueba.pop(self.refFenotipo)

        else:
            self.listaEncabezadoPrueba.pop(self.refFenotipo)

        if self.listaEncabezadoEntrenamiento != self.listaEncabezadoPrueba:
            print("GestionDatos - Error: Los encabezados del conjunto de datos de prueba y de entrenamiento no son equivalentes")

        self.numInstanciasPrueba = len(datosPruebaCrudos)

        print("GestionDatos: Numero de atributos = " + str(self.numAtributos))
        print("GestionDatos: Numero de instancias = " + str(self.numInstanciasPrueba))

    def discriminarAtributos(self, datosCrudos):
        """ Determina si el atributo es discreto o continuo."""

        print("GestionDatos: Detectando atributos...")
        self.conteoDiscreto = 0
        self.conteoContinuo = 0

        for atributo in range(len(datosCrudos[0])):
            # Obtener solo las columnas de atributos (ignora las
            # columnas del fenotipo y de IDInstancia)
            if atributo != self.refIDInstancia and atributo != self.refFenotipo:
                atirbutoEsDiscreto = True
                inst = 0
                diccionarioEstados = {}

                # Revisa que discrimina entre atributos continuos y discretos
                while len(list(diccionarioEstados.keys())) <= cons.limiteAtributoDiscreto and inst < self.numInstanciasEntrenamiento:
                    # No usar instancias de entrenamiento que no tengan
                    # endpoint definido
                    if inst in self.listaEndpointsFaltantes:
                        inst += 1
                        pass

                    else:
                        objetivo = datosCrudos[inst][atributo]

                        # Revisar si ya se ha visto este estado de atributo
                        # antes
                        if objetivo in list(diccionarioEstados.keys()):
                            diccionarioEstados[objetivo] += 1

                        # Ignorar datos faltantes
                        elif objetivo == cons.etiquetaDatosFaltantes:
                            pass

                        # Nuevo estado observado
                        else:
                            diccionarioEstados[objetivo] = 1

                        inst += 1

                if len(list(diccionarioEstados.keys())) > cons.limiteAtributoDiscreto:
                    atirbutoEsDiscreto = False

                if atirbutoEsDiscreto:
                    self.infoAtributos.append([0, []])
                    self.conteoDiscreto += 1

                else:
                    # Valores minimos y maximos de cada instancia
                    self.infoAtributos.append([1, [float(objetivo), float(objetivo)]])
                    self.conteoContinuo += 1

        print("GestionDatos: Se identificaron " + str(self.conteoDiscreto) + " atributos discretos y " + str(self.conteoContinuo) + " continuos.")

    def caracterizarAtributos(self, datosCrudos):
        """ Determina el rango o estados de cada atributo. """

        print("GestionDatos: Caracterizando atributos...")
        IDAtributo = 0

        self.conteoEstadosPromedio = 0

        for atributo in range(len(datosCrudos[0])):
            # Obtener solo las columnas de atributos
            if atributo != self.refIDInstancia and atributo != self.refFenotipo:
                for inst in range(len(datosCrudos)):
                    # No usar instancias de entrenamiento sin informacion
                    # del endpoint
                    if inst in self.listaEndpointsFaltantes:
                        pass

                    else:
                        objetivo = datosCrudos[inst][atributo]

                        # Si el atributo es discreto
                        if not self.infoAtributos[IDAtributo][0]:
                            if objetivo in self.infoAtributos[IDAtributo][1] or objetivo == cons.etiquetaDatosFaltantes:
                                pass

                            else:
                                self.infoAtributos[IDAtributo][1].append(objetivo)
                                self.conteoEstadosPromedio += 1

                        # Si el atributo es continuo
                        else:
                            # Encuentra valores minimos y maximos del atributo,
                            # de esta forma conocemos el rango
                            if objetivo == cons.etiquetaDatosFaltantes:
                                pass

                            elif float(objetivo) > self.infoAtributos[IDAtributo][1][1]:
                                self.infoAtributos[IDAtributo][1][1] = float(objetivo)

                            elif float(objetivo) < self.infoAtributos[IDAtributo][1][0]:
                                self.infoAtributos[IDAtributo][1][0] = float(objetivo)

                            else:
                                pass

                # Si el atributo es continuo
                if self.infoAtributos[IDAtributo][0]:
                    # Se simplifican los atributos continuos para que
                    # sean contados como variables de dos estados
                    # (max / min) para calculos de limiteEspec
                    self.conteoEstadosPromedio += 2

                IDAtributo += 1

        self.conteoEstadosPromedio = self.conteoEstadosPromedio / float(self.numAtributos)

    def calcularDE(self, listaFenotipos):
        """ Calcula la desviacion estandar para los puntajes
        de fenotipos continuos. """

        for i in range(len(listaFenotipos)):
            listaFenotipos[i] = float(listaFenotipos[i])

        prom = float(sum(listaFenotipos) / len(listaFenotipos))
        desv = []

        for x in listaFenotipos:
            desv.append(x - prom)
            cuad = []

        for x in desv:
            cuad.append(x * x)

        return math.sqrt(sum(cuad) / (len(cuad) - 1))

    def formatearDatos(self, datosCrudos, entrenamiento):
        """ Formatea los datos en una manera conveniente para
        que el algoritmo pueda interactuar con ellos. Este formato
        es consistente con nuestra representacion de reglas, es decir, 
        representacion de conocimiento en listas de atributos. """

        formateados = []
        endpointsPruebaFaltantes = []

        # Inicializar el formateo de datos
        for i in range(len(datosCrudos)):
            # [Estados atributo, Fenotipo, IDInstancia]
            formateados.append([None, None, None])

        for inst in range(len(datosCrudos)):
            listaEstados = []
            IDAtributo = 0

            for atributo in range(len(datosCrudos[0])):
                if atributo != self.refIDInstancia and atributo != self.refFenotipo:
                    objetivo = datosCrudos[inst][atributo]

                    # Si el atributo es continuo
                    if self.infoAtributos[IDAtributo][0]:
                        if objetivo == cons.etiquetaDatosFaltantes:
                            listaEstados.append(objetivo)

                        else:
                            listaEstados.append(float(objetivo))

                    # Si el atributo es discreto - Formatear los datos para que
                    # correspondan con el GABIL (DeJong 1991)
                    else:
                        listaEstados.append(objetivo)

                    IDAtributo += 1

            # Formato final
            formateados[inst][0] = listaEstados
            if self.fenotipoDiscreto:
                if not entrenamiento:
                    if datosCrudos[inst][self.refFenotipo] == self.etiquetaDatosFaltantes:
                        endpointsPruebaFaltantes.append(inst)

                # Fenotipo se guarda aqui
                formateados[inst][1] = datosCrudos[inst][self.refFenotipo]

            else:
                print("GestionDatos - Error: Tangente Penitente no puede manejar endpoints continuos.")

            if self.sonIDsIntancia:
                # IDs de instancia se guardan aqui
                formateados[inst][2] = datosCrudos[inst][self.refIDInstancia]

            else:
                # Un ID de instancia se requiere para amarrar las instancias
                # a los puntajes de seguimiento de los atributos.
                # Los IDs se asignan aqui antes de ser barajeados 
                formateados[inst][2] = inst

        if entrenamiento:
            if len(self.listaEndpointsFaltantes) > 0:
                self.listaEndpointsFaltantes.reverse()

                for each in self.listaEndpointsFaltantes:
                    formateados.pop(each)

                self.numInstanciasEntrenamiento = self.numInstanciasEntrenamiento - len(self.listaEndpointsFaltantes)

                print("GestionDatos: Numero ajustado de instancias de entrenamiento = " + str(self.numInstanciasEntrenamiento))

            # Aleatorizacion de las instancias de los datos, de tal
            # forma que si los datos fueron ordenados por el fenotipo,
            # este potencial sesgo (basado en el ordenamiento de las 
            # instancias) es eliminado
            random.shuffle(formateados)

        else:
            if len(endpointsPruebaFaltantes) > 0:
                endpointsPruebaFaltantes.reverse()

                for each in endpointsPruebaFaltantes:
                    formateados.pop(each)

                self.numInstanciasPrueba = self.numInstanciasPrueba - len(endpointsPruebaFaltantes)
                print("GestionDatos: Numero ajustado de instancias de prueba = " + str(self.numInstanciasPrueba))

        return formateados

    def guardarDatosTurfTemp(self):
        """ Guarda y preserva el formateo original del conjunto de
        datos para generacion de CE Turf. """

        self.turfFormateado = copy.deepcopy(self.entrenamientoFormateados)
        self.turfListaEncabezados = copy.deepcopy(self.listaEncabezadoEntrenamiento)
        self.turfNumAtributos = copy.deepcopy(self.numAtributos)
        self.listaEmpates = [] # Guardara los nombres de los atributos de la lista de encabezados

    def regresarDatosCompletos(self):
        """ Al terminar el TuRF, regresar al conjunto de datos
        completo original """

        self.entrenamientoFormateados = self.turfFormateado
        self.listaEncabezadoEntrenamiento = self.turfListaEncabezados
        self.numAtributos = self.turfNumAtributos

    def gestionDatosTurf(self, puntajesFiltro, porcentajeTurf):
        """ Agrega el envoltorio 'Turf' a cualquier algoritmo
        basado en Relief, de tal forma que el respectivo algorimo
        es ejecutado iterativamente, en cada iteracion se elimina
        un porcentaje de atributos a consideracion, para 
        recalculacion de puntajes de atributos que quedan. Por ejemplo,
        el algorimo ReliefF con este envoltorio se llama Turf, el
        algoritmo SURF con este envoltorio es llamado SURFTurf. """

        numEliminados = int(self.numAtributos * porcentajeTurf)
        print("Eliminado " + str(numEliminados) + " atributo(s). ")

        listaFiltradaActual = []

        for i in range(0, numEliminados):
            valorBajo = min(puntajesFiltro)
            refBajo = puntajesFiltro.index(valorBajo)

            listaFiltradaActual.append(self.listaEncabezadoEntrenamiento.pop(refBajo))
            self.numAtributos -= 1

            for k in range(self.numInstanciasEntrenamiento):
                self.entrenamientoFormateados[k][0].pop(refBajo)

            puntajesFiltro.pop(refBajo)

        # Guarda atributos filtrados como lista de niveles eliminados
        self.listaEmpates.append(listaFiltradaActual)
        # Solo hace la diferencia si un subconjunto de instancias es
        # usada para calculos, de esta forma un subconjunto diferente
        # es usado cada vez.
        random.shuffle(self.entrenamientoFormateados)

        print("Quedan " + str(self.numAtributos) + " atributos despues de iteraciones Turf.")

        if self.numAtributos * float(porcentajeTurf) < 1:
            seguir = False

        else:
            seguir - True

        return seguir

    def hacerConjuntoDatosFiltrado(self, atributosEnDatos, nombreArchivo, puntajesFiltro):
        """ Hace un nuevo conjunto de datos, que tiene filtrados
        los atributos con puntajes mas bajos. """

        if atributosEnDatos > self.numAtributos:
            print("NOTA: El numero solicitado de atributos ( " + str(atributosEnDatos) + " en el conjunto de datos no esta disponible. Regresando al numero total de numero de atributos disponibles. (" + str(self.numAtributos) + ")")
            atributosEnDatos = self.numAtributos

        try:
            salidaDatos = open(nombreArchivo + '_filtrado.txt', 'w')

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('No se pudo abrir', nombreArchivo + '_filtrado.txt')

            raise

        if atributosEnDatos < self.numAtributos:
            numEliminados = self.numAtributos - atributosEnDatos

        else:
            numEliminados = 0

        # Iterar a traves de los datos eliminando el mas bajo cada vez
        for i in range(0, numEliminados):
            refBajo = 0
            valorBajo = puntajesFiltro[0]

            for j in range(1, self.numAtributos):
                if puntajesFiltro[j] < valorBajo:
                    valorBajo = puntajesFiltro[j]
                    refBajo = j

            # Valor mas bajo encontrado
            self.listaEncabezadoEntrenamiento.pop(refBajo)
            self.listaEncabezadoPrueba.pop(refBajo)
            self.infoAtributos.pop(refBajo)
            self.numAtributos -= 1

            for k in range(self.numInstanciasEntrenamiento):
                self.entrenamientoFormateados[k][0].pop(refBajo)

            for k in range(self.numInstanciasPrueba):
                self.pruebaFormateados[k][0].pop(refBajo)

        # numAtributos ahora es igual al numero de atributos filtrados
        for i in range(self.numAtributos):
            salidaDatos.write(self.listaEncabezadoEntrenamiento[i] + '\t')
        
        salidaDatos.write('Clase' + '\n')

        for i in range(self.numInstanciasEntrenamiento):
            for j in range(self.numAtributos):
                salidaDatos.write(str(self.entrenamientoFormateados[i][0][j]) + '\t')

            salidaDatos.write(str(self.entrenamientoFormateados[i][1]) + '\n')

        salidaDatos.close()