"""
TANGENTE PENITENTE
Nombre: tp_AmbienteOnline.py
Descripcion: Tangente Penitente es más adecuado para el aprendizaje 
             iterativo fuera de línea, sin embargo, este módulo se ha 
             puesto en práctica como un ejemplo de cómo Tangente Penitente 
             puede utilizarse para realizar también aprendizaje Online. 
             En este caso, este módulo ha sido escrito para realizar un 
             aprendizaje en línea para un problema de n-multiplexores, en 
             el que las instancias de capacitación se generan de forma online. 
             Este módulo no ha sido probado completamente.
"""

# Importar modulos requeridos
from tp_Datos import GestionDatos
from tp_Constantes import *
#from Online_Learning.problem_multiplexer import *  #http://stackoverflow.com/questions/4383571/importing-files-from-different-folder-in-python
import sys
#

class AmbienteOnline:
    def __init__(self):
        """ Specify source of online data with appropriate method. """
        trainFile = None
        testFile = None
        """ Specifically Designed to get n-bit Mulitplexer problem data
        Valid Multiplexers:
        Address Bits = 1 (3-Multiplexer)
        Address Bits = 2 (6-Multiplexer)
        Address Bits = 3 (11-Multiplexer)   
        Address Bits = 4 (20-Multiplexer)  
        Address Bits = 5 (37-Multiplexer)                      
        Address Bits = 6 (70-Multiplexer)   
        Address Bits = 7 (135-Multiplexer)   
        Address Bits = 8 (264-Multiplexer) 
        """
        #Multiplexer specific variables
        self.num_bits = 6 # E.g. 3, 6, 11, 20...

        infoList = self.mulitplexerInfoList()

        self.formatData = GestionDatos(trainFile, testFile, infoList)
        first_Instance = generate_multiplexer_instance(self.num_bits)
        print(first_Instance)
        self.currentTrainState = first_Instance[0]
        self.currentTrainPhenotype = first_Instance[1]

        
    def mulitplexerInfoList(self):
        """ Manually specify all dataset parameters for Multiplexer problem. """      
        numAttributes = self.num_bits
        discretePhenotype = True
        attributeInfo = []
        for i in range(self.num_bits):
            attributeInfo.append([0,[]])

        phenotypeList = ['0','1']
        phenotypeRange = None
        trainHeaderList = []
        for i in range(self.num_bits):
            trainHeaderList.append('X_'+str(i)) #Give online data some arbitrary attribute names.
        numTrainInstances = 0
        infoList = [numAttributes,discretePhenotype,attributeInfo,phenotypeList,phenotypeRange,trainHeaderList,numTrainInstances]
        print(infoList)
        return infoList
        
            
    def newInstance(self,eval): 
        """  Shifts the environment to the next instance in the data. """
        new_Instance = generate_multiplexer_instance(self.num_bits)
        self.currentTrainState = new_Instance[0]
        self.currentTrainPhenotype = new_Instance[1]
         

    def getTrainInstance(self):
        """ Returns the current training instance. """ 
        return [self.currentTrainState, self.currentTrainPhenotype]
        
    def startEvaluationMode(self):
        """ Turns on evaluation mode.  Saves the instance we left off in the training data. Also important when using RAIN."""
        pass
        
        
    def stopEvaluationMode(self):
        """ Turns off evaluation mode.  Re-establishes place in dataset."""
        pass