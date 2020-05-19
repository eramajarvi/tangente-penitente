"""
TANGENTE PENITENTE
Nombre: tp_CE.py
Descripcion: Un paso de preprocesamiento cuando se activa en Tangente Penitente. 
             Convierte las puntuaciones numéricas del conocimiento experto de 
             cualquier fuente en probabilidades para orientar el mecanismo de 
             covering en la determinación de los atributos que se especificarán 
             y los que se generalizarán. Esta estrategia fue propuesta y publicada 
             por Ryan Urbanowicz, Delaney Granizo-Mackenzie y Jason Moore en 
             "Using Expert Knowledge to Guide Covering and Mutation in a Michigan 
             Style Learning Classifier System to Detecting Epistasis and Heterogeneity". [2012].
"""

# Importar modulos requeridos
import os
import copy
import time
from RBA.relieff import *
from RBA.surf import *
from RBA.surfstar import *
from RBA.multisurf import *
from RBA.turf_wrapper import *
#

class ExpertKnowledge:
    def __init__(self, cons):
        """ Expert knowledge initialization - Scores ordered as the appear in the dataset"""
        self.scores = None
        self.EKRank = None
 
        if cons.internal_EK_Generation or cons.onlyEKScores:
            print("ExpertKnowledge: Begin internal generation of EK.")
            self.scores = self.runFilter(cons)
        else:
            print("ExpertKnowledge: Loading external EK.")
            self.scores = self.loadEK(cons.EK_source, cons)
        
        #print self.scores
        self.adjustScores(cons) #Ensures that scores are non-negative.

        #New specification protocol
        self.EKSum = sum(self.scores)
        self.EKRank = []
        tempEK = copy.deepcopy(self.scores)
        for i in range(len(self.scores)):
            bestEK = tempEK[0]
            bestC = 0
            for j in range(1,len(tempEK)):
                if tempEK[j] > bestEK:
                    bestEK = tempEK[j]
                    bestC = j
            self.EKRank.append(bestC)
            tempEK[bestC] = 0  
        #print self.EKRank #Debugging
        #Used to select attributes for specification in covering (without replacement)
        self.refList = []
        for i in range(len(self.scores)):
            self.refList.append(i)

        #Used to select attributes for specification in covering (without replacement)
        self.refList = []
        for i in range(len(self.scores)):
            self.refList.append(i)

        #Convert the list from ajusted scores to probabilities
        #----------------------------------------
        maxVal = max(self.scores)
        probList = []
        for i in range(cons.env.formatData.numAttributes):
            if maxVal == 0.0:
                probList.append(0.5)
            else:
                probList.append(self.scores[i]/float(maxVal + maxVal*0.01))  #perhaps make this float a constant, or think of better way to do this.

        self.EKprobabilityList = probList
        #print self.EKprobabilityList #Debugging


    def adjustScores(self,cons):
        """ Ensure that the minimum score value is zero. """
        minEK = min(self.scores)
        if minEK < 0:
            for i in range(len(self.scores)):
                self.scores[i] = self.scores[i] - minEK + cons.init_fit #Addition of 0.01 prevents lowest scoring attribute from having zero weight.


    def runFilter(self, cons):
        """ Runs the specified filter algorithm and creates a filter output text file in the same format as MDR (multifactor dimmensionality reduction) software. """
        fileName = str(cons.outEKFileName) + '_'+str(cons.filterAlgorithm) +'_scores.txt' 
            
        if not os.path.exists(fileName):
            globalStartRef = time.time()
            labelName = None
            dummy = None
            dummy2 = None
            if cons.filterAlgorithm=="multisurf_turf":
                turf = TuRFMe(cons.env,cons.filterAlgorithm, cons.turfPercent, dummy, dummy2)
                filterScores = turf.filterScores
                labelName = 'MultiSURF_TuRF'
            elif cons.filterAlgorithm=="surfstar_turf":
                turf = TuRFMe(cons.env,cons.filterAlgorithm, cons.turfPercent,cons.reliefSampleFraction, dummy)
                filterScores = turf.filterScores
                labelName = 'SURFStar_TuRF'
            elif cons.filterAlgorithm=="surf_turf":
                turf = TuRFMe(cons.env,cons.filterAlgorithm, cons.turfPercent,cons.reliefSampleFraction, dummy)
                filterScores = turf.filterScores
                labelName = 'SURF_TuRF'
            elif cons.filterAlgorithm=="relieff_turf":
                turf = TuRFMe(cons.env,cons.filterAlgorithm, cons.turfPercent,cons.reliefSampleFraction,cons.reliefNeighbors)
                filterScores = turf.filterScores
                labelName = 'ReliefF_TuRF'

            elif cons.filterAlgorithm=="multisurf":
                filterScores = Run_MultiSURF(cons.env.formatData)
                labelName = 'MultiSURF'
            elif cons.filterAlgorithm=="surfstar":
                filterScores = Run_SURFStar(cons.env.formatData,cons.reliefSampleFraction)
                labelName = 'SURFStar'
            elif cons.filterAlgorithm=="surf":
                filterScores = Run_SURF(cons.env.formatData,cons.reliefSampleFraction)
                labelName = 'SURF'
            elif cons.filterAlgorithm=="relieff":
                filterScores = Run_ReliefF(cons.env.formatData, cons.reliefSampleFraction,cons.reliefNeighbors)
                labelName = 'ReliefF'
            else:
                print("ERROR: Algorithm not found.")
            globalTime = (time.time() - globalStartRef)
            
            #OUTPUT RELEIF-BASED ATTRIBUTE SCORE FILE---------------------------------------------
            try:  
                filterOut = open(fileName,'w') 
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open', fileName)
                raise 

            print(filterScores)
            filterOut.write(str(labelName)+" Analysis Completed with ExSTraCS" + '\n')
            filterOut.write("Run Time (sec):" +str(globalTime)+'\n')
            filterOut.write("=== SCORES ===" +'\n')
            scoreList = []
            for i in range(len(filterScores)):
                scoreList.append([cons.env.formatData.trainHeaderList[i],filterScores[i]])
            sortedFilterList = sorted(scoreList,key=lambda test: test[1], reverse=True)
            #print sortedFilterList #Debugging
            for i in range(len(sortedFilterList)):
                filterOut.write(str(sortedFilterList[i][0]) +'\t')
                filterOut.write(str(sortedFilterList[i][1]) +'\t')
                filterOut.write(str(i+1) +'\n')

            filterOut.close()
 
            #----------------------------------------------------------------------------------------
            return filterScores
            
        else: #Attribute Score file already exists - load existing file and proceed without re-running attribute score algorithm
            try:
                orderedValueList = self.loadEK(cons.outEKFileName + '_'+str(cons.filterAlgorithm)+'_scores.txt', cons)
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open', cons.outEKFileName + '_'+str(cons.filterAlgorithm)+'_scores.txt')
                raise 
            else:
                return orderedValueList 
    
    
    def loadEK(self, pathName, cons):
        """ Loads an existing expert knowledge file in the Relief Format."""
        try:
            fileObject = open(pathName, 'rU')  # opens each datafile to read.
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', pathName)
            print("Error Loading Expert Knowledge File: Check EK file for content or formatting errors.")
            raise 
        else:
            print("EK File Loaded.")
            tempLine = None
            for i in range(3): #gets through garbage
                tempLine = fileObject.readline()
                
            headerDict = {}
            for i in range(cons.env.formatData.numAttributes):
                tempLine = fileObject.readline()
                tempList = tempLine.strip().split('\t')
                headerDict[tempList[0]] = float(tempList[1]) #all attributes and corresponding EK scores are hashed in a dictionary

            #Order the list by ID
            orderedValueList = []
            for i in range(cons.env.formatData.numAttributes):
                orderedValueList.append(float(headerDict[cons.env.formatData.trainHeaderList[i]])) #ordered by attribute order in dataset

        return orderedValueList
