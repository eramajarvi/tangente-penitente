"""
TANGENTE PENITENTE
Nombre: tp_AmbienteOffline.py
Descripcion: En el contexto de las tareas de extracción y clasificación de datos, 
             el "entorno" de Tangente Penitente es un conjunto de datos con un número 
             limitado de instancias con cierto número de atributos y un único endpoint 
             (típicamente un fenotipo o clase discreta) de interés. Este módulo gestiona 
             el paso de Tangente Penitente por las iteraciones de aprendizaje, y las 
             instancias de datos respectivamente. Se incluyen métodos especiales para 
             pasar del aprendizaje a la evaluación de un conjunto de datos de capacitación.
"""

# Importar modulos requeridos
from exstracs_data import DataManagement
from exstracs_constants import * 
import sys
# 

class Offline_Environment:
    def __init__(self):
        """  """
        #Initialize global variables-------------------------------------------------
        self.dataRef = 0
        self.storeDataRef = 0
        self.formatData = DataManagement(cons.trainFile, cons.testFile)
        
        self.currentTrainState = self.formatData.trainFormatted[self.dataRef][0]
        self.currentTrainPhenotype = self.formatData.trainFormatted[self.dataRef][1]
        if cons.testFile == 'None':
            pass
        else:
            self.currentTestState = self.formatData.testFormatted[self.dataRef][0]
            self.currentTestPhenotype = self.formatData.testFormatted[self.dataRef][1]
        

    def getTrainInstance(self):
        """ Returns the current training instance. """  #NOTE: Probably faster way of doing this than additional 'if' statement every learning iteration
        return [self.currentTrainState, self.currentTrainPhenotype] #Return unadulterated training data
        
        
    def getTestInstance(self):
        """ Returns the current training instance. """
        return [self.currentTestState, self.currentTestPhenotype]
    
    
    def newInstance(self, isTraining): 
        """  Shifts the environment to the next instance in the data. """
        #-------------------------------------------------------
        # Training Data
        #-------------------------------------------------------
        if isTraining: 
            if self.dataRef < (self.formatData.numTrainInstances-1):
                self.dataRef += 1
                self.currentTrainState = self.formatData.trainFormatted[self.dataRef][0]
                self.currentTrainPhenotype = self.formatData.trainFormatted[self.dataRef][1]

            else: #Once learning has completed an epoch (i.e. learning iterations though the entire dataset) it starts back at the first instance in the data)
                self.resetDataRef(isTraining)
        #-------------------------------------------------------
        # Testing Data
        #-------------------------------------------------------
        else: 
            if self.dataRef < (self.formatData.numTestInstances-1):
                self.dataRef += 1
                self.currentTestState = self.formatData.testFormatted[self.dataRef][0]
                self.currentTestPhenotype = self.formatData.testFormatted[self.dataRef][1]
      
      
    def resetDataRef(self, isTraining):
        """ Resets the iteration count through the current data set. """
        self.dataRef = 0 
        if isTraining:
            self.currentTrainState = self.formatData.trainFormatted[self.dataRef][0]
            self.currentTrainPhenotype = self.formatData.trainFormatted[self.dataRef][1]
        else:
            self.currentTestState = self.formatData.testFormatted[self.dataRef][0]
            self.currentTestPhenotype = self.formatData.testFormatted[self.dataRef][1]


    def startEvaluationMode(self):
        """ Turns on evaluation mode.  Saves the instance we left off in the training data. Also important when using RAIN."""
        self.storeDataRef = self.dataRef
        
        
    def stopEvaluationMode(self):
        """ Turns off evaluation mode.  Re-establishes place in dataset."""
        self.dataRef = self.storeDataRef
