"""
TANGENTE PENITENTE
Nombre: tp_Constantes.py
Descripcion: Almacena y pone a disposición todos los parámetros de 
             ejecución alogrítmicos, y actúa como una puerta de enlace 
             para referenciar el cronometro, el entorno, las propiedades 
             del conjunto de datos, el seguimiento de los atributos y las 
             puntuaciones/pesos del conocimiento experto. Aquí es también 
             donde se controla la generación del conocimiento experto y 
             sus respectivos pesos.
"""

# Importar modulos requeridos
import copy
import os
import time
#

class Constantes:
    def fijarConstantes(self,par):
        """ Toma los parámetros analizados como un diccionario en tp_ConfigParseador
            y hace que estos parámetros estén disponibles en todo Tangente Penitente. 
            Se proporcionan valores por defecto para algunos parámetros mediante el 
            uso de comandos try/except para que los usuarios puedan generar archivos 
            de configuración más sencillos que sólo. """

        try:
            chequeoExt = par['archivoEntrenamiento'][len(par['archivoEntrenamiento'])-4:len(par['archivoEntrenamiento'])] #Check for included .txt file extension
            if chequeoExt == '.txt':
                self.archivoEntrenamiento = par['archivoEntrenamiento'][0:len(par['archivoEntrenamiento'])-4]
            else:
                self.archivoEntrenamiento = par['archivoEntrenamiento']                                           #Saved as text
        except:
            print('Constants: Error - Default value not available for "archivoEntrenamiento", please specify value in the configuration file.')
        try:
            chequeoExt = par['archivoPrueba'][len(par['archivoPrueba'])-4:len(par['archivoPrueba'])]  #Check for included .txt file extension
            if chequeoExt == '.txt':
                self.archivoPrueba = par['archivoPrueba'][0:len(par['archivoPrueba'])-4]
            else:
                self.archivoPrueba = par['archivoPrueba']                                             #Saved as text
        except:
            self.archivoPrueba = 'None'
        nombreEntrenamiento = self.archivoEntrenamiento.split('/')
        nombreEntrenamiento = nombreEntrenamiento[len(nombreEntrenamiento)-1] #Grab FileName only.
        try:
            if str(par['archivoSalida']) == 'None' or str(par['archivoSalida']) == 'none':
                self.nombreOriginalArchivoSalida = nombreEntrenamiento                               #Saved as text
                self.archivoSalida = nombreEntrenamiento +'_TangPenit'                          #Saved as text
            else:
                self.nombreOriginalArchivoSalida = str(par['archivoSalida'])+nombreEntrenamiento           #Saved as text
                self.archivoSalida = str(par['archivoSalida'])+nombreEntrenamiento+'_TangPenit'                      #Saved as text
        except:
            self.nombreOriginalArchivoSalida = nombreEntrenamiento                               #Saved as text
            self.archivoSalida = nombreEntrenamiento +'_TangPenit'                          #Saved as text
        try:
            self.datosOffline = bool(int(par['datosOffline']))                        #Saved as Boolean
        except: #Default
            self.datosOffline = True
        try:
            self.validacionCruzadaInterna = int(par['validacionCruzadaInterna'])      #Saved as int
        except: #Default
            self.validacionCruzadaInterna = 0
            
        try:
            if par['semillaAleatoria'] == 'False' or par['semillaAleatoria'] == 'false':
                self.usarSemilla = False
            else:
                self.usarSemilla = True
                self.semillaAleatoria = int(par['semillaAleatoria'])                            #Saved as int
        except: #Default
            self.usarSemilla = False
              
        #----------------------------------------------------------------------------------
        try:
            self.etiquetaIDInstancia = par['etiquetaIDInstancia']                           #Saved as text
        except: #Default
            self.etiquetaIDInstancia = 'IDInstancia'
        try:
            self.etiquetaFenotipo = par['etiquetaFenotipo']                             #Saved as text
        except: #Default
            self.etiquetaFenotipo = 'Clase'
        try:
            self.limiteAtributoDiscreto = int(par['limiteAtributoDiscreto'])        #Saved as int
        except: #Default
            self.limiteAtributoDiscreto = 10
        try:
            self.etiquetaDatosFaltantes = par['etiquetaDatosFaltantes']                         #Saved as text
        except: #Default
            self.etiquetaDatosFaltantes = 'NA'
        try:
            self.salidaResumen = bool(int(par['salidaResumen']))                    #Saved as Boolean
        except: #Default
            self.salidaResumen = True
        try:
            self.salidaPoblacion = bool(int(par['salidaPoblacion']))              #Saved as Boolean
        except: #Default
            self.salidaPoblacion = True
        try:
            self.salidaAttCoOccur = bool(int(par['salidaAttCoOccur']))              #Saved as Boolean  
        except: #Default
            self.salidaAttCoOccur = True     
        try:
            self.salidaPrediccionesPrueba = bool(int(par['salidaPrediccionesPrueba']))              #Saved as Boolean  
        except: #Default
            self.salidaPrediccionesPrueba = True  
        try:
            self.soloPrueba = bool(int(par['soloPrueba']))              #Saved as Boolean  
        except: #Default
            self.soloPrueba = False

        #----------------------------------------------------------------------------------
        try:
            self.frecuenciaSeguimiento = int(par['frecuenciaSeguimiento'])      #Saved as int
        except: #Default
            self.frecuenciaSeguimiento = 0
        try:
            self.iteracionesAprendizaje = par['iteracionesAprendizaje']         #Saved as text
        except: #Default
            self.iteracionesAprendizaje ='5000.10000.20000.100000'
        try:
            self.N = int(par['N'])                                      #Saved as int
        except: #Default
            self.N = 1000
        try:
            self.nu = int(par['nu'])                                    #Saved as int
        except: #Default
            self.nu = 1
        try:
            self.chi = float(par['chi'])                                #Saved as float
        except: #Default
            self.chi = 0.8
        try:
            self.epsilon = float(par['epsilon'])                        #Saved as float
        except: #Default
            self.epsilon = 0.04
        try:
            self.theta_GA = int(par['theta_GA'])                        #Saved as int
        except: #Default
            self.theta_GA = 25
        try:
            self.theta_del = int(par['theta_del'])                      #Saved as int
        except: #Default
            self.theta_del = 20
        try:
            self.theta_sub = int(par['theta_sub'])                      #Saved as int
        except: #Default
            self.theta_sub = 20
        try:
            self.acc_sub = float(par['acc_sub'])                        #Saved as float
        except: #Default
            self.acc_sub = 0.99
        try:
            self.beta = float(par['beta'])                              #Saved as float
        except: #Default
            self.beta = 0.2
        try:
            self.delta = float(par['delta'])                            #Saved as float
        except: #Default
            self.delta = 0.1
        try:
            self.init_apt = float(par['init_apt'])                      #Saved as float
        except: #Default
            self.init_apt = 0.01
        try:
            self.reduccionAptitud = float(par['reduccionAptitud'])      #Saved as float
        except: #Default
            self.reduccionAptitud = 0.1
        try:
            self.theta_sel = float(par['theta_sel'])                    #Saved as float
        except: #Default
            self.theta_sel = 0.5
        try:
            self.RSL_Override = int(par['RSL_Override'])                    #Saved as float
        except: #Default
            self.RSL_Override = 0
        
        try:
            self.hacerSubsuncion = bool(int(par['hacerSubsuncion']))                #Saved as Boolean
        except: #Default
            self.hacerSubsuncion = True
        try:
            self.metodoSeleccion = par['metodoSeleccion']                       #Saved as text
        except: #Default
            self.metodoSeleccion = 'torneo'
        
        try:
            self.hacerSeguimientoAtributos = bool(int(par['hacerSeguimientoAtributos']))    #Saved as Boolean
        except: #Default
            self.hacerSeguimientoAtributos = True
        try:
            self.hacerFeedbackAtributos = bool(int(par['hacerFeedbackAtributos']))    #Saved as Boolean
        except: #Default
            self.hacerFeedbackAtributos = True
            
        #Expert Knowledge Parameters -----------------------------------------------------------------------
        try:
            self.usarConocimientoExperto = bool(int(par['usarConocimientoExperto']))          #Saved as Boolean
        except: #Default
            self.usarConocimientoExperto = True
            
        if self.usarConocimientoExperto:
            try:
                if str(par['generacionExternaCE']) == 'None' or str(par['generacionExternaCE']) == 'none':
                    self.generacionInternaCE = True
                    try:
                        if par['nombrearchivoSalidaCE'] == 'None' or par['nombrearchivoSalidaCE'] == 'none':
                            self.nombrearchivoSalidaCE = nombreEntrenamiento 
                            self.originalnombrearchivoSalidaCE = nombreEntrenamiento
                        else:
                            self.nombrearchivoSalidaCE = par['nombrearchivoSalidaCE']+nombreEntrenamiento          #Saved as text
                            self.originalnombrearchivoSalidaCE = par['nombrearchivoSalidaCE']+nombreEntrenamiento
                    except:
                        self.nombrearchivoSalidaCE = nombreEntrenamiento 
                        self.originalnombrearchivoSalidaCE = nombreEntrenamiento
                    
                else:
                    self.generacionInternaCE = False
                    try:
                        self.fuenteCE = str(par['generacionExternaCE'])  #Saved as text
                    except:
                        print('Constants: Error - No default available for external EK file.')
     
            except: #Default - generacionExternaCE is not specified.
                self.generacionInternaCE = True
                try:
                    if par['nombrearchivoSalidaCE'] == 'None' or par['nombrearchivoSalidaCE'] == 'none':
                        self.nombrearchivoSalidaCE = nombreEntrenamiento 
                        self.originalnombrearchivoSalidaCE = nombreEntrenamiento
                    else:
                        self.nombrearchivoSalidaCE = par['nombrearchivoSalidaCE']+nombreEntrenamiento          #Saved as text
                        self.originalnombrearchivoSalidaCE = par['nombrearchivoSalidaCE']+nombreEntrenamiento
                except:
                    self.nombrearchivoSalidaCE = nombreEntrenamiento 
                    self.originalnombrearchivoSalidaCE = nombreEntrenamiento
                    
        try:
            self.algoritmoFiltro = par['algoritmoFiltro']                       #Saved as text
        except: #Default
            self.algoritmoFiltro = 'multisurf'
        try:
            self.porcentajeTurf = float(par['porcentajeTurf'])                       #Saved as Boolean
        except: #Default
            self.porcentajeTurf = 0.05                              

        if self.algoritmoFiltro == 'relieff':
            try:
                self.vecinosRelief = int(par['vecinosRelief'])                  #Saved as int
            except: #Default
                self.vecinosRelief = 10
        if self.algoritmoFiltro != 'multisurf': 
            try:
                self.fraccionMuestreoRelief = float(par['fraccionMuestreoRelief'])      #Saved as float
            except: #Default
                self.fraccionMuestreoRelief = 1.0 
        try:
            self.soloPuntajesCE = bool(int(par['soloPuntajesCE']))                  #Saved as Boolean
        except: #Default
            self.soloPuntajesCE = False
            
        #Rule Compaction Parameters--------------------------------------------------------------------------------
        try:
            self.hacerCompactacionReglas = bool(int(par['hacerCompactacionReglas']))          #Saved as Boolean
        except: #Default
            self.hacerCompactacionReglas = True
        try:
            self.soloCR = bool(int(par['soloCR']))                              #Saved as Boolean
        except: #Default
            self.soloCR = False
        try:
            self.metodoCompactacionReglas = par['metodoCompactacionReglas']             #Saved as text
        except: #Default
            self.metodoCompactacionReglas = 'QRF'
        #Population Reboot Parameters------------------------------------------------------------------
        try:
            self.hacerReinicioPoblacion = bool(int(par['hacerReinicioPoblacion']))      #Saved as Boolean
        except: #Default
            self.hacerReinicioPoblacion = False
        if self.hacerReinicioPoblacion:
            try:
                self.rutaReinicioPob = self.archivoSalida+'_'+par['iteracionReinicioPob']                           #Saved as text
            except:
                print('Constants: Error - Default value not available for "rutaReinicioPob", please specify value in the configuration file.')
    
        self.primeraEpocaCompleta = False
        
        #CALLBACKS - GUI
        self.llamadasEpoca = []
        self.llamadasIteracion = []
        self.llamadasPuntosControl = []
        
        #CONTROL OBJECTS - GUI
        self.parar = False
        self.forzarPuntoControl = False
        
        if self.validacionCruzadaInterna == 0 or self.validacionCruzadaInterna == 1: 
            pass
        else: #Do internal CV
            self.originalarchivoEntrenamiento = copy.deepcopy(self.archivoEntrenamiento)
            self.originalarchivoPrueba = copy.deepcopy(self.archivoPrueba) 
        
        
    def referenciaCronometro(self, cronometro):
        """ Guarda la referencia al objeto del cronometro """
        self.cronometro = cronometro
        
        
    def referenciaAmb(self, e):
        """ Guarda la referencia al objeto del ambiente """
        self.amb = e


    def referenceAttributeTracking(self, SA):
        """ Guarda la referencia al objeto del seguimiento de atributos """
        self.SA = SA


    def referenciaConocimientoExperto(self, CE):
        """ Guarda la referencia al objeto del conocimiento experto """
        self.CE = CE
    
    
    def parsearIteraciones(self):
        """ Formatea otros parámetros clave de ejecución (es decir, iteraciones máximas, puntos de control de evaluación completa y frecuencia de seguimiento de la evaluación local). """
        puntoscontrol = self.iteracionesAprendizaje.split('.') # Analizar el string que especifica los puntos de control de evaluación, y el número máximo de iteraciones de aprendizaje.
        
        for i in range(len(puntoscontrol)): # Convierte las iteraciones de los puntos de control de strings a ints.
            puntoscontrol[i] = int(puntoscontrol[i])

        self.puntoscontrolAprendizaje = puntoscontrol
        self.maxiteracionesAprendizaje = self.puntoscontrolAprendizaje[(len(self.puntoscontrolAprendizaje)-1)]

        if self.frecuenciaSeguimiento == 0:
            self.frecuenciaSeguimiento = self.amb.datosFormateados.numInstanciasEntrenamiento # Ajustar la frecuencia de seguimiento para que coincida con el tamaño de los datos de entrenamiento - el seguimiento del aprendizaje ocurre una vez cada época


    def actualizarNombresArchivos(self, part):
        """ Un método de actualización de nombres utilizado cuando se aplica la validación cruzada interna """
        nombreTemp = copy.deepcopy(self.originalarchivoEntrenamiento)
        folderName = self.originalarchivoEntrenamiento # [0:len(self.originalarchivoEntrenamiento)-4]
        fileName = nombreTemp.split('\\')
        fileName = fileName[len(fileName)-1]
        #fileName = fileName[0:len(self.originalarchivoEntrenamiento)-4]
        
        self.archivoEntrenamiento = folderName+'\\'+fileName+'_CV_'+str(part)+'_Train'
        self.archivoPrueba = folderName+'\\'+fileName+'_CV_'+str(part)+'_Test'
        self.archivoSalida = self.nombreOriginalArchivoSalida+'_CV_'+str(part)+'_TangPenit'
        self.nombrearchivoSalidaCE = self.originalnombrearchivoSalidaCE+'_CV_'+str(part)+'_TangPenit'
            
            
    def overrideParameters(self):
        """ Overrides user specified parameters for algorithm features that can not be applied to online datasets. """
        self.hacerSeguimientoAtributos = False    #Saved as Boolean
        self.hacerFeedbackAtributos = False    #Saved as Boolean
        self.usarConocimientoExperto = False     #Saved as Boolean
        self.generacionInternaCE = False #Saved as Boolean
        self.archivoPrueba = 'None'
        self.archivoEntrenamiento = 'None'
        self.hacerCompactacionReglas = False       #Saved as Boolean
        self.soloCR = False                 #Saved as Boolean
        if self.frecuenciaSeguimiento == 0:
            self.frecuenciaSeguimiento = 50
    
cons = Constantes() #To access one of the above constant values from another module, import GHCS_Constants * and use "cons.Xconstant"