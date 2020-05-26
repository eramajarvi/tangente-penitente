"""
TANGENTE PENITENTE
Nombre: tp_Prediccion.py
Descripcion: Basándose en un determinado conjunto de coincidencias, este módulo 
             utiliza un esquema de votación para seleccionar la predicción del 
             fenotipo para Tangente Penitente.
"""

# Importar modulos requeridos
from tp_Constantes import *
import random
#

class Prediccion:
    def __init__(self, population):  #now takes in population ( have to reference the match set to do prediction)  pop.matchSet
        """ Constructs the voting array and determines the prediction decision. """
        self.decision = None
        #-------------------------------------------------------
        # DISCRETE PHENOTYPE
        #-------------------------------------------------------
        if cons.env.formatData.discretePhenotype: 
            self.vote = {}
            self.tieBreak_Numerosity = {}
            self.tieBreak_TimeStamp = {}
            
            for eachClass in cons.amb.formatData.phenotypeList:
                self.vote[eachClass] = 0.0
                self.tieBreak_Numerosity[eachClass] = 0.0
                self.tieBreak_TimeStamp[eachClass] = 0.0
                
            for ref in population.matchSet:
                cl = population.popSet[ref]
                self.vote[cl.phenotype] += cl.fitness * cl.numerosity * cons.env.formatData.classPredictionWeights[cl.phenotype]
                self.tieBreak_Numerosity[cl.phenotype] += cl.numerosity
                self.tieBreak_TimeStamp[cl.phenotype] += cl.initTimeStamp
                
            highVal = 0.0
            bestClass = [] #Prediction is set up to handle best class ties for problems with more than 2 classes
            for thisClass in cons.amb.formatData.phenotypeList:
                if self.vote[thisClass] >= highVal:
                    highVal = self.vote[thisClass]
                    
            for thisClass in cons.amb.formatData.phenotypeList:
                if self.vote[thisClass] == highVal: #Tie for best class
                    bestClass.append(thisClass)
            #---------------------------
            if highVal == 0.0:
                self.decision = None
            #-----------------------------------------------------------------------
            elif len(bestClass) > 1: #Randomly choose between the best tied classes
                bestNum = 0
                newBestClass = []
                for thisClass in bestClass:
                    if self.tieBreak_Numerosity[thisClass] >= bestNum:
                        bestNum = self.tieBreak_Numerosity[thisClass]
                        
                for thisClass in bestClass:
                    if self.tieBreak_Numerosity[thisClass] == bestNum:
                        newBestClass.append(thisClass)
                #-----------------------------------------------------------------------
                if len(newBestClass) > 1:  #still a tie
                    bestStamp = 0
                    newestBestClass = []
                    for thisClass in newBestClass:
                        if self.tieBreak_TimeStamp[thisClass] >= bestStamp:
                            bestStamp = self.tieBreak_TimeStamp[thisClass]
                            
                    for thisClass in newBestClass:
                        if self.tieBreak_TimeStamp[thisClass] == bestStamp:
                            newestBestClass.append(thisClass)
                    #-----------------------------------------------------------------------
                    if len(newestBestClass) > 1: # Prediction is completely tied - ExSTraCS has no useful information for making a prediction
                        self.decision = 'Tie'
                else:
                    self.decision = newBestClass[0]
            #----------------------------------------------------------------------
            else: #One best class determined by fitness vote
                self.decision = bestClass[0]
        
        #-------------------------------------------------------
        # CONTINUOUS PHENOTYPE
        #-------------------------------------------------------
        else: 
            print("Prediction - Error: ExSTraCS 2.0 can not handle continuous endpoints.")

                        
    def getFitnessSum(self,population,low,high):
        """ Get the fitness Sum of rules in the rule-set. For continuous phenotype prediction. """
        fitSum = 0
        for ref in population.matchSet:
            cl = population.popSet[ref]
            if cl.phenotype[0] <= low and cl.phenotype[1] >= high: #if classifier range subsumes segment range.
                fitSum += cl.fitness
        return fitSum
    
                    
    def obtenerDecision(self):
        """ Returns prediction decision. """
        return self.decision

    def getSet(self):
        """ Returns prediction decision. """
        return self.vote