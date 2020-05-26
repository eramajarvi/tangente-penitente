"""
TANGENTE PENITENTE
Nombre: tp_ConfigParseador.py
Descripcion: Maneja el archivo de configuración cargando, analizando 
             y pasando sus valores a tp_Constantes. También incluye 
             un método para generar conjuntos de datos para la validación cruzada.
"""

# Importar modulos requeridos
from tp_Constantes import *
import os
import copy
import random
# 

class ConfigParseador:
    def __init__(self, filename):
        random.seed(1) #Same Random Seed always used here, such that the same CV datasets will be generated if run again.
        self.commentChar = '#'
        self.paramChar =  '='
        self.parameters = self.parsearConfiguracion(filename) #Parse the configuration file and get all parameters.
        cons.fijarConstantes(self.parameters) #Begin building constants Class using parameters from configuration file
        
        if cons.validacionCruzadaInterna == 0 or cons.validacionCruzadaInterna == 1: 
            pass
        else: #Do internal CV
            self.partirVC()
        
 
    def parsearConfiguracion(self, filename):
        """ Parse the Configuration File"""
        parameters = {}
        try:
            f = open(filename,'rU')
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', filename)
            raise 
        else:
            for line in f:
                # First, remove comments:
                if self.commentChar in line:
                    # split on comment char, keep only the part before
                    line, comment = line.split(self.commentChar, 1)
                # Second, find lines with an parameter=value:
                if self.paramChar in line:
                    # split on parameter char:
                    parameter, value = line.split(self.paramChar, 1)
                    # strip spaces:
                    parameter = parameter.strip()
                    value = value.strip()
                    # store in dictionary:
                    parameters[parameter] = value
                    
            f.close()
        return parameters
    
    
    def partirVC(self):
        """ Given a data set, CVPart randomly partitions it into X random balanced 
        partitions for cross validation which are individually saved in the specified file. 
        filePath - specifies the path and name of the new datasets. """
        numPartitions = cons.validacionCruzadaInterna
        folderName = copy.deepcopy(cons.trainFile)
        fileName = folderName.split('\\')
        fileName = fileName[len(fileName)-1]
        filePath = folderName+'\\'+fileName

        #Make folder for CV Datasets
        if not os.path.exists(folderName):
            os.mkdir(folderName)     
            
        # Open the specified data file.
        try:
            f = open(cons.trainFile+'.txt', 'rU')
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', cons.trainFile+'.txt')
            raise 
        else:
            datasetList = []
            headerList = f.readline().rstrip('\n').split('\t')  #strip off first row
            for line in f:
                lineList = line.strip('\n').split('\t')
                datasetList.append(lineList)
            f.close()
        dataLength = len(datasetList)   
            
        #Characterize Phenotype----------------------------------------------------------------------------
        discretePhenotype = True
        if cons.labelPhenotype in headerList:
            phenotypeRef = headerList.index(cons.labelPhenotype)
        else:
            print("Error: ConfigParser - Phenotype Label not found.")

        inst = 0
        classDict = {}
        while len(list(classDict.keys())) <= cons.discreteAttributeLimit and inst < dataLength:  #Checks which discriminate between discrete and continuous attribute
            target = datasetList[inst][phenotypeRef]
            if target in list(classDict.keys()):  #Check if we've seen this attribute state yet.
                classDict[target] += 1
            else: #New state observed
                classDict[target] = 1
            inst += 1
            
        if len(list(classDict.keys())) > cons.discreteAttributeLimit:
            discretePhenotype = False
        else:
            pass
        #---------------------------------------------------------------------------------------------------
        
        CVList = [] #stores all partitions
        for x in range(numPartitions):
            CVList.append([])
        
        if discretePhenotype:
            masterList = []
            classKeys = list(classDict.keys())
            for i in range(len(classKeys)):
                masterList.append([])
            for i in datasetList:
                notfound = True
                j = 0
                while notfound:
                    if i[phenotypeRef] == classKeys[j]:
                        masterList[j].append(i)
                        notfound = False
                    j += 1
            
            #Randomize class instances before partitioning------------------
            from random import shuffle
            for i in range(len(classKeys)):
                shuffle(masterList[i])
            #---------------------------------------------------------------
                
            for currentClass in masterList:
                currPart = 0
                counter = 0
                for x in currentClass:
                    CVList[currPart].append(x)
                    counter += 1
                    currPart = counter%numPartitions
                    
            self.hacerParticiones(CVList,numPartitions,filePath,headerList)
            
        else: #Continuous Endpoint
            from random import shuffle
            shuffle(datasetList)  
            currPart = 0
            counter = 0
            for x in datasetList:
                CVList[currPart].append(x)
                counter += 1
                currPart = counter%numPartitions
            
            self.hacerParticiones(CVList,numPartitions,filePath,headerList)
            
            
    def hacerParticiones(self,CVList,numPartitions,filePath,headerList):         
        for part in range(numPartitions): #Builds CV data files.
            if not os.path.exists(filePath+'_CV_'+str(part)+'_Train.txt') or not os.path.exists(filePath+'_CV_'+str(part)+'_Test.txt'):
                print("Making new CV files:  "+filePath+'_CV_'+str(part))
                trainFile = open(filePath+'_CV_'+str(part)+'_Train.txt','w')
                testFile = open(filePath+'_CV_'+str(part)+'_Test.txt','w')
                
                for i in range(len(headerList)):   
                    if i < len(headerList)-1:
                        testFile.write(headerList[i] + "\t")
                        trainFile.write(headerList[i] + "\t")  
                    else:
                        testFile.write(headerList[i] + "\n")
                        trainFile.write(headerList[i] + "\n") 
    
                testList=CVList[part]
                trainList=[]
                tempList = []                 
                for x in range(numPartitions): 
                    tempList.append(x)                            
                tempList.pop(part)
    
                for v in tempList: #for each training partition
                    trainList.extend(CVList[v])    
            
                for i in testList: #Write to Test Datafile
                    tempString = ''
                    for point in range(len(i)):
                        if point < len(i)-1:
                            tempString = tempString + str(i[point])+"\t"
                        else:
                            tempString = tempString +str(i[point])+"\n"                        
                    testFile.write(tempString)
                          
                for i in trainList: #Write to Train Datafile
                    tempString = ''
                    for point in range(len(i)):
                        if point < len(i)-1:
                            tempString = tempString + str(i[point])+"\t"
                        else:
                            tempString = tempString +str(i[point])+"\n"                        
                    trainFile.write(tempString)
                                                    
                trainFile.close()
                testFile.close()  
