"""
TANGENTE PENITENTE
Nombre:      tp_Algoritmo.py
Descripcion: El principal módulo de control de Tangente Penitente. Incluye el bucle 
             de ejecución principal que controla el aprendizaje sobre un número específico 
             de iteraciones. También incluye el seguimiento periódico del rendimiento estimado, 
             y puntos de control donde se realizan evaluaciones completas de la población de 
             reglas de Tangente Penitente.
"""

# Importar modulos requeridos
from tp_Constantes import *
from tp_ConjuntoClasificadores import ConjuntoClasificadores
from tp_Prediccion import *
from tp_SA import *
from tp_CR import CompactacionReglas
from tp_PresicionClases import PresicionClases
from tp_Salida import AdminSalida

import copy
import random
import math
import random
# 

class Algoritmo:
    def __init__(self):
        """ Inicializa el algoritmo de Tangente Penitente """

        print("Algoritmo: Inicializando...")

        # Parametros globales
        self.poblacion = None
        self.salidaSeguimientoAprendizaje = None  # Archivo de salida que guarda la informacion del seguimiento durante el aprendizaje     

        #-------------------------------------------------------
        # REINICIO DE LA POBLACION
        # Inicia el aprendizaje desde una poblacion existente de reglas guardada
        #-------------------------------------------------------  
        
        if cons.hacerReinicioPoblacion: # Si estamos reiniciando desde una poblacion de reglas previamente guardadas           
            try: # Reabrir el archivo de aprendizaje para continuar el seguimiento continuado del progreso
                nombrearchivo = "{}._SeguimientoAprendizaje.txt".format(cons.archivoSalida)
                os.makedirs(os.path.dirname(nombrearchivo), exist_ok=True)
                self.salidaSeguimientoAprendizaje = open(nombrearchivo,'a')

            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('No se pudo abrir', cons.archivoSalida + '_SeguimientoAprendizaje.txt')
                raise

            self.reinicioPoblacion()

        #-------------------------------------------------------
        # TANGENTE PENITENTE NORMAL
        # Ejecuta Tangente Penitente desde cero con los datos dados
        #-------------------------------------------------------
        else:
            try: # Establece el archivo de salida para guardar el progreso de aprendizaje
                nombrearchivo = "{}._SeguimientoAprendizaje.txt".format(cons.archivoSalida)
                os.makedirs(os.path.dirname(nombrearchivo), exist_ok=True)
                self.salidaSeguimientoAprendizaje = open(nombrearchivo,'w')

            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('No se pudo abrir', cons.archivoSalida+'_SeguimientoAprendizaje.txt')
                raise
            else:
                self.salidaSeguimientoAprendizaje.write("Iteracion_Exploracion\tTamanoMacroPob\tTamanoMicroPop\tEstimado_Precision\tGeneralidadProm\tReglasExp\tTiempo(min)\n")

            # Instanciar poblacion
            self.poblacion = ConjuntoClasificadores()
            self.exploreIter = 0
            self.correcto  = [0.0 for i in range(cons.frecuenciaSeguimiento)]
            self.listaPrediccion = [] # Para ir sacando predicciones de prueba crudas
            self.listaReal = []
            self.conjuntoPrediccion = []

    def correrTP(self):
        """ Ejecuta el algoritmo de Tangente Penitente inicializado """
        print("Iniciando iteraciones de aprendizaje")
        print("----------------------------------------------------")

        #-------------------------------------------------------
        # MAYOR BUCLE DE APRENDIZAJE
        #-------------------------------------------------------
        while self.exploreIter < cons.maxiteracionesAprendizaje and not cons.parar:
            #---------------------------------------------------------------------
            # Obtener una nueva instancia y ejecutar una iteracion de aprendizaje
            #---------------------------------------------------------------------
            estadoFenotipo = cons.amb.obtenerInstanciaEntrenamiento()
            self.correrIteracion(estadoFenotipo, self.exploreIter)

            #---------------------------------
            # Evaluaciones del algoritmo
            #---------------------------------
            cons.cronometro.iniciarTiempoEvaluacion()

            #-----------------------------------
            # SEGUIR ESTIMADOS DE APRENDIZAJE
            #-----------------------------------
            if (self.exploreIter % cons.frecuenciaSeguimiento) == (cons.frecuenciaSeguimiento - 1) and self.exploreIter > 0:

                self.poblacion.ejecutarEvalPobProm(self.exploreIter)

                presicionSeguida = sum(self.correcto)/float(cons.frecuenciaSeguimiento) # Presicion sobre el ultimo numero de iteracion de "frecuenciaSeguimiento" 

                self.salidaSeguimientoAprendizaje.write(self.poblacion.obtenerSeguimientoPob(presicionSeguida, self.exploreIter + 1, cons.frecuenciaSeguimiento)) # Reporta el progreso de aprendizaje al archivo de salida estandar y de segumineto

                for observador in cons.llamadasEpoca:
                    observador(self.exploreIter, self.poblacion, presicionSeguida)

            cons.cronometro.detenerTiempoEvaluacion()

            #-------------------------------------------------------------------------------
            # PUNTO DE CONTROL - Evaluacion completa de la poblacion
            # La estrategia de evaluacion es diferente para fenotipos discretos vs continuos
            #-------------------------------------------------------------------------------
            if (self.exploreIter + 1) in cons.puntoscontrolAprendizaje or cons.forzarPuntoControl:

                if(cons.forzarPuntoControl):
                    cons.forzarPuntoControl = False

                cons.cronometro.iniciarTiempoEvaluacion()

                print("-----------------------------------------------------------")
                print("Ejecutando evaluacion de la poblacion despues de " + str(self.exploreIter + 1) + " iteraciones.")
                self.poblacion.ejecutarEvalPobProm(self.exploreIter)
                self.poblacion.ejecutarSumaGeneralidadAtributos()

                cons.amb.iniciarModoEvaluacion()

                if cons.archivoPrueba != 'None': # Si hay un archivo de prueba disponible
                    if cons.amb.datosFormateados.fenotipoDiscreto:
                        evalEntrena = self.hacerEvaluacionPob(True)
                        evalPrueba = self.hacerEvaluacionPob(False)

                    else:
                        print("Algoritmo - Error: Tangente Penitente no puede manejar endpoints continuos")

                elif cons.archivoEntrenamiento != 'None':
                    if cons.amb.datosFormateados.fenotipoDiscreto:
                        evalEntrena = self.hacerEvaluacionPob(True)
                        evalPrueba = None

                    else:
                        print("Algoritmo - Error: Tangente Penitente no puede manejar endpoints continuos.")

                else: # Ambiente online
                    evalEntrena = None
                    evalPrueba = None

                cons.amb.detenerModoEvaluacion() # Se devuelve a la posicion de aprendizaje en los datos de entrenamiento
                cons.cronometro.detenerTiempoEvaluacion()

                #-----------------------------
                # ESCRIBIR ARCHIVOS DE SALIDA
                #-----------------------------
                cons.cronometro.iniciarTiempoArchivoSalida()
                AdminSalida().escribirEstadisticasPob(cons.archivoSalida, evalEntrena, evalPrueba, self.exploreIter + 1, self.poblacion, self.correcto)
                AdminSalida().escribirPob(cons.archivoSalida, self.exploreIter + 1, self.population)
                AdminSalida().occurenciaAttCo(cons.archivoSalida, self.exploreIter + 1, self.population)
                AdminSalida().guardarSeguimiento(self.exploreIter, cons.archivoSalida)
                AdminSalida().escribirPredicciones(self.exploreIter, cons.archivoSalida, self.listaPrediccion, self.listaReal, self.conjuntoPrediccion)
                cons.cronometro.detenerTiempoArchivoSalida()

                #
                for observador in cons.llamadasPuntosControl:
                    observador(evalEntrena, evalPrueba)
                #

                print("Algoritmo: Continua aprendiendo...")
                print("--------------------------------------------------------------------------------")
                #------------------------
                # COMPACTACION DE REGLAS
                #------------------------
                if self.exploreIter + 1 == cons.maxiteracionesAprendizaje and cons.hacerCompactacionReglas:
                    cons.cronometro.iniciarTiempoCompReg()
                    if evalPrueba == None:
                        CompactacionReglas(self.poblacion, evalEntrena[0], None)

                    else:
                        CompactacionReglas(self.poblacion, evalEntrena[0], evalPrueba[0])

                    cons.cronometro.detenerTiempoCompReg()

                    #-----------------------------------------------------
                    # EVALUACION GLOBAL DE POBLACION DE REGLAS COMPACTADA
                    #-----------------------------------------------------
                    cons.cronometro.iniciarTiempoEvaluacion()
                    self.poblacion.recalculateNumerositySum()
                    self.poblacion.runPopAveEval(self.exploreIter)
                    self.poblacion.runAttGeneralitySum()
                    #----------------------------------------------------------

                    cons.amb.iniciarModoEvaluacion()

                    if cons.archivoPrueba != 'None': # Si hay disponible un archivo de prueba
                        if cons.env.datosFormateados.fenotipoDiscreto:
                            evalEntrena = self.hacerEvaluacionPob(True)
                            evalPrueba = self.hacerEvaluacionPob(False)

                        else:
                            print("Algoritmo - Error: Tangente Penitente no puede manipular endpoints continuos")
                    else:
                        if cons.env.formatData.discretePhenotype:
                            evalEntrena = self.hacerEvaluacionPob(True)
                            evalPrueba = None

                        else:
                            print("Algoritmo - Error: Tangente Penitente no puede manipular endpoints continuos")

                    cons.amb.detenerModoEvaluacion()
                    cons.cronometro.detenerTiempoEvaluacion()

                    #-----------------------------
                    # ESCRIBIR ARCHIVOS DE SALIDA
                    #-----------------------------
                    cons.cronometro.iniciarTiempoArchivoSalida()

                    AdminSalida().escribirEstadisticasPob(cons.archivoSalida + "_CR_" + cons.metodoCompactacionReglas, evalEntrena, evalPrueba, self.exploreIter + 1, self.population, self.correcto)
                    AdminSalida().escribirPob(cons.archivoSalida + "_CR_" + cons.metodoCompactacionReglas, self.exploreIter + 1, self.population)
                    AdminSalida().occurenciaAttCo(cons.archivoSalida + "_CR_" + cons.metodoCompactacionReglas, self.exploreIter + 1, self.population)
                    AdminSalida().escribirPredicciones(self.exploreIter, cons.archivoSalida + "_RC_" + cons.metodoCompactacionReglas, self.listaPrediccion, self.listaReal, self.conjuntoPrediccion)
                    cons.cronometro.detenerTiempoArchivoSalida()

            #
            for observador in cons.iterationCallbacks:
                observador()
            #

            #-----------------------------------------------------
            # AJUSTAR VALORES MAYORES PARA LA SIGUIENTE ITERACION
            #-----------------------------------------------------
            self.exploreIter += 1
            cons.amb.nuevaInstancia(True) # Mover a la siguiente instancia en el conjunto de entrenamiento

        # Una vez Tangente Penitente ha alcanzado la ultima iteracion de aprendizaje, cerrar el archivo de seguimiento
        self.salidaSeguimientoAprendizaje.close()
        print("Ejecucion de Tangente Penitente completada")


    def correrIteracion(self, estado_fenotipo, exploreIter):
        """ Ejecuta una unica iteracion de aprendizaje """
        #------------------------------------
        # FORMA UN CONJUNTO DE COINCIDENCIAS
        # Incluyendo el covering
        #------------------------------------
        self.poblacion.hacerConjuntoCoincidencias(estado_fenotipo, exploreIter)
        cons.timer.startTimeEvaluation()

        #--------------------------------------------------------------------------
        # HACER UNA PREDICCION
        # Utilizado aqui para seguir el progreso estimado de aprendizaje
        # Normalmente usado en la fase de exploracion de varios algoritmos de LCS
        #--------------------------------------------------------------------------
        prediccion = Prediccion(self.poblacion)
        prediccionFenotipo = prediccion.obtenerDecision()

        #-----------------------
        # PREDICCION NO POSIBLE
        #-----------------------
        if prediccionFenotipo == None or prediccionFenotipo == 'Tie':
            if cons.amb.datosFormateados.fenotipoDiscreto:
                prediccionFenotipo = random.choice(cons.amb.datosFormateados.listaFenotipos)

            else:
                prediccionFenotipo = random.randrange(cons.amb.datosFormateados.listaFenotipos[0], cons.amb.datosFormateados.listaFenotipos[1], (cons.amb.datosFormateados.listaFenotipos[1] - cons.amb.datosFormateados.listaFenotipos[0])/float(1000))

        else:
        #-------------------------------
        # PREDICCION FENOTIPO DISCRETO
        #-------------------------------
            if cons.amb.datosFormateados.fenotipoDiscreto:
                if prediccionFenotipo == estado_fenotipo[1]:
                    self.correcto[exploreIter % cons.frecuenciaSeguimiento] = 1

                else:
                    self.correcto[exploreIter % cons.frecuenciaSeguimiento] = 0
            else:
        #------------------------------
        # PREDICCION FENOTIPO CONTINUO
        #------------------------------
                prediccionError = math.fabs(prediccionFenotipo - float(estado_fenotipo[1]))
                rangoFenotipo = cons.amb.datosFormateados.listaFenotipos[1] - cons.amb.datosFormateados.listaFenotipos[0]
                estimadoPrecision = 1.0 - (prediccionError / float(rangoFenotipo))
                self.correcto[exploreIter % cons.frecuenciaSeguimiento] = estimadoPrecision

        cons.cronometro.detenerTiempoEvaluacion()

        #------------------------------
        # FORMAR CONJUNTO CORRECTO
        #------------------------------
        self.poblacion.hacerConjuntoCorrecto(estado_fenotipo[1])

        #------------------------
        # ACTUALIZAR PARAMETROS
        #------------------------
        self.poblacion.actualizarConjuntos(exploreIter)

        #--------------------------------------------------------------------------------------
        # SUBSUNCION
        # Aplicado a un conjunto correcto
        # Un heuristico para agregar presion de generalizacion adicional a Tangente Penitente
        #--------------------------------------------------------------------------------------
        if cons.hacerSubsuncion:
            cons.cronometro.iniciarTiempoSubsuncion()
            self.poblacion.hacerSubsuncionConjuntoCorrecto()
            cons.cronometro.detenerTiempoSubsuncion()

        #----------------------------------------------------------------------------------
        # SEGUIMIENTO DE ATRIBUTOS Y FEEDBACK
        # Un mecanismo de memoria a largo plazo que rastrea cada instancia en el conjunto
        # de datos y es usado para ayudar a guiar al algoritmo genetico
        #----------------------------------------------------------------------------------
        if cons.hacerSeguimientoAtributos:
            cons.cronometro.iniciarTiempoSA()
            cons.SA.updateAttTrack(self.poblacion)

            if cons.hacerFeedbackAtributos:
                cons.SA.updatePercent(exploreIter)
                cons.SA.genTrackProb()

            cons.cronometro.detenerTiempoSA()
        #----------------------------------------------------------------
        # EJECUTAR EL ALGORITMO GENETICO
        # Descubrir nuevas reglas hijas de un par seleccionado de padres
        #----------------------------------------------------------------
        self.poblacion.ejecutarAG(exploreIter, estado_fenotipo[0], estado_fenotipo[1]) # El AG es ejecutado dentro del conjunto correcto

        #---------------------------------------------------------------------------------------------------------------
        # SELECCIONAR REGLAS PARA ELIMINACION
        # Esto se hace cuando sea que haya mas reglas en la poblacion que "N", el maximo tamano posible de la poblacion
        #---------------------------------------------------------------------------------------------------------------
        self.poblacion.eliminacion(exploreIter)
        self.poblacion.limpiarConjuntos() # Limpia los conjuntos correctos y de coincidencias para la siguiente iteracion de aprendizaje


    def hacerEvaluacionPob(self, esEntrenamiento):
        """ Lleva a cabo una evaluacion completa de la poblacion de reglas actual. Solo a fenotipos discretos. La poblacion no cambia en esta evaluacion. Funciona en los datos de entrenamiento y de prueba """
        if esEntrenamiento:
            miTipo = "ENTRENANDO"

        else:
            miTipo = "PROBANDO"

        sinCoincidencia = 0 # Que tan a menudo la poblacion falla en tener un clasificador que que coincide en una instancia en los datos
        empate = 0 # Que tan a menudo puede el algoritmo no hacer una decision entre las clases debido a un empate
        cons.amb.resetearDataRef(esEntrenamiento)  # Ir a la primera instancia en el conjunto de datos
        listaFenotipos = cons.amb.datosFormateados.listaFenotipos

        # Inicializa entrada de directoria para cada clase
        diccPrecClase = {}
        for each in listaFenotipos:
            diccPrecClase[each] = PresicionClases()
        #----------------------------------------------
        if esEntrenamiento:
            instancias = cons.amb.datosFormateados.numInstanciasEntrenamiento

        else:
            instancias = cons.amb.datosFormateados.numInstanciasPrueba

        self.listaPrediccion = []
        self.conjuntoPrediccion = []
        self.listaReal = []

        #-------------------------------------------------------
        # OBTENER PREDICCION Y DETERMINAR ESTADO DE PREDICCION
        #-------------------------------------------------------
        for inst in range(instancias):
            if esEntrenamiento:
                estado_fenotipo = cons.amb.obtenerInstanciaEntrenamiento()

            else:
                estado_fenotipo = cons.amb.obtenerInstanciaPrueba()

            # ---------------------------------------------------
            self.population.makeEvalMatchSet(estado_fenotipo[0])
            prediccion = Prediccion(self.population)
            seleccionFenotipo = prediccion.obtenerDecision()

            if not esEntrenamiento:
                conjuntoFenotipo = prediccion.obtenerConjunto()

                self.listaPrediccion.append(seleccionFenotipo) # Usado para sacar predicciones de prueba crudas
                self.conjuntoPrediccion.append(conjuntoFenotipo)
                self.listaReal.append(estado_fenotipo[1])
            # ---------------------------------------------------
            if seleccionFenotipo == None:
                sinCoincidencia += 1

            elif seleccionFenotipo == 'Empate':
                empate += 1

            else: # Instancias en que fallaron en ser cubiertas son excluidas de los calculos iniciales de precision
                for each in listaFenotipos:
                    soyYo = False
                    fenotipoPreciso = False
                    fenotipoReal = estado_fenotipo[1]

                    if each == fenotipoReal:
                        soyYo = True # Es el fenotipo actual el fenotipo real?

                    if seleccionFenotipo == fenotipoReal:
                        fenotipoPreciso = True
                        
                    diccPrecClase[each].actualizarPrecision(soyYo, fenotipoPreciso)

            cons.amb.nuevaInstancia(esEntrenamiento) # Siguiente instancia

            self.poblacion.limpiarConjuntos()

        #-----------------------------------------------------------------------------
        # CALCULAR PRECISION
        # Situacion improbable en que no se encuentran reglas de coincidencia
        # En los datos de entrenamiento o de prueba (esto puede suceder en los datos 
        # de prueba cuando se produce una fuerte sobrecarga de entrenamiento)
        #-----------------------------------------------------------------------------
        if sinCoincidencia == instancias:
            probAleatoria = float (1.0 / len(cons.amb.datosFormateados.listaFenotipos))
            print("-------------------------------------------")
            print(str(miTipo)+" Resultados de precision: ")
            print("Cubrimiento de instancias = " + str(0) + '%')
            print("Empates de prediccion = " + str(0) + '%')
            print(str(0) + ' de ' + str(instancias) + ' instancias cubiertas y correctamente clasificadas')
            print("Precision estandar (ajustada) = " + str(probAleatoria))
            print("Precision balanceada (ajustada) = " + str(probAleatoria))

            # Las precisiones estandar y balanceadas solo seran iguales cuando hay
            # la misma cantidad de instancias representativas de cada fenotipo Y hay un
            # covering del 100%. (NOTA: incluso con un covering del 100%, los valores
            # pueden diferir debido a pequenas diferencias de calculo)

            listaResultados = [probAleatoria, 0]
            return listaResultados

        #--------------------
        # CALCULAR PRECISION 
        #--------------------
        else:
            # Calcular precision estandar
            precisionEstandar = 0

            for each in listaFenotipos:
                instanciasCorrectamenteClasificadas = diccPrecClase[each].T_myClass + diccPrecClase[each].T_otherClass
                instanciasIncorrectamenteClasificadas = diccPrecClase[each].F_myClass + diccPrecClase[each].F_otherClass

                precisionClases = float(instanciasCorrectamenteClasificadas) / float(instanciasCorrectamenteClasificadas + instanciasIncorrectamenteClasificadas)
                precisionEstandar += precisionClases

            precisionEstandar = precisionEstandar / float(len(listaFenotipos))

            # Calcular precision balanceada
            precisionBalanceada = 0
            for each in listaFenotipos:
                try:
                    sensibilidad = diccPrecClase[each].T_myClass / (float(diccPrecClase[each].T_myClass + diccPrecClase[each].F_otherClass))

                except:
                    sensibilidad = 0.0

                try:
                    especifidad = diccPrecClase[each].T_otherClass / (float(diccPrecClase[each].T_otherClass + diccPrecClase[each].F_myClass))

                except:
                    especifidad = 0.0

                precisionClasesBalanceada = (sensibilidad + especifidad) / 2.0
                precisionBalanceada += precisionClasesBalanceada

            precisionBalanceada = precisionBalanceada / float(len(listaFenotipos))

            # Ajuste para instancias no cubiertas
            # Para evitar sesgos positivos o negativos se incorpora la probabilidad de adivinar un fenotipo (ej. 50% si son dos fenotipos)
            falloPrediccion = float(sinCoincidencia)/float(instancias)
            empatePrediccion = float(empate)/float(instancias)
            cubrimientoInstancia = 1.0 - falloPrediccion
            prediccionHecha = 1.0 - (falloPrediccion + empatePrediccion)

            precisionEstandarAjustada = (precisionEstandar * prediccionHecha) + ((1.0 - prediccionHecha) * (1.0 / float(len(listaFenotipos))))
            precisionBalanceadaAjustada = (precisionBalanceada * prediccionHecha) + ((1.0 - prediccionHecha) * (1.0 / float(len(listaFenotipos))))

            # La precision balanceada ajustada es calculada de tal manera que
            # las instancias que no coincidieron tienen una probabilidad
            # de ser correctamente classificadas en la precision reportada
            print("-------------------------------------------")
            print(str(miTipo)+" Resultados de precision: ")
            print("Cubrimiento de instancias = "+ str(cubrimientoInstancia * 100.0) + '%')
            print("Empates de prediccion = "+ str(empatePrediccion * 100.0) + '%')
            print(str(instanciasCorrectamenteClasificadas) + ' de ' + str(instancias) + ' instancias cubiertas y correctamente clasificadas.')
            print("Precision estandar (ajustada) = " + str(precisionEstandarAjustada))
            print("Precision balanceada (ajustada) = " + str(precisionBalanceadaAjustada))

            # Las precisiones estandar y balanceadas solo seran iguales cuando hay
            # la misma cantidad de instancias representativas de cada fenotipo Y hay un
            # covering del 100%. (NOTA: incluso con un covering del 100%, los valores
            # pueden diferir debido a pequenas diferencias de calculo)
            listaResultados = [precisionBalanceadaAjustada, cubrimientoInstancia]
            return listaResultados


    def reinicioPoblacion(self):
        """ Maneja el cargado y la evolucion/aprendizaje continuado de una poblacion de clasificadores previamente guardada """
        cons.cronometro.fijarTiempoReinicio(cons.rutaReinicioPob) # Reconstruir objetos de tiempo

        # Extraer la ultima iteracion
        temp = cons.rutaReinicioPob.split('_')
        iterRef = len(temp)-1
        iteracionesCompletadas = int(temp[iterRef])
        print("Reiniciando poblacion despues de " +str(iteracionesCompletadas)+ " iteraciones.")

        self.exploreIter = iteracionesCompletadas - 1

        for i in range(len(cons.puntoscontrolAprendizaje)):
            cons.learningCheckpoints[i] += iteracionesCompletadas

        cons.maxiteracionesAprendizaje += iteracionesCompletadas

        # Reconstruir poblacion existente del archivo de texto
        self.poblacion = ConjuntoClasificadores(cons.rutaReinicioPob)

        try:
            f = open(cons.popRebootPath+"_EstadisticasPob.txt", 'rU')
            correctRef = 39 # Referencia para rastrear estimado de precision de aprendizaje guardado en EstadisticasPob 
            
            lineaTemp = None

            for i in range(correctRef):
                lineaTemp = f.readline()

            listaTemp = lineaTemp.strip().split('\t')

            self.correcto = listaTemp

            if cons.amb.datosFormateados.fenotipoDiscreto:
                for i in range(len(self.correcto)):
                    self.correcto[i] = int(self.correcto[i])

            else:
                for i in range(len(self.correcto)):
                    self.correcto[i] = float(self.correcto[i])

            f.close()

        except IOError as excepcion:
            (errno, strerror) = excepcion.args
            print(("Error de I/O (%s): %s" % (errno, strerror)))
            raise


    def correrSoloCR(self):
        """ Ejecutar compactacion de reglas en una poblacion de reglas existente """

        print("Iniciando compactacion de reglas...")
        #---------------------------------------------------------------------------------------------------
        # CHEQUEAR PARA REINICIO DE POBLACION
        # Requerida para ejecutar solo compactacion de reglas en una poblacion de reglas guardada existente
        #---------------------------------------------------------------------------------------------------
        if not cons.hacerReinicioPoblacion:
            print("Algoritmo - Error: - Poblacion de reglas existente se requiere para ejecutar solo la compactacion de reglas")
            return

        try:
            fileObject = open(cons.rutaReinicioPob + "_EstadisticasPob.txt", 'rU')

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('No se puede abrir', cons.rutaReinicioPob + "_EstadisticasPob.txt")
            raise

        # Recupera las últimas precisiones de entrenamiento y prueba del archivo guardado
        lineaTemp = None

        for i in range(3):
            lineaTemp = fileObject.readline()

        listaTemp = lineaTemp.strip().split('\t')
        precEntrena = float(listaTemp[0])

        if cons.archivoPrueba != 'None': # Si hay disponible un archivo de prueba
            precPrueba = float(listaTemp[1])

        else:
            precPrueba = None

        #-------------------------
        # COMPACTACION DE REGLAS
        #-------------------------
        cons.cronometro.iniciarTiempoCompReg()
        CompactacionReglas(self.poblacion, precEntrena, precPrueba)
        cons.cronometro.detenerTiempoCompReg()

        #-----------------------------------------------------
        # EVALUACION GLOBAL DE POBLACION DE REGLAS COMPACTADA
        #-----------------------------------------------------
        cons.cronometro.iniciarTiempoEvaluacion()
        self.poblacion.recalcularSumaNumerosidad()
        self.poblacion.ejecutarEvalPobProm(self.exploreIter)
        self.poblacion.ejecutarSumaGeneralidadAtributos()

        
        cons.amb.iniciarModoEvaluacion()

        if cons.archivoPrueba != 'None': # Si hay un archivo de prueba disponible
            if cons.amb.datosFormateados.fenotipoDiscreto:
                evalEntrena = self.hacerEvaluacionPob(True)
                evalPrueba = self.hacerEvaluacionPob(False)

            else:
                print("Algoritmo - Error: Tangente Penitente no puede manipular endpoints continuos.")

        elif cons.archivoEntrenamiento != 'None':
            if cons.amb.datosFormateados.fenotipoDiscreto:
                evalEntrena = self.hacerEvaluacionPob(True)
                evalPrueba = None

            else:
                print("Algoritmo - Error: Tangente Penitente no puede manipular endpoints continuos")

        else: # Ambiente online
            evalEntrena = None
            evalPrueba = None

        cons.amb.detenerModoEvaluacion()
        cons.cronometro.detenerTiempoEvaluacion()
        
        cons.cronometro.devolverCronometroGlobal()
        
        # -----------------------------
        # ESCRIBIR ARCHIVOS DE SALIDA
        #------------------------------
        AdminSalida().escribirEstadisticasPob(cons.archivoSalida + "_CR_" + cons.metodoCompactacionReglas, evalEntrena, evalPrueba, self.exploreIter + 1, self.population, self.correcto)
        AdminSalida().escribirPob(cons.archivoSalida + "_CR_" + cons.metodoCompactacionReglas, self.exploreIter + 1, self.population)
        AdminSalida().occurenciaAttCo(cons.archivoSalida + "_CR_" + cons.metodoCompactacionReglas, self.exploreIter + 1, self.population)
        AdminSalida().escribirPredicciones(self.exploreIter, cons.archivoSalida + "_CR_" + cons.metodoCompactacionReglas, self.listaPrediccion, self.listaReal, self.conjuntoPrediccion)

        print("Compactacion de reglas completada")


    def correrSoloPrueba(self):
        """ Ejecuta evaluacion del conjunto de prueba en una poblacion de reglas existene """

        print("Inicializando evaluacion de conjunto de datos de prueba")
        #---------------------------------------------------------------------------------------------
        # CHEQUEAR REINICIO DE POBLACION
        # Requerido para ejecutar solamente evaluacion de prueba en una poblacion de reglas existente
        #---------------------------------------------------------------------------------------------
        if not cons.hacerReinicioPoblacion:
            print("Algoritmo - Error: Se requiere poblacion de reglas para ejecutar compactacion de reglas solamente")
            return

        cons.amb.iniciarModoEvaluacion()

        if cons.archivoPrueba != 'None': # Si hay un archivo de prueba disponible
            if cons.amb.datosFormateados.fenotipoDiscreto:
                evalPrueba = self.hacerEvaluacionPob(False)

            else:
                print("Algoritmo - Error: Tangente Penitente no puede manipular endpoints continuos")

        else: # Ambiente online
            evalPrueba = None

        cons.amb.detenerModoEvaluacion()
        cons.cronometro.detenerTiempoEvaluacion()

        cons.cronometro.devolverCronometroGlobal()
        
        AdminSalida().editarEstadsPob(evalPrueba)
        AdminSalida().escribirPredicciones(self.exploreIter, cons.archivoSalida, self.listaPrediccion, self.listaReal, self.conjuntoPrediccion)
