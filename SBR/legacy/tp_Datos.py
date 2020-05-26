"""
TANGENTE PENITENTE
Nombre: tp_Datos.py
Descripcion: Carga el conjunto de datos, caracteriza y almacena las características 
             críticas de los conjuntos de datos (incluyendo los atributos discretos 
             frente a los continuos y el fenotipo), maneja los datos que faltan y, 
             finalmente, da formato a los datos para que puedan ser convenientemente 
             utilizados por Tangente Penitente.
"""

# Importar modulos requeridos
import math
import random
import sys
from tp_Constantes import * 
# 

class GestionDatos:
    def __init__(self, archivoEntrenamiento, archivoPrueba, listaInfor = None):
        # Fijar la semilla aleatoria si se especifica
        if cons.usarSemilla:
            random.seed(cons.semillaAleatoria)

        else:
            random.seed(None)
            
        if cons.datosOffline:
            # Inicializar variables globales
            self.numAtributos = None # Guarda el numero de atributos del archivo de entrada
            self.sonIDsInstancia = False
            self.refIDInstancia = None
            self.refFenotipo = None
            self.fenotipoDiscreto = True 
            self.infoAtributos = [] # Guarda discreto (0) vs. continuo (1)
            self.listaFenotipos = [] # Guarda valores discretos del fenotipo O para fenotipos continuos, valores max. y min.
            self.seleccAleatoriaFenotipo = None # Se utiliza para aproximar la precisión de la selección de fenotipos aleatorios.
            self.rangoFenotipo = None
            self.fenoDE = None
            self.etiquetaDatosFaltantes = cons.etiquetaDatosFaltantes
            self.listaEndpointsFaltantes = []
            
            # Especificos al entrenamiento/prueba
            self.listaEncabezadosEntrenamiento = []
            self.listaEncabezadosPrueba = []
            self.numInstanciasEntrenamiento = None 
            self.numInstanciasPrueba = None 
            self.conteoEstadosPromedio = None     
            
            self.conteoDiscretos = 0
            self.conteoContinuos = 0
            self.conteoClases = {}
            self.pesosPrediccionClases = {}

            # Detectar caracteristicas de los datos de entrenamiento
            print("----------------------------------------------------------------------------")
            print("Ambiente: Formateando datos... ")
            
            datosEntrenamientoCrudos = self.cargarDatos(archivoEntrenamiento+'.txt', True) # Carga los datos crudos
    
            self.caracterizarConjuntodatos(datosEntrenamientoCrudos)  # Detecta el numero de atributos, instancias y ubicaciones de las referencias

            if cons.archivoPrueba == 'None': # Si no hay datos de prueba, el formateo recae solamente en los datos de entrenamiento                
                datosParaFormatear = datosEntrenamientoCrudos

            else:
                datosPruebaCrudos = self.cargarDatos(archivoPrueba + '.txt', False) # Carga los datos crudos
                self.compararConjuntodatos(datosPruebaCrudos) # Asegurarse de que las características principales son las mismas entre los conjuntos de datos de entrenamiento y de prueba.
    
            self.discriminarFenotipo(datosEntrenamientoCrudos) # Determina si el endpoint/fenotipo es continuo o discreto

            if self.fenotipoDiscreto:
                self.discriminarClases(datosEntrenamientoCrudos) # Detecta el numero de identificadores unicos del fenotipo

            else:
                print("GestionDatos - Error: Tangente Penitente no puede manejar fenotipos continuos.")
                
            self.discriminarAtributos(datosEntrenamientoCrudos) # Detecta si los atributos son discretos o continuos.
            self.caracterizarAtributos(datosEntrenamientoCrudos) # Determina los posibles estados o rangos de los atributos.
            
            # Regla Límite de especificidad (REL/RSL)
            if cons.RSL_Override > 0:
                self.limiteEspec = cons.RSL_Override

            else:
                # Calcular el REL
                print("GestionDatos: Estimación del límite de la especificación del clasificador...")

                i = 1
                combinacionesUnicas = math.pow(self.conteoEstadosPromedio, i)

                while combinacionesUnicas < self.numInstanciasEntrenamiento:
                    i += 1
                    combinacionesUnicas = math.pow(self.conteoEstadosPromedio,i)

                self.limiteEspec = i

                if self.numAtributos < self.limiteEspec:  # Nunca permitir que el limiteEspec sea mayor que el número de atributos en el conjunto de datos
                    self.limiteEspec = self.numAtributos

            print("GestionDatos: Limite de la Especificacion = "+str(self.limiteEspec))
            
            # Formatear y barajar el conjuntos de datos
            if cons.archivoPrueba != 'None':
                self.pruebaFormateados = self.formatearDatos(datosPruebaCrudos, False) # Almacena el conjunto de datos de prueba formateados utilizados en todo el algoritmo

            self.entrenamientoFormateados = self.formatearDatos(datosEntrenamientoCrudos, True) #Almacena el conjunto de datos de entrenamiento formateados utilizados en todo el algoritmo.      
            
            print("----------------------------------------------------------------------------")

        else:
            # Inicializar variables globales
            self.numAtributos = listaInfor[0]
            self.sonIDsInstancia = False
            self.refIDInstancia = None
            self.refFenotipo = None
            self.fenotipoDiscreto = listaInfor[1]
            self.infoAtributos = listaInfor[2] # Guarda discreto (0) vs. continuo (1)
            self.listaFenotipos = listaInfor[3] # Guarda valores discretos del fenotipo O para fenotipos continuos, valores max. y min.
            self.rangoFenotipo = listaInfor[4]
            self.listaEncabezadosEntrenamiento = listaInfor[5]
            self.numInstanciasEntrenamiento = listaInfor[6]
            self.limiteEspec = 7
        
    def cargarDatos(self, archivoDatos, hacerEntrenamiento):
        """ Carga el archivo de datos """

        print("GestionDatos: Cargando datos... " + str(archivoDatos))
        listaConjuntosdatos = []

        try:       
            f = open(archivoDatos,'rU')

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('No se pudo abrir', archivoDatos)
            raise 

        else:
            if hacerEntrenamiento:
                self.listaEncabezadosEntrenamiento = f.readline().rstrip('\n').split(' ')   # Eliminar la primera fila

            else:
                self.listaEncabezadosPrueba = f.readline().rstrip('\n').split(' ')   # Eliminar la primera fila

            for linea in f:
                lineList = linea.strip('\n').split(' ')
                listaConjuntosdatos.append(lineList)

            f.close()

        return listaConjuntosdatos
    
    def caracterizarConjuntodatos(self, rawTrainData):
        " Detecta parametros basicos del conjunto de datos " 

        # Detecte los IDs de las instancias y guarda la ubicación si se producen
        if cons.etiquetaIDInstancia in self.listaEncabezadosEntrenamiento:
            self.sonIDsInstancia = True
            self.refIDInstancia = self.listaEncabezadosEntrenamiento.index(cons.etiquetaIDInstancia)

            print("GestionDatos: Ubicacion de la columan de los IDs de instancia = " + str(self.refIDInstancia))

            self.numAtributos = len(self.listaEncabezadosEntrenamiento) - 2 # una columna para IDInstancia y otra para el fenotipo
        
        else:
            self.numAtributos = len(self.listaEncabezadosEntrenamiento) - 1
            
        if cons.etiquetaFenotipo in self.listaEncabezadosEntrenamiento:
            self.refFenotipo = self.listaEncabezadosEntrenamiento.index(cons.etiquetaFenotipo)

            print("GestionDatos: Ubicacion de la columna del fenotipo = " + str(self.refFenotipo))

        else:
            print("GestionDatos - Error: No se encontro la columan del fenotipo. Revisa el conjunto de datos para asegurarse la correcta etiqueta de la columna del fenotipo, o la inclusión en los datos.")

        if self.sonIDsInstancia:
            if self.refFenotipo > self.refIDInstancia:
                self.listaEncabezadosEntrenamiento.pop(self.refFenotipo)
                self.listaEncabezadosEntrenamiento.pop(self.refIDInstancia)

            else:
                self.listaEncabezadosEntrenamiento.pop(self.refIDInstancia)
                self.listaEncabezadosEntrenamiento.pop(self.refFenotipo)

        else:
            self.listaEncabezadosEntrenamiento.pop(self.refFenotipo)
            
        self.numInstanciasEntrenamiento = len(rawTrainData)

        print("GestionDatos: Numero de atributos = " + str(self.numAtributos))
        print("GestionDatos: Numero de instancias = " + str(self.numInstanciasEntrenamiento))


    def discriminarFenotipo(self, rawData):
        """ Determina si el fenotipo es discreto (clases) o continuo """

        print("GestionDatos: Analizando fenotipo...")
        inst = 0
        diccClases = {}

        while len(list(diccClases.keys())) <= cons.limiteAtributoDiscreto and inst < self.numInstanciasEntrenamiento:
            target = rawData[inst][self.refFenotipo]

            if target in list(diccClases.keys()):  # Revisa si ha visto este estado de atributo antes
                diccClases[target] += 1

            elif target == cons.etiquetaDatosFaltantes: # Ignora las filas de datos con endpoints faltantes
                self.listaEndpointsFaltantes.append(inst)

            else: # Nuevo estado observado
                diccClases[target] = 1

            inst += 1

        if len(list(diccClases.keys())) > cons.limiteAtributoDiscreto:
            self.fenotipoDiscreto = False
            self.listaFenotipos = [float(target),float(target)]
            print("GestionDatos: Fenotipo detectado como continuo.")

        else:
            print("GestionDatos: Fenotipo detectado como discreto.")
            
    
    def discriminarClases(self, datosCrudos):
        """ Determina el número de clases y sus identificadores. Sólo se utiliza si el fenotipo es discreto. Requiere tanto el conjunto de datos de entrenamiento como de pruebas para estandarizar el formato en ambos. """

        print("GestionDatos: Detectando clases...")
        inst = 0

        while inst < self.numInstanciasEntrenamiento:
            objetivo = datosCrudos[inst][self.refFenotipo]

            if objetivo in self.listaFenotipos:
                self.conteoClases[objetivo] += 1 # NOTA: Podría potencialmente almacenar información de frecuencia de estado para guiar el aprendizaje.
                self.pesosPrediccionClases[objetivo] += 1

            elif objetivo == cons.etiquetaDatosFaltantes: # Ignorar datos faltantes
                pass

            else:
                self.listaFenotipos.append(objetivo)
                self.conteoClases[objetivo] = 1
                self.pesosPrediccionClases[objetivo] = 1

            inst += 1

        print("GestionDatos: Se detectaron las siguientes clases:")
        print(self.listaFenotipos)
        total = 0

        for each in list(self.conteoClases.keys()):
            total += self.conteoClases[each]
            print("Clase: " + str(each) + " conteo = " + str(self.conteoClases[each]))
            
        for each in list(self.conteoClases.keys()):
            self.pesosPrediccionClases[each] = 1- (self.pesosPrediccionClases[each] /float(total))

        print(self.pesosPrediccionClases)
        
        # Determinación de la selección aleatoria (no adaptada específicamente para el desequilibrio de clases)
        self.seleccAleatoriaFenotipo = 1 / float(len(self.listaFenotipos))
            
                     
    def compararConjuntodatos(self, datosPruebaCrudos):
        " Asegura que los parámetros clave de los conjuntos de datos son de hecho los mismos para el conjunto de datos de entrenamiento y el de pruebas "

        if self.sonIDsInstancia:
            if self.refFenotipo > self.refIDInstancia:
                self.listaEncabezadosPrueba.pop(self.refFenotipo)
                self.listaEncabezadosPrueba.pop(self.refIDInstancia)

            else:
                self.listaEncabezadosPrueba.pop(self.refIDInstancia)
                self.listaEncabezadosPrueba.pop(self.refFenotipo)

        else:
            self.listaEncabezadosPrueba.pop(self.refFenotipo)
            
        if self.listaEncabezadosEntrenamiento != self.listaEncabezadosPrueba:
            print("GestionDatos - Error: Los encabezados de los conjuntos de datos de prueba y de entrenamiento no son los mismos ")

        self.numInstanciasPrueba = len(datosPruebaCrudos)

        print("GestionDatos: Numero de atributos = " + str(self.numAtributos))
        print("GestionDatos: Numero de instancias = " + str(self.numInstanciasPrueba))

    def discriminarAtributos(self, datosCrudos):
        """ Determinar si los atributos son Discretos o Continuos. Requiere tanto el conjunto de datos de entrenamiento como de pruebas para estandarizar el formato en ambos. """

        print("GestionDatos: Detectando atributos...")

        self.conteoDiscretos = 0
        self.conteoContinuos = 0
        
        for att in range(len(datosCrudos[0])):
            if att != self.refIDInstancia and att != self.refFenotipo: # Obtiene sólo las columnas de atributos (ignora las columnas de fenotipo e IDInstancia)
                attIsDiscrete = True
                inst = 0
                stateDict = {}

                while len(list(stateDict.keys())) <= cons.limiteAtributoDiscreto and inst < self.numInstanciasEntrenamiento:  #Checks which discriminate between discrete and continuous attribute
                    if inst in self.listaEndpointsFaltantes: #don't use training instances without endpoint information.
                        inst += 1
                        pass
                    else:
                        target = datosCrudos[inst][att]
                        if target in list(stateDict.keys()):  #Check if we've seen this attribute state yet.
                            stateDict[target] += 1
                        elif target == cons.etiquetaDatosFaltantes: #Ignore missing data
                            pass
                        else: #New state observed
                            stateDict[target] = 1
                        inst += 1

                if len(list(stateDict.keys())) > cons.limiteAtributoDiscreto:
                    attIsDiscrete = False
                if attIsDiscrete:
                    self.infoAtributos.append([0,[]])    
                    self.discreteCount += 1
                else:
                    self.infoAtributos.append([1,[float(target),float(target)]])   #[min,max]
                    self.conteoContinuos += 1
                    
        print("DataManagement: Identified "+str(self.conteoDiscretos)+" discrete and "+str(self.conteoContinuos)+" continuous attributes.") #Debug
            
    def caracterizarAtributos(self, datosCrudos):
        """ Determinar el rango o los estados de cada atributo. Requiere tanto el conjunto de datos de entrenamiento como de pruebas para estandarizar el formato en ambos. """

        print("GestionDatos: Caracterizando atributos...")
        IDAtributo = 0
        self.conteoEstadosPromedio = 0

        for att in range(len(datosCrudos[0])):
            if att != self.refIDInstancia and att != self.refFenotipo:  #Get just the attribute columns (ignores phenotype and instanceID columns)
                for inst in range(len(datosCrudos)):
                    if inst in self.listaEndpointsFaltantes: #don't use training instances without endpoint information.
                        pass
                    else:
                        target = datosCrudos[inst][att]
                        if not self.infoAtributos[IDAtributo][0]: #If attribute is discrete
                            if target in self.infoAtributos[IDAtributo][1] or target == cons.labelMissingData:
                                pass  #NOTE: Could potentially store state frequency information to guide learning.
                            else:
                                self.infoAtributos[IDAtributo][1].append(target)
                                self.averageStateCount += 1
                        else: #If attribute is continuous
                            #Find Minimum and Maximum values for the continuous attribute so we know the range.
                            if target == cons.etiquetaDatosFaltantes:
                                pass
                            elif float(target) > self.infoAtributos[IDAtributo][1][1]:  #error
                                self.infoAtributos[IDAtributo][1][1] = float(target)
                            elif float(target) < self.infoAtributos[IDAtributo][1][0]:
                                self.infoAtributos[IDAtributo][1][0] = float(target)
                            else:
                                pass
                if self.infoAtributos[IDAtributo][0]: #If attribute is continuous
                    self.conteoEstadosPromedio += 2 #Simplify continuous attributes to be counted as two-state variables (high/low) for specLimit calculation.
                IDAtributo += 1
        self.conteoEstadosPromedio = self.conteoEstadosPromedio / float(self.numAtributos)


    def calcSD(self, phenList):
        """  Calculate the standard deviation of the continuous phenotype scores. """
        for i in range(len(phenList)):
            phenList[i] = float(phenList[i])

        avg = float(sum(phenList)/len(phenList))
        dev = []
        for x in phenList:
            dev.append(x-avg)
            sqr = []
        for x in dev:
            sqr.append(x*x)
            
        return math.sqrt(sum(sqr)/(len(sqr)-1))
     
            
    def formatearDatos(self,rawData,training):
        """ Get the data into a format convenient for the algorithm to interact with. Our format is consistent with our rule representation, namely, Attribute-list knowledge representation (ALKR),"""
        formatted = []
        testMissingEndpoints = []
        #Initialize data format---------------------------------------------------------
        for i in range(len(rawData)):  
            formatted.append([None,None,None]) #[Attribute States, Phenotype, InstanceID]

        for inst in range(len(rawData)):
            stateList = []
            attributeID = 0
            for att in range(len(rawData[0])):
                if att != self.refIDInstancia and att != self.refFenotipo:  #Get just the attribute columns (ignores phenotype and instanceID columns)
                    target = rawData[inst][att]
                    
                    if self.infoAtributos[attributeID][0]: #If the attribute is continuous
                        if target == cons.etiquetaDatosFaltantes:
                            stateList.append(target) #Missing data saved as text label
                        else:
                            stateList.append(float(target)) #Save continuous data as floats. 
                    else: #If the attribute is discrete - Format the data to correspond to the GABIL (DeJong 1991)
                        stateList.append(target) #missing data, and discrete variables, all stored as string objects   
                    attributeID += 1
            
            #Final Format-----------------------------------------------
            formatted[inst][0] = stateList                           #Attribute states stored here
            if self.fenotipoDiscreto:
                if not training: #Testing Data Check for Missing Endpoints to exclude from analysis
                    if rawData[inst][self.phenotypeRef] == self.labelMissingData:
                        testMissingEndpoints.append(inst)
                formatted[inst][1] = rawData[inst][self.refFenotipo]        #phenotype stored here
            else:
                print("DataManagement - Error: ExSTraCS 2.0 can not handle continuous endpoints.")
            if self.sonIDsInstancia:
                formatted[inst][2] = rawData[inst][self.instanceIDRef]   #Instance ID stored here
            else: #An instance ID is required to tie instances to attribute tracking scores
                formatted[inst][2] = inst #NOTE ID's are assigned before shuffle - id's capture order of instances in original dataset file.
            #-----------------------------------------------------------
        if training:
            #Remove instances without endpoint information.  We do this here so that automatically added instance identifiers still correspond to original dataset.
            if len(self.listaEndpointsFaltantes) > 0:
                self.listaEndpointsFaltantes.reverse() #Remove from last to first to avoid problems.
                for each in self.listaEndpointsFaltantes:
                    formatted.pop(each)
                self.numInstanciasEntrenamiento = self.numTrainInstances - len(self.listaEndpointsFaltantes) #Correct number of training instances based on number of instances with missing endpoints.
                print("DataManagement: Adjusted Number of Training Instances = " + str(self.numTrainInstances)) #DEBUG
            random.shuffle(formatted) #One time randomization of the order the of the instances in the data, so that if the data was ordered by phenotype, this potential learning bias (based on instance ordering) is eliminated.  
        else:
            if len(testMissingEndpoints) > 0:
                testMissingEndpoints.reverse() #Remove from last to first to avoid problems.
                for each in testMissingEndpoints:
                    formatted.pop(each)
                self.numInstanciasPrueba = self.numTestInstances - len(testMissingEndpoints) #Correct number of training instances based on number of instances with missing endpoints.
                print("DataManagement: Adjusted Number of Testing Instances = " + str(self.numTestInstances)) #DEBUG
        return formatted
    
    
    def saveTempTurfData(self):
        """  Store and preserve original dataset formatting for TuRF EK generation. """
        self.turfformatted = copy.deepcopy(self.entrenamientoFormateados)
        self.turfHeaderList = copy.deepcopy(self.listaEncabezadosEntrenamiento)
        self.turfNumAttributes = copy.deepcopy(self.numAtributos)
        self.tierList = [] #will store attribute names from headerList
        
        
    def returntoFullData(self):
        """ Following TuRF completion, return to orignal complete dataset. """
        self.entrenamientoFormateados = self.turfformatted
        self.listaEncabezadosEntrenamiento = self.turfHeaderList
        self.numAtributos = self.turfNumAttributes
        
    
    def turfDataManagement(self, filterScores, turfPercent):
        """ Add 'Turf' wrapper to any Relief Based algorithm, so that the respective algorithm is run iteratively, each iteration removing 
        a percentage of attributes from consideration, for recalculation of remaining attribute scores. For example, the ReliefF algorithm 
        with this wrapper is called Turf, The SURF algorithm with this wrapper is called SURFnTurf.  The SURF* algorithm with this wrapper 
        is called SURF*nTurf."""
        #Determine number of attributes to remove.
        numRemove = int(self.numAtributos*turfPercent)
        print("Removing "+str(numRemove)+" attribute(s).")
        
        currentFilteredList = []
        #Iterate through data removing lowest each time.
        for i in range(0, numRemove):
            lowVal = min(filterScores)
            lowRef = filterScores.index(lowVal)
            currentFilteredList.append(self.listaEncabezadosEntrenamiento.pop(lowRef))
            self.numAttributes -= 1
            for k in range(self.numTrainInstances):
                self.entrenamientoFormateados[k][0].pop(lowRef)
            filterScores.pop(lowRef)

        self.tierList.append(currentFilteredList) #store filtered attributes as list of removed levels.
        random.shuffle(self.entrenamientoFormateados) #Only makes a difference if a subset of instances is being used for calculations, this way a different subset will be used each time.

        print(str(self.numAtributos) + " remaining after turf iteration.")
        
        if self.numAttributes*float(turfPercent) < 1: #Prevent iterations that do not remove attributes (useful for smaller datasets)
            keepGoing = False
        else:
            keepGoing = True
            
        return keepGoing
    

    def makeFilteredDataset(self, attsInData, fileName, filterScores):
        """ Makes a new dataset, which has filtered out the lowest scoring attributes ( """
        if attsInData > self.numAttributes:
            print("NOTICE: Requested number of attributes ("+str(attsInData)+" in dataset not available.  Returning total number of available attributes instead. ("+str(self.numAtributos)+")")
            attsInData = self.numAtributos
        
        try:  
            dataOut = open(fileName+'_filtered.txt','w') 
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', fileName+'_filtered.txt')
            raise 

        if attsInData < self.numAttributes:
            numRemove = self.numAtributos - attsInData
        else:
            numRemove = 0
        
        #Iterate through data removing lowest each time.
        for i in range(0, numRemove):
            lowRef = 0
            lowVal = filterScores[0]
            for j in range(1,self.numAtributos):
                if filterScores[j] < lowVal:
                    lowVal = filterScores[j]
                    lowRef = j
            #Lowest Value found
            self.listaEncabezadosEntrenamiento.pop(lowRef)
            self.listaEncabezadosPrueba.pop(lowRef)
            self.infoAtributos.pop(lowRef)
            self.numAttributes -= 1
            for k in range(self.numTrainInstances):
                self.entrenamientoFormateados[k][0].pop(lowRef)
            for k in range(self.numTestInstances):
                self.pruebaFormateados[k][0].pop(lowRef)
                
        #numAttributes is now equal to the filtered attribute number specified.
        for i in range(self.numAtributos):
            dataOut.write(self.listaEncabezadosEntrenamiento[i]+'\t')
        dataOut.write('Class'+'\n')
        
        for i in range(self.numTrainInstances):
            for j in range(self.numAtributos):
                dataOut.write(str(self.entrenamientoFormateados[i][0][j])+'\t')
            dataOut.write(str(self.entrenamientoFormateados[i][1])+'\n')

        dataOut.close()
  