"""
TANGENTE PENITENTE
Nombre:      TangentePenitente_Main.py
Descripcion: Este modulo es para ejecutar el algoritmo de Tangente Penitente localmente.
             La inicializacion del algoritmo y sus mecanismos clave ocurren aqui
"""

# Importar modulos requeridos
from tp_Cronometro import Timer
from tp_configParseador import ConfigParser
from tp_AmbienteOffline import Offline_Environment
from tp_AmbienteOnline import Online_Environment
from tp_Algoritmo import ExSTraCS
from tp_Constantes import *
from tp_SA import AttributeTracking
from tp_CE import ExpertKnowledge
#


# Obtener el archivo de configuracion
archivoConfiguracion = "Configuracion-TangentePenitente.txt"

#Initialize the Parameters object - this will parse the configuration file and store all constants and parameters.
ConfigParser(archivoConfiguracion)

if cons.offlineData:  
    print('ExSTraCS Offline Environment Mode Initiated.')
    if cons.internalCrossValidation == 0 or cons.internalCrossValidation == 1:  #No internal Cross Validation
        #Engage Timer - tracks run time of algorithm and it's components.
        timer = Timer() #TIME
        cons.referenceTimer(timer)
        cons.timer.startTimeInit()
        #Initialize the Environment object - this manages the data presented to ExSTraCS 
        env = Offline_Environment()
        cons.referenceEnv(env) #Send reference to environment object to constants - to access from anywhere in ExSTraCS
        cons.parseIterations() 
        
        #Instantiate ExSTraCS Algorithm
        algorithm = ExSTraCS()
        if cons.onlyTest:
            cons.timer.stopTimeInit()
            algorithm.runTestonly()
        else:
            if cons.onlyRC:
                cons.timer.stopTimeInit()
                algorithm.runRConly()
            else: 
                if cons.onlyEKScores:
                    cons.timer.stopTimeInit()
                    EK = ExpertKnowledge(cons)
                    print("Algorithm Run Complete")
                else: #Run the ExSTraCS algorithm.
                    if cons.useExpertKnowledge: #Transform EK scores into probabilities weights for covering. Done once. EK must be externally provided.
                        cons.timer.startTimeEK()
                        EK = ExpertKnowledge(cons)
                        cons.referenceExpertKnowledge(EK)
                        cons.timer.stopTimeEK()
                        
                    if cons.doAttributeTracking:
                        cons.timer.startTimeAT()
                        AT = AttributeTracking(True)
                        cons.timer.stopTimeAT()
                    else:
                        AT = AttributeTracking(False)
                    cons.referenceAttributeTracking(AT)
                    cons.timer.stopTimeInit()
                    algorithm.runExSTraCS()
    else:
        print("Running ExSTraCS with Internal Cross Validation") 
        for part in range(cons.internalCrossValidation):
            cons.updateFileNames(part)  
            
            #Engage Timer - tracks run time of algorithm and it's components.
            timer = Timer() #TIME
            cons.referenceTimer(timer)
            cons.timer.startTimeInit()
            #Initialize the Environment object - this manages the data presented to ExSTraCS 
            env = Offline_Environment()
            cons.referenceEnv(env) #Send reference to environment object to constants - to access from anywhere in ExSTraCS
            cons.parseIterations() 
            
            #Instantiate ExSTraCS Algorithm
            algorithm = ExSTraCS()
            if cons.onlyTest:
                cons.timer.stopTimeInit()
                algorithm.runTestonly()
            else:
                if cons.onlyRC:
                    cons.timer.stopTimeInit()
                    algorithm.runRConly()
                else: 
                    if cons.onlyEKScores:
                        cons.timer.stopTimeInit()
                        cons.runFilter()
                        print("Algorithm Run Complete") 
                    else: #Run the ExSTraCS algorithm.
                        if cons.useExpertKnowledge: #Transform EK scores into probabilities weights for covering. Done once. EK must be externally provided.
                            cons.timer.startTimeEK()
                            EK = ExpertKnowledge(cons)
                            cons.referenceExpertKnowledge(EK)
                            cons.timer.stopTimeEK()
                            
                        if cons.doAttributeTracking:
                            cons.timer.startTimeAT()
                            AT = AttributeTracking(True)
                            cons.timer.stopTimeAT()
                        else:
                            AT = AttributeTracking(False)
                        cons.referenceAttributeTracking(AT)
                        cons.timer.stopTimeInit()
                        algorithm.runExSTraCS()
else: #Online Dataset (Does not allow Expert Knowledge, Attribute Tracking, Attribute Feedback, or cross-validation)
    #Engage Timer - tracks run time of algorithm and it's components.
    print("ExSTraCS Online Environment Mode Initiated.") 
    timer = Timer() #TIME
    cons.referenceTimer(timer)
    cons.timer.startTimeInit()
    cons.overrideParameters()
    
    #Initialize the Environment object - this manages the data presented to ExSTraCS 
    env = Online_Environment()
    cons.referenceEnv(env) #Send reference to environment object to constants - to access from anywhere in ExSTraCS
    cons.parseIterations() 
    
    #Instantiate ExSTraCS Algorithm
    algorithm = ExSTraCS()
    cons.timer.stopTimeInit()
    if cons.onlyRC:
        algorithm.runRConly()
    else: 
        algorithm.runExSTraCS()