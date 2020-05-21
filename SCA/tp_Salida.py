"""
TANGENTE PENITENTE
Nombre: tp_Salida.py
Descripcion: Este módulo contiene los métodos para generar los diferentes archivos 
             de salida generados por Tangente Penitente. Estos archivos se generan 
             en cada punto de control de aprendizaje, y en la última iteración. 
             Estos incluyen: 
             writePopStats: Resumen de las estadísticas de población
             writePop: Produce una instantánea de toda la población de reglas, incluyendo las condiciones de los clasificadores, las clases y los parámetros.
             attCo_Ocurrence: Calcula y produce puntuaciones de co-ocurrencia para cada par de atributos en el conjunto de datos.
"""

# Importar modulos requeridos
from tp_Constantes import *
from tp_SA import *
import copy
#

class AdminSalida:     

    def writePopStats(self, outFile, trainEval, testEval, exploreIter, pop, correct):
        """ Makes output text file which includes all of the parameter settings used in the run as well as all of the evaluation stats including Time Track Output. """
        if cons.outputSummary:
            try:  
                popStatsOut = open(outFile + '_'+ str(exploreIter)+'_PopStats.txt','w') # Outputs Population run stats
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open', outFile + '_'+ str(exploreIter)+'_PopStats.txt')
                raise 
            else:
                print("Writing Population Statistical Summary File...")
            
            #Evaluation of pop
            popStatsOut.write("Performance Statistics:------------------------------------------------------------------------\n")
            popStatsOut.write("Training Accuracy\tTesting Accuracy\tTraining Coverage\tTesting Coverage\n")
            
            if cons.testFile != 'None':
                popStatsOut.write(str(trainEval[0])+"\t")
                popStatsOut.write(str(testEval[0])+"\t")
                popStatsOut.write(str(trainEval[1]) +"\t")
                popStatsOut.write(str(testEval[1])+"\n\n") 
            elif cons.trainFile != 'None':
                popStatsOut.write(str(trainEval[0])+"\t")
                popStatsOut.write("NA\t")
                popStatsOut.write(str(trainEval[1]) +"\t")
                popStatsOut.write("NA\n\n")
            else:
                popStatsOut.write("NA\t")
                popStatsOut.write("NA\t")
                popStatsOut.write("NA\t")
                popStatsOut.write("NA\n\n")
            
            popStatsOut.write("Population Characterization:------------------------------------------------------------------------\n")  
            popStatsOut.write("MacroPopSize\tMicroPopSize\tGenerality\n") 
            popStatsOut.write(str(len(pop.popSet))+"\t"+ str(pop.microPopSize)+"\t"+str(pop.aveGenerality)+"\n\n")
    
            popStatsOut.write("SpecificitySum:------------------------------------------------------------------------\n")       
            headList = cons.amb.formatData.trainHeaderList #preserve order of original dataset
    
            for i in range(len(headList)): 
                if i < len(headList)-1:
                    popStatsOut.write(str(headList[i])+"\t")
                else:
                    popStatsOut.write(str(headList[i])+"\n")
                    
            # Prints out the Specification Sum for each attribute 
            for i in range(len(pop.attributeSpecList)):
                if i < len(pop.attributeSpecList)-1:
                    popStatsOut.write(str(pop.attributeSpecList[i])+"\t")
                else:
                    popStatsOut.write(str(pop.attributeSpecList[i])+"\n")  
                          
            popStatsOut.write("\nAccuracySum:------------------------------------------------------------------------\n")
            for i in range(len(headList)): 
                if i < len(headList)-1:
                    popStatsOut.write(str(headList[i])+"\t")
                else:
                    popStatsOut.write(str(headList[i])+"\n")
                    
            # Prints out the Accuracy Weighted Specification Count for each attribute 
            for i in range(len(pop.attributeAccList)):
                if i < len(pop.attributeAccList)-1:
                    popStatsOut.write(str(pop.attributeAccList[i])+"\t")
                else:
                    popStatsOut.write(str(pop.attributeAccList[i])+"\n")    
                    
            if cons.onlyRC: # When RC ONLY, there is no AttributeTrackingGlobalSums
                popStatsOut.write("\nAttributeTrackingGlobalSums:----Rule Compaction ONLY, Attribute Tracking not loaded-----------------\n")
                for i in range(len(headList)): 
                    if i < len(headList)-1:
                        popStatsOut.write(str(headList[i])+"\t")
                    else:
                        popStatsOut.write(str(headList[i])+"\n")
                for i in range(len(headList)): 
                    if i < len(headList)-1:
                        popStatsOut.write(str(0.0)+"\t")
                    else:
                        popStatsOut.write(str(0.0)+"\n")
            elif cons.doAttributeTracking:
                popStatsOut.write("\nAttributeTrackingGlobalSums:------------------------------------------------------------------------\n")
                for i in range(len(headList)): 
                    if i < len(headList)-1:
                        popStatsOut.write(str(headList[i])+"\t")
                    else:
                        popStatsOut.write(str(headList[i])+"\n")
                        
                sumGlobalAttTrack = cons.AT.sumGlobalAttTrack()        
                for i in range(len(sumGlobalAttTrack)):
                    if i < len(sumGlobalAttTrack)-1:
                        popStatsOut.write(str(sumGlobalAttTrack[i])+"\t")
                    else:
                        popStatsOut.write(str(sumGlobalAttTrack[i])+"\n") 
            else:
                popStatsOut.write("\nAttributeTrackingGlobalSums:----Tracking not applied!-----------------------------------------------\n")
                for i in range(len(headList)): 
                    if i < len(headList)-1:
                        popStatsOut.write(str(headList[i])+"\t")
                    else:
                        popStatsOut.write(str(headList[i])+"\n")
                for i in range(len(headList)): 
                    if i < len(headList)-1:
                        popStatsOut.write(str(0.0)+"\t")
                    else:
                        popStatsOut.write(str(0.0)+"\n")
                      
            #Time Track ---------------------------------------------------------------------------------------------------------     
            popStatsOut.write("\nRun Time(in minutes):------------------------------------------------------------------------\n") 
            popStatsOut.write(cons.timer.reportTimes())
            popStatsOut.write("\nCorrectTrackerSave:------------------------------------------------------------------------\n")
            for i in range(len(correct)):
                popStatsOut.write(str(correct[i])+"\t")
                    
            popStatsOut.close()

        else:
            pass
        
    
    def writePop(self, outFile, exploreIter, pop):
        """ Writes a tab delimited text file specifying the evolved rule population, including conditions, phenotypes, and all rule parameters. """
        if cons.outputPopulation:
            try:  
                rulePopOut = open(outFile + '_'+ str(exploreIter)+'_RulePop.txt','w') # Outputs tab delimited text file of rule population and respective rule stats
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open', outFile + '_'+ str(exploreIter)+'_RulePop.txt')
                raise 
            else:
                print("Writing Population as Data File...")
                
            rulePopOut.write("Specified\tCondition\tPhenotype\tFitness\tAccuracy\tNumerosity\tAveMatchSetSize\tTimeStampGA\tInitTimeStamp\tSpecificity\tDeletionProb\tCorrectCount\tMatchCount\tCorrectCover\tMatchCover\tEpochComplete\n")
    
            #Write each classifier--------------------------------------------------------------------------------------------------------------------------------------
            for cl in pop.popSet:
                rulePopOut.write(str(cl.printClassifier())) 
            rulePopOut.close() 
        else:
            pass

  
    def attCo_Occurence(self, outFile, exploreIter, pop):
        """ Calculates pairwise attribute co-occurence througout all rules in the population."""
        if cons.outputAttCoOccur:
            print("Calculating Attribute Co-occurence Scores...")
            dataLink = cons.amb.formatData
            dim = dataLink.numAttributes
            maxAtts = 50  #Test 10
            attList = []
            #-------------------------------------------------------
            # IDENTIFY ATTRIBUBTES FOR CO-OCCRRENCE EVALUATION
            #-------------------------------------------------------
            if dim <= maxAtts:
                for i in range(0,dim):
                    attList.append(i)
            else:
                tempList = copy.deepcopy(pop.attributeSpecList)
                tempList = sorted(tempList,reverse=True)
                maxVal = tempList[maxAtts]
                overflow = []
                for i in range(0,dim):
                    if pop.attributeSpecList[i] >= maxVal: #get roughly the top 50 specified attributes. (may grab some extras, depending on 
                        attList.append(i)
                        if pop.attributeSpecList[i] == maxVal:
                            overflow.append(i)
                while len(attList) > maxAtts:
                    target = random.choice(overflow)
                    attList.remove(target)
                    overflow.remove(target)
                    #print(attList)
                    
            #-------------------------------------------------------
            # CO-OCCRRENCE EVALUATION
            #-------------------------------------------------------   
            comboList = []
            castList = [None,None,0,0] #att1, att2, Specificity, Accuracy Weighted Specificity
            count = 0
            dim = dataLink.numAttributes
            #Specify all attribute pairs.
            for i in range(0, len(attList)-1):
                for j in range(i+1,len(attList)):
                    comboList.append(copy.deepcopy(castList))
                    comboList[count][0] = dataLink.trainHeaderList[attList[i]]
                    comboList[count][1] = dataLink.trainHeaderList[attList[j]]   
                    count += 1
    
            for cl in pop.popSet:
                count = 0
                for i in range(len(attList)-1):
                    for j in range(i+1,len(attList)):
                        if attList[i] in cl.specifiedAttList and attList[j] in cl.specifiedAttList:
                            comboList[count][2] += cl.numerosity
                            comboList[count][3] += cl.numerosity * cl.accuracy
                        count += 1
            
            tupleList = []
            for i in comboList:
                tupleList.append((i[0],i[1],i[2],i[3]))
            sortedComboList = sorted(tupleList,key=lambda test: test[3], reverse=True)
            print("Writing Attribute Co-occurence scores as data file...")
            try:
                f = open(outFile + '_'+ str(exploreIter)+ '_CO.txt', 'w')
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open', outFile + '_'+ str(exploreIter)+ '_CO.txt')
                raise 
            else:
                for i in range(len(sortedComboList)):
                    for j in range(len(sortedComboList[0])): #att1, att2, count, AWcount
                        if j < len(sortedComboList[0])-1:
                            f.write(str(sortedComboList[i][j])+'\t')
                        else:
                            f.write(str(sortedComboList[i][j])+'\n')
                f.close()
        else:
            pass


    def save_tracking(self, exploreIter, outFile):
        if cons.doAttributeTracking:
            """ Prints out Attribute Tracking scores to txt file. """    
            try:  
                f = open(outFile + '_'+ str(exploreIter + 1)+'_AttTrack.txt','w') # Outputs tab delimited text file of rule population and respective rule stats
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open', outFile + '_'+ str(exploreIter + 1)+'_AttTrack.txt')
                raise 
            else:
                print("Writing Attribute Tracking as Data File...")
            
            trackingSums = cons.AT.attAccuracySums
            #-------------------------------------------------------------------
            f.write(str(cons.labelInstanceID) + '\t') #Write InstanceID label
            for att in cons.amb.formatData.trainHeaderList:
                f.write(str(att) + '\t')
            f.write(str(cons.labelPhenotype)+ '\n') #Write phenotype label
            #---------------------------------------------------------------
            for i in range(len(trackingSums)):
                trackList = trackingSums[i]
                f.write(str(cons.amb.formatData.trainFormatted[i][2])+ '\t') #Write InstanceID
                for att in trackList:
                    f.write(str(att) + '\t')
                f.write(str(cons.amb.formatData.trainFormatted[i][1]) +'\n') #Write phenotype
    
            f.close()


    def writePredictions(self, exploreIter, outFile, predictionList, realList, predictionSets):
        if cons.outputTestPredictions:
            """ Prints out the Testing Predictions to txt file."""
            try:  
                f = open(outFile + '_'+ str(exploreIter + 1)+'_Predictions.txt','w') # Outputs tab delimited text file of rule population and respective rule stats
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open', outFile + '_'+ str(exploreIter + 1)+'_Predictions.txt')
                raise 
            else:
                print("Writing Predictions to File...")

            f.write(str(cons.labelInstanceID) + '\t'+'Endpoint Predictions'+'\t' + 'True Endpoint')
            if cons.env.formatData.discretePhenotype:
                for eachClass in cons.amb.formatData.phenotypeList:
                    f.write('\t'+ str(eachClass))
            f.write('\n')
            
            for i in range(len(predictionList)):
                f.write(str(cons.amb.formatData.testFormatted[i][2])+ '\t') #Write InstanceID
                f.write(str(predictionList[i])+'\t'+str(realList[i]))
                if cons.env.formatData.discretePhenotype:
                    propList = []
                    for eachClass in cons.amb.formatData.phenotypeList:
                        propList.append(predictionSets[i][eachClass])
                    for each in propList:
                        f.write('\t'+ str(each))
                f.write('\n')
            f.close()
            
    def editPopStats(self, testEval):
        """ Takes an existing popStatsFile and edits it to report Testing Accuracy performance, and Testing coverage on a specified testing dataset. """
        try:
            fileObject = open(cons.popRebootPath+"_PopStats.txt", 'rU')  # opens each datafile to read.
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', cons.popRebootPath+"_PopStats.txt")
            raise 
        #Grab the existing file information (only a couple items will change, i.e. testing acccuracy and testing coverage)
        fileStorage = []
        for each in fileObject:
            fileStorage.append(each)
            
        fileObject.close()
  
        
        try:  
            popStatsOut = open(cons.popRebootPath+'_PopStats_Testing.txt','w') # Outputs Population run stats
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', cons.popRebootPath+'_PopStats_Testing.txt')
            raise 
        else:
            print("Writing Population Statistical Summary File...")
        
        for i in range(2):
            popStatsOut.write(fileStorage[i])
        
        tempList = fileStorage[2].strip().split('\t')
        popStatsOut.write(str(tempList[0])+"\t")
        popStatsOut.write(str(testEval[0])+"\t")
        popStatsOut.write(str(tempList[2]) +"\t")
        popStatsOut.write(str(testEval[1])+"\n\n") 
        
        for i in range(4,36):
            popStatsOut.write(fileStorage[i])
      
        popStatsOut.close()
  