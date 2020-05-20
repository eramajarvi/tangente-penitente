"""
TANGENTE PENITENTE
Nombre:      TangentePenitente_Main.py
Descripcion: Este modulo es para ejecutar el algoritmo de Tangente Penitente localmente.
             La inicializacion del algoritmo y sus mecanismos clave ocurren aqui
"""

# Importar modulos requeridos
from tp_Cronometro import Cronometro
from tp_ConfigParseador import ConfigParseador
from tp_AmbienteOffline import AmbienteOffline
from tp_AmbienteOnline import AmbienteOnline
from tp_Algoritmo import Algoritmo
from tp_Constantes import *
from tp_SA import SeguimientoAtributos
from tp_CE import ConocimientoExperto
#


# Obtener el archivo de configuracion
archivoConfiguracion = "Configuracion-TangentePenitente.txt"

# Inicializa el objeto de parametros - esto parsea el archivo de configuracion y almacena todas las constantes y parametros
ConfigParseador(archivoConfiguracion)

if cons.datosOffline:  
    print('Tangente Penitente: Modo con Ambiente Offline iniciado')

    if cons.validacionCruzadaInterna == 0 or cons.validacionCruzadaInterna == 1:  # No se hace validacion cruzada interna
        # Enganche del cronometro - cuenta el tiempo de ejecucion del algoritmo y sus componentes
        tempo = Cronometro() # Tiempo
        cons.referenciaCronometro(tempo)
        cons.cronometro.startTimeInit()

        # Inicializa el objeto del ambiente - esto administra los datos presentados a Tangente Penitente
        amb = AmbienteOffline() 
        cons.referenceEnv(amb) # Envia referencia del objeto ambiente a las constantes - para acceder desde cualquier lugar en TP
        cons.parsearIteraciones() 
        
        # Instanciar el algoritmo de Tangente Penitente
        algoritmo = Algoritmo()

        if cons.soloPrueba:
            cons.cronometro.stopTimeInit()
            algoritmo.correrSoloPrueba()

        else:
            if cons.soloCR:
                cons.cronometro.stopTimeInit()
                algoritmo.correrSoloCR()

            else: 
                if cons.soloPuntajesCE:
                    cons.cronometro.stopTimeInit()
                    CE = ConocimientoExperto(cons)
                    print("Tangente Penitente: Ejecucion del algoritmo completada")

                else: # Ejecuta el algoritmo de Tangente Penitente
                    if cons.useExpertKnowledge: # Transforma los puntajes de CE en pesos de probabilidades para el covering. Se hace una vez. El CE desde ser proveido externamente
                        cons.cronometro.startTimeEK() 
                        CE = ConocimientoExperto(cons)
                        cons.referenciaConocimientoExperto(CE)
                        cons.cronometro.stopTimeEK()
                        
                    if cons.hacerSeguimientoAtributos:
                        cons.cronometro.startTimeAT()
                        AT = SeguimientoAtributos(True)
                        cons.cronometro.stopTimeAT()

                    else:
                        AT = SeguimientoAtributos(False)

                    cons.referenceAttributeTracking(AT)
                    cons.cronometro.stopTimeInit()
                    algoritmo.correrTP()

    else:
        print("Ejecutando Tangente Penitente con validacion cruzada interna...") 
        
        for part in range(cons.validacionCruzadaInterna):
            cons.actualizarNombresArchivos(part)  
            
            # Enganche del cronometro - cuenta el tiempo de ejecucion del algoritmo y sus componentes
            tempo = Cronometro()
            cons.referenciaCronometro(tempo)
            cons.cronometro.startTimeInit()

            # Inicializa el objeto del ambiente - esto administra los datos presentados a Tangente Penitente
            amb = AmbienteOffline()
            cons.referenciaAmb(amb) # Envia referencia del objeto ambiente a las constantes - para acceder desde cualquier lugar en TP
            cons.parsearIteraciones() 
            
            # Instanciar el algoritmo de Tangente Penitente
            algoritmo = Algoritmo()
            if cons.soloPrueba:
                cons.cronometro.stopTimeInit()
                algoritmo.correrSoloPrueba()

            else:
                if cons.soloCR:
                    cons.cronometro.stopTimeInit()
                    algoritmo.correrSoloCR()

                else: 
                    if cons.soloPuntajesCE:
                        cons.cronometro.stopTimeInit()
                        cons.runFilter()
                        print("Tangente Penitente: Ejecucion del algoritmo completada")

                    else: #Run the ExSTraCS algorithm.
                        if cons.useExpertKnowledge: #Transform CE scores into probabilities weights for covering. Done once. CE must be externally provided.
                            cons.timer.startTimeEK()
                            CE = ConocimientoExperto(cons)
                            cons.referenceExpertKnowledge(CE)
                            cons.timer.stopTimeEK()
                            
                        if cons.doAttributeTracking:
                            cons.timer.startTimeAT()
                            AT = SeguimientoAtributos(True)
                            cons.timer.stopTimeAT()

                        else:
                            AT = SeguimientoAtributos(False)

                        cons.referenceAttributeTracking(AT)
                        cons.timer.stopTimeInit()
                        algoritmo.correrTP()

else: # Conjunto de datos online (No permite Conocimiento Experto, Seguimiento de Atributos, o validacion cruzada)
    # Enganche del cronometro - cuenta el tiempo de ejecucion del algoritmo y sus componentes
    print("Tangente Penitente: Modo con Ambiente Online iniciado") 
    tempo = Cronometro()
    cons.referenciaCronometro(tempo)
    cons.cronometro.startTimeInit()
    cons.overrideParameters()
    
    # Inicializa el objeto del ambiente - esto administra los datos presentados a Tangente Penitente
    amb = AmbienteOnline()
    cons.referenciaAmb(amb) # Envia referencia del objeto ambiente a las constantes - para acceder desde cualquier lugar en TP
    cons.parsearIteraciones() 
    
    #Instantiate ExSTraCS Algorithm
    algoritmo = Algoritmo()
    cons.cronometro.stopTimeInit()
    if cons.soloCR:
        algoritmo.correrSoloCR()
    else: 
        algoritmo.correrTP()