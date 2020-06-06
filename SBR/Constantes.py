# TANGENTE PENITENTE
# Constantes.py

"""
Almacena y pone a disposición todos los parámetros de ejecución 
algorítmicos, y actúa como una puerta de enlace para referenciar 
el cronometro, el entorno, las propiedades del conjunto de datos, 
el seguimiento de los atributos y las puntuaciones/pesos del 
conocimiento experto. Aquí es también donde se controla la 
generación del conocimiento experto y sus respectivos pesos.
"""

class Constantes:
    def fijarConstantes(self, par):
        """ Toma los parámetros analizados como un diccionario 
        en ConfigParseador y hace que estos parámetros estén 
        disponibles en todo Tangente Penitente. Se proporcionan 
        valores por defecto para algunos parámetros mediante el 
        uso de comandos try/except para que los usuarios puedan 
        generar archivos de configuración más sencillos """

        # archivoEntrenamiento
        try:
            # Revisa la extension .txt
            revisarExt = par['archivoEntrenamiento'][len(par['archivoEntrenamiento']) - 4: len(par['archivoEntrenamiento'])]

            if revisarExt == '.txt':
                self.archivoEntrenamiento = par['archivoEntrenamiento'][0:len(par['archivoEntrenamiento']) - 4]

            else:
                self.archivoEntrenamiento = par['archivoEntrenamiento']

        except:
            print('Constantes - Error: No hay valor para "archivoEntrenamiento". Por favor defina uno en el archivo de configuracion.')

        # archivoPrueba
        try:
            # Revisar la extension .txt
            revisarExt = par['archivoPrueba'][len(par['archivoPrueba']) - 4: len(par['archivoPrueba'])]

            if revisarExt == '.txt':
                self.archivoPrueba = par['archivoPrueba'][0:len(par['archivoPrueba']) - 4]

            else:
                self.archivoPrueba = par['archivoPrueba']
        
        except:
           self.archivoPrueba = 'None'

        nombreEntrenamiento = self.archivoEntrenamiento.split('/')
        # Sacar solo el nombre del archivo
        nombreEntrenamiento = nombreEntrenamiento[len(nombreEntrenamiento - 1)]

        # nombreArchivoSalida
        try:
            if str(par['nombreArchivoSalida']) == 'None' or str(par['nombreArchivoSalida'] == 'none'):
                self.nombreArchivoSalidaOriginal = nombreEntrenamiento
                self.nombreArchivoSalida = nombreEntrenamiento + '_TP'

            else:
                self.nombreArchivoSalidaOriginal = str(par['nombreArchivoSalida']) + nombreEntrenamiento
                self.nombreArchivoSalida = str(par['nombreArchivoSalida']) + nombreEntrenamiento + '_TP'

        except:
            self.nombreArchivoSalidaOriginal = nombreEntrenamiento
            self.nombreArchivoSalida = nombreEntrenamiento + '_TP'

        # datosOffline
        try:
            self.datosOffline = bool(int(par['datosOffline']))
        
        except:
            self.datosOffline = True

        # validacionCruzadaInterna
        try:
            self.validacionCruzadaInterna = int(par['validacionCruzadaInterna'])

        except:
            self.validacionCruzadaInterna = 0

        # semillaAleatoria
        try:
            if par['semillaAleatoria'] == 'False' or par['semillaAleatoria'] == 'false':
                self.usarSemilla = False

            else:
                self.usarSemilla = True
                self.semillaAleatoria = int(par['semillaAleatoria'])

        except:
            self.usarSemilla = False

        # -------------------------------------------------------
        # etiquetaIDInstancia
        try:
            self.etiquetaIDInstancia = par['etiquetaIDInstancia']
            
        except:
            self.etiquetaIDInstancia = 'IDInstancia'

        # etiquetaFenotipo
        try:
            self.etiquetaFenotipo = par['etiquetaFenotipo']

        except:
            self.etiquetaFenotipo = 'Clase'

        # limiteAtributoDiscreto
        try:
            self.limiteAtributoDiscreto = int(par['limiteAtributoDiscreto'])

        except:
            self.limiteAtributoDiscreto = 10

        # etiquetaDatosFaltantes
        try:
            self.etiquetaDatosFaltantes = par['etiquetaDatosFaltantes']

        except:
            self.etiquetaDatosFaltantes = 'NA'

        # salidaResumen
        try:
            self.salidaResumen = bool(int(par['salidaResumen']))

        except:
            self.salidaResumen = True

        # salidaPoblacion
        try:
            self.salidaPoblacion = bool(int(par['salidaPoblacion']))

        except:
            self.salidaPoblacion = True

        # salidaAttCoOccur
        try:
            self.salidaAttCoOccur = bool(int(par['salidaAttCoOccur']))

        except:
            self.salidaAttCoOccur = True

        # salidaPrediccionesPrueba
        try:
            self.salidaPrediccionesPrueba = bool(int(par['salidaPrediccionesPrueba']))

        except:
            self.salidaPrediccionesPrueba = True

        # soloPrueba
        try:
            self.soloPrueba = bool(int(par['soloPrueba']))
            
        except:
            self.soloPrueba = False

        # -------------------------------------------------------
        # frecuenciaSeguimiento
        try:
            self.frecuenciaSeguimiento = int(par['frecuenciaSeguimiento'])

        except:
            self.frecuenciaSeguimiento = 0

        # iteracionesAprendizaje
        try:
            self.iteracionesAprendizaje - par['iteracionesAprendizaje']

        except:
            self.iteracionesAprendizaje = '5000.10000.20000.100000'

        # N
        try:
            self.N = int(par['N'])

        except:
            self.N = 1000

        # nu
        try:
            self.nu = int(par['nu'])

        except:
            self.nu = 1

        # chi
        try:
            self.chi = float(par['chi'])

        except:
            self.chi = 0.8

        # upsilon
        try:
            self.upsilon = float(par['upsilon'])

        except:
            self.upsilon = 0.04
        
        # theta_GA
        try:
            self.theta_GA = int(par['theta_GA'])

        except:
            self.theta_GA = 25

        # theta_del
        try:
            self.theta_del = int(par['theta_del'])

        except:
            self.theta_del = 20

        # theta_sub
        try:
            self.theta_sub = int(par['theta_sub'])
        
        except:
            self.theta_sub = 20

        # acc_sub
        try:
            self.acc_sub = float(par['acc_sub'])
        
        except:
            self.acc_sub = 0.99

        # beta
        try:
            self.beta = float(par['beta'])
        
        except:
            self.beta = 0.2

        # delta
        try:
            self.delta = float(par['delta'])
        
        except:
            self.delta = 0.1

        # aptitudInicial
        try:
            self.aptitudInicial = float(par['aptitudInicial'])
        
        except:
            self.aptitudInicial = 0.01

        # reduccionAptitud
        try:
            self.reduccionAptitud = float(par['reduccionAptitud'])

        except:
            self.reduccionAptitud = 0.1

        # theta_sel
        try:
            self.theta_sel = float(par['theta_sel'])

        except:
            self.theta_sel = 0.5

        # RSL_Override
        try:
            self.RSL_Override = int(par['RSL_Override'])

        except:
            self.RSL_Override = 0

        # hacerSubsuncion
        try:
            self.hacerSubsuncion = bool(int(par['hacerSubsuncion']))

        except:
            self.hacerSubsuncion = True

        # metodoSeleccion
        try:
            self.metodoSeleccion = par['metodoSeleccion']

        except:
            self.metodoSeleccion = 'torneo'

        # hacerSeguimientoAtributos
        try:
            self.hacerSeguimientoAtributos = bool(int(par['hacerSeguimientoAtributos']))

        except:
            self.hacerSeguimientoAtributos = True

        # hacerFeedbackAtributos
        try:
            self.hacerFeedbackAtributos = bool(int(par['hacerFeedbackAtributos']))

        except:
            self.hacerFeedbackAtributos = True

        # -------------------------------------------------------
        # Parametros del Conocimiento Experto

        # usarConocimientoExperto
        try:
            self.usarConocimientoExperto = bool(int(par['usarConocimientoExperto']))

        except:
            self.usarConocimientoExperto = True

        # u
        if self.usarConocimientoExperto:
            try:
                if str(par['generacionExternaCE']) == 'None' or str(par['generacionExternaCE']) =='none':
                    self.generacionInternaCE = True

                    try:
                        if par['nombrearchivoSalidaCE'] == 'None' or par['nombrearchivoSalidaCE'] =='none':
                            self.nombrearchivoSalidaCE = nombreEntrenamiento
                            self.nombreArchivoSalidaOriginal = nombreEntrenamiento

                        else:
                            self.nombrearchivoSalidaCE = par['nombrearchivoSalidaCE'] + nombreEntrenamiento
                            self.nombreArchivoSalidaOriginal = par['nombrearchivoSalidaCE'] + nombreEntrenamiento

                    except:
                        self.nombrearchivoSalidaCE = nombreEntrenamiento
                        self.nombreArchivoSalidaOriginal = nombreEntrenamiento

                else:
                    self.generacionInternaCE = False

                    try:
                        self.fuenteCE = str(par['generacionExternaCE'])

                    except:
                        print('Constantes - Error: No hay archivo de Conocimiento Experto')

            # Valor predeterminado - cuando generacionExternaCE
            # no se especifica
            except:
                self.generacionInternaCE = True

                try:
                    if par['nombrearchivoSalidaCE'] == 'None' or par['nombrearchivoSalidaCE'] == 'none':
                        self.nombrearchivoSalidaCE = nombreEntrenamiento
                        self.nombreArchivoSalidaOriginal = nombreEntrenamiento

                    else:
                        self.nombrearchivoSalidaCE = par['generacionExternaCE'] + nombreEntrenamiento
                        self.nombreArchivoSalidaOriginal = par['nombrearchivoSalidaCE'] + nombreEntrenamiento

                except:
                    self.nombrearchivoSalidaCE = nombreEntrenamiento
                    self.nombreArchivoSalidaOriginal = nombreEntrenamiento

        # algoritmoFiltro
        try:
            self.algoritmoFiltro = par['algoritmoFiltro']

        except:
            self.algoritmoFiltro = 'multisurf'

        # porcentajeTurf
        try:
            self.porcentajeTurf = float(par['porcentajeTurf'])

        except:
            self.porcentajeTurf = 0.05

        # vecinosRelief
        if self.algoritmoFiltro == 'relieff':
            try:
                self.vecinosRelief = int(par['vecinosRelief'])

            except:
                self.vecinosRelief = 10

        # fraccionMuestreoRelief
        if self.algoritmoFiltro != 'multisurf':
            try:
                self.fraccionMuestreoRelief = float(par['fraccionMuestreoRelief'])

            except:
                self.fraccionMuestreoRelief = 1.0

        # soloPuntajesCE
        try:
            self.soloPuntajesCE = bool(int['soloPuntajesCE'])

        except:
            self.soloPuntajesCE = False

        # -------------------------------------------------------
        # Parametros de compactacion de reglas

        # hacerCompactacionReglas
        try:
            self.hacerCompactacionReglas = bool(int(par['hacerCompactacionReglas']))

        except:
            self.hacerCompactacionReglas = True

        # soloCR
        try:
            self.soloCR = bool(int(par['soloCR']))

        except:
            self.soloCR = False

        # metodoCompactacionReglas
        try:
            self.metodoCompactacionReglas = par['metodoCompactacionReglas']

        except:
            self.metodoCompactacionReglas = 'QRF'

        # -------------------------------------------------------
        # Parametros de reinicio de parametros

        # hacerReinicioPoblacion
        try:
            self.hacerReinicioPoblacion = bool(int(par['hacerReinicioPoblacion']))

        except:
            self.hacerReinicioPoblacion = False

        # rutaReinicioPob
        if self.hacerReinicioPoblacion:
            try:
                self.rutaReinicioPob = self.nombreArchivoSalida + '_' + par['iteracionReinicioPob']

            except:
                print('Constanes - Error: no hay valor para rutaReinicioPob, por favor especifique uno en el archivo de configuracion.')

        self.primeraEpocaCompleta = False

        # LLAMADAS
        self.llamadasEpoca = []
        self.llamadasIteracion = []
        self.llamadasPuntoControl = []

        # OBJETOS DE CONTROL
        self.parar = False
        self.forzarPuntoControl = False

        if self.validacionCruzadaInterna == 0 or self.validacionCruzadaInterna == 1:
            pass

        else:
            self.archivoEntrenamientoOriginal = copy.deepcopy(self.archivoEntrenamiento)
            self.archivoPruebaOriginal = copy.deepcopy(self.archivoPrueba)

    def referenciarCronometro(self, cronometro):
        """ Guarda la referencia al objeto del cronometro """
        self.cronometro = cronometro

    def referenciarAmb(self, amb):
        """ Guarda la referencia al objeto del ambiente """
        self.amb = amb

    def referenciarSeguimientoAtributos(self, SA):
        """ Guarda la referencia al objeto del seguimiento de atributos """
        self.SA = SA

    def referenciarConocimientoExperto(self, CE):
        """ Guarda la referencia al objeto del conocimiento experto """
        self.CE = CE

    def parsearIteraciones(self):
        """ Formatea otros parametros de ejecucion importantes 
        (tales como: iteraciones maximas, puntos de control de evaluacion
        y frecuencia de seguimiento de evaluacion"""

        # Parse el string que especifica los puntos de control de
        # evaluacion y el numero maximo de iteraciones de 
        # aprendizaje
        puntosControl = self.iteracionesAprendizaje.split('.')

        for i in range(len(puntosControl)):
            # Convierte las iteraciones del punto de control de string a ints
            puntosControl[i] = int(puntosControl[i])

        self.puntosControlAprendizaje = puntosControl

        self.iteracionesAprendizajeMax = self.puntosControlAprendizaje[(self.puntosControlAprendizaje) - 1]

        # Ajustar la frecuencia de seguimiento para que concuerde
        # con el tamano de los datos de entrenamiento - aprendizaje
        # ocurre en cada epoca
        if self.frecuenciaSeguimiento == 0:
            self.frecuenciaSeguimiento = self.amb.datosFormateados.numInstanciasEntrenamiento

    def actualizarNombreArchivos(self, part):
        pass

    def sobrescribirParametros(self):
        pass

cons = Constantes()