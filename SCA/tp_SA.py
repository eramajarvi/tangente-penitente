"""
TANGENTE PENITENTE
Nombre: tp_SA.py
Descripcion: Maneja el almacenamiento, la actualización y la aplicación de la 
             heurística de seguimiento de atributos y del feedback.  Esta 
             estrategia fue propuesta y publicada por Ryan Urbanowicz, Ambrose 
             Granizo-Mackenzie y Jason Moore en "Instance-Linked Attribute Tracking 
             and Feedback for Michigan-Style Supervised Learning Classifier Systems". [2012].
"""

# Importar modulos requeridos
from tp_Constantes import *
import copy
import random
#

class AttributeTracking:
    def __init__(self, doAttTrack):
        """ Initialize Attribute Tracking Object"""
        self.percent = 0.0
        if doAttTrack:
            self.probabilityList = []
            self.attAccuracySums = [[0]*cons.env.formatData.numAttributes for i in range(cons.env.formatData.numTrainInstances)]
            if cons.doPopulationReboot:
                self.rebootAT()

    
    def updatePercent(self, exploreIter):
        """ Determines the frequency with which attribute feedback is applied within the GA.  """
        self.percent = exploreIter/float(cons.maxLearningIterations)
        
           
    def updateAttTrack(self, pop):
        """ Attribute Tracking update."""
        dataRef = cons.env.dataRef
        for ref in pop.correctSet:
            for each in pop.popSet[ref].specifiedAttList:
                self.attAccuracySums[dataRef][each] += (pop.popSet[ref].accuracy) #Add rule accuracy

    
    def getTrackProb(self):
        """ Returns the tracking probability list. """
        return self.probabilityList
       
       
    def genTrackProb(self):
        """ Calculate and return the attribute probabilities based on the attribute tracking scores. """
        #Choose a random data instance attribute tracking scores
        currentInstance = random.randint(0,cons.env.formatData.numTrainInstances-1)
        #Get data set reference.
        trackList = copy.deepcopy(self.attAccuracySums[currentInstance])
        #----------------------------------------
        minVal = min(trackList)
        for i in range(len(trackList)):
            trackList[i] = trackList[i] - minVal
        maxVal = max(trackList)
        #----------------------------------------
        probList = []
        for i in range(cons.env.formatData.numAttributes):
            if maxVal == 0.0:
                probList.append(0.5)
            else:
                probList.append(trackList[i]/float(maxVal + maxVal*0.01))  #perhaps make this float a constant, or think of better way to do this.

        self.probabilityList = probList
      
      
    def sumGlobalAttTrack(self):
        """ For each attribute, sum the attribute tracking scores over all instances. For Reporting and Debugging"""
        globalAttTrack = [0.0 for i in range(cons.env.formatData.numAttributes)]
        for i in range(cons.env.formatData.numAttributes):
            for j in range(cons.env.formatData.numTrainInstances):
                globalAttTrack[i] += self.attAccuracySums[j][i]
        return globalAttTrack


    def rebootAT(self):
        """ Rebuilds attribute tracking scores from previously stored run. """
        try: #Obtain existing attribute tracking
            f = open(cons.popRebootPath+"_AttTrack.txt", 'rU')
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', cons.popRebootPath+"_AttTrack.txt")
            raise 
        else:
            junkList = f.readline().rstrip('\n').split('\t')
            ATList = []
            for line in f:
                lineList = line.strip('\n').split('\t')
                ATList.append(lineList)
            f.close()

            #Reorder old att-track values to match new data shuffling.
            dataLink = cons.env.formatData
            for i in range(dataLink.numTrainInstances):
                targetID = dataLink.trainFormatted[i][2] #gets each instance ID
                notFound = True
                j = 0
                while notFound and j < dataLink.numTrainInstances:
                    if str(targetID) == str(ATList[j][0]): #found relevant instance
                        for w in range(dataLink.numAttributes):
                            self.attAccuracySums[i][w] = float(ATList[j][w+1])
                    j += 1              
