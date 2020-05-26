"""
Nombre: tp_CR.py
Descripcion: Incluye varias estrategias de compactación de reglas/filtros 
             de reglas, que pueden seleccionarse como una etapa de posprocesamiento 
             después del aprendizaje de la población del clasificador Tangente Penitente. 
             Las estrategias Fu1, Fu2 y CRA2 fueron previamente propuestas/publicadas 
             por otros autores.  QRC, PDRC y QRF fueron propuestas y publicadas por Jie Tan, 
             Jason Moore y Ryan Urbanowicz en "Rapid Rule Compaction Strategies for Global 
             Knowledge Discovery in a Supervised Learning Classifier System". [2013].
"""

#Import Required Modules-------------------------------
from tp_Constantes import *
from tp_PresicionClases import PresicionClases
from tp_Prediccion import *
from tp_ConjuntoClasificadores import ConjuntoClasificadores
import copy
import math
#------------------------------------------------------

class CompactacionReglas:
    def __init__(self, pop, originalTrainAcc, originalTestAcc):
        """ Initialize and run the specified rule compaction strategy. """
        print("---------------------------------------------------------------------------------------------------------")
        print("Starting Rule Compaction Algorithm ("+str(cons.ruleCompactionMethod)+") ...")
        self.pop = pop
        self.originalTrainAcc = originalTrainAcc
        self.originalTestAcc = originalTestAcc
        
        #Outside Rule Compaction Strategies------------------------------------------------------------------------------------
        if cons.ruleCompactionMethod == 'Fu1': #(Implemented by Jie Tan, Referred to as 'A12' in original code.)
            self.Approach_Fu1()  
        elif cons.ruleCompactionMethod =='Fu2': #(Implemented by Jie Tan, Referred to as 'A13' in original code.)
            self.Approach_Fu2()  
        elif cons.ruleCompactionMethod =='CRA2': #(Implemented by Jie Tan, Referred to as 'A8' or 'Dixon' in original code.)
            self.Approach_CRA2() 
        #------------------------------------------------------------------------------------------------------------------------
        #ExSTraCS Original Rule Compaction Strategies:--------------------------------------------------------------------------------
        elif cons.ruleCompactionMethod =='QRC': #Quick Rule Compaction (Developed by Jie Tan, Referred to as 'A9' or 'UCRA' in original code.)
            self.Approach_QRC() 
        elif cons.ruleCompactionMethod =='PDRC': #Parameter Driven Rule Compaction - (Developed by Jie Tan, Referred to as 'A17' or 'QCRA' in original code.)
            self.Approach_PDRC()  
        elif cons.ruleCompactionMethod == 'QRF': #Quick Rule Filter - (Developed by Ryan Urbanowicz, Referred to as 'Quick Rule Cleanup' or 'QRC' in original code.) 
            self.Approach_QRF()
        else:
            print("RuleCompaction: Error - specified rule compaction strategy not found.")
        
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # COMPACTION STRATEGIES
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def Approach_Fu1(self):
        """ This approach completely follows Fu's first approach. In the third stage, the number of instances a rule matched is used to rank 
        the rules and guide covering. Ranking list is updated each time some instances are covered and removed from the training set. """
        
        #Order Classifier Set---------------------------------------------------------------------------------------------------------
        lastGood_popSet = sorted(self.pop.popSet, key = self.numerositySort)
        self.pop.popSet = lastGood_popSet[:]
        print("Starting number of classifiers = " + str(len(self.pop.popSet))) 
        print("Original Training Accuracy = " +str(self.originalTrainAcc))
        print("Original Testing Accuracy = " +str(self.originalTestAcc))
        
        #STAGE 1----------------------------------------------------------------------------------------------------------------------
        keepGoing = True
        while keepGoing:
            del self.pop.popSet[0] #Remove next classifier
            newAccuracy = self.performanceEvaluation(True) #Perform classifier set training accuracy evaluation

            if newAccuracy < self.originalTrainAcc:
                keepGoing = False
                self.pop.popSet = lastGood_popSet[:]
            else:
                lastGood_popSet = self.pop.popSet[:]
            if len(self.pop.popSet) == 0:
                keepGoing = False
        print("STAGE 1 Ended: Classifiers Remaining = " +str(len(self.pop.popSet))) 
        
        #STAGE 2----------------------------------------------------------------------------------------------------------------------
        retainedClassifiers = []
        RefAccuracy = self.originalTrainAcc
        for i in range(len(self.pop.popSet)): 
            heldClassifier = self.pop.popSet[0]
            del self.pop.popSet[0]
            newAccuracy = self.performanceEvaluation(True) #Perform classifier set training accuracy evaluation

            if newAccuracy < RefAccuracy:
                retainedClassifiers.append(heldClassifier)
                RefAccuracy = newAccuracy

        self.pop.popSet = retainedClassifiers
        print("STAGE 2 Ended: Classifiers Remaining = " +str(len(self.pop.popSet))) 
        
        #STAGE 3----------------------------------------------------------------------------------------------------------------------
        finalClassifiers = []
        completelyGeneralRuleRef = None
        if len(self.pop.popSet) == 0: #Stop Check
            keepGoing = False
        else:
            keepGoing = True

        #Make the match count list in preparation for state 3------------------------------------------------------------------------- 
        matchCountList = [0.0 for v in range(len(self.pop.popSet))] 
        cons.amb.startEvaluationMode()
        for i in range(len(self.pop.popSet)): #For the population of classifiers
            cons.amb.resetDataRef(True)
            for j in range(cons.amb.formatData.numTrainInstances): #For each instance in training data
                cl = self.pop.popSet[i]
                state = cons.amb.getTrainInstance()[0]
                doesMatch = cl.match(state)
                if doesMatch:
                    matchCountList[i] += 1
                cons.amb.newInstance(True)
            if len(self.pop.popSet[i].condition) == 0:
                completelyGeneralRuleRef = i
      
        cons.amb.stopEvaluationMode()
        if completelyGeneralRuleRef != None: #gets rid of completely general rule.
            del matchCountList[completelyGeneralRuleRef]
            del self.pop.popSet[completelyGeneralRuleRef]

        #----------------------------------------------------------------------------------------------------------------------------
        tempEnv = copy.deepcopy(cons.amb)
        trainingData = tempEnv.formatData.trainFormatted 
        while len(trainingData) > 0 and keepGoing: 
            bestRef = None
            bestValue = None
            for i in range(len(matchCountList)):
                if bestValue == None or bestValue < matchCountList[i]:
                    bestRef = i
                    bestValue = matchCountList[i]
                    
            if bestValue == 0.0 or len(self.pop.popSet) < 1:
                keepGoing = False
                continue

            #Update Training Data----------------------------------------------------------------------------------------------------
            matchedData = 0
            w = 0
            cl = self.pop.popSet[bestRef]
            for i in range(len(trainingData)):
                state = trainingData[w][0]
                doesMatch = cl.match(state)
                if doesMatch:
                    matchedData += 1
                    del trainingData[w]
                else:
                    w += 1
            if matchedData > 0:
                finalClassifiers.append(self.pop.popSet[bestRef]) #Add best classifier to final list - only do this if there are any remaining matching data instances for this rule!
            
            #Update classifier list
            del self.pop.popSet[bestRef]

            #re-calculate match count list
            matchCountList = [0.0 for v in range(len(self.pop.popSet))]
            for i in range(len(self.pop.popSet)):
                dataRef = 0 
                for j in range(len(trainingData)): #For each instance in training data
                    cl = self.pop.popSet[i]
                    state = trainingData[dataRef][0]
                    doesMatch = cl.match(state)
                    if doesMatch:
                        matchCountList[i] += 1
                    dataRef +=1
                
            if len(self.pop.popSet) == 0:
                keepGoing = False
           
        self.pop.popSet = finalClassifiers 
        print("STAGE 3 Ended: Classifiers Remaining = " +str(len(self.pop.popSet))) 
        
        
    ############################################################################################################################################################################################
    def Approach_Fu2(self):
        """ This approach completely follows Fu's second approach. All three stages use accuracy to sort rules."""
        #Order Classifier Set---------------------------------------------------------------------------------------------------------
        lastGood_popSet = sorted(self.pop.popSet, key = self.numerositySort)
        self.pop.popSet = lastGood_popSet[:]
        print("Starting number of classifiers = " + str(len(self.pop.popSet))) 
        print("Original Training Accuracy = " +str(self.originalTrainAcc))
        print("Original Testing Accuracy = " +str(self.originalTestAcc))
        
        #STAGE 1----------------------------------------------------------------------------------------------------------------------
        keepGoing = True
        while keepGoing:
            del self.pop.popSet[0] #Remove next classifier
            newAccuracy = self.performanceEvaluation(True) #Perform classifier set training accuracy evaluation
            if newAccuracy < self.originalTrainAcc:
                keepGoing = False
                self.pop.popSet = lastGood_popSet[:]
            else:
                lastGood_popSet = self.pop.popSet[:]
            if len(self.pop.popSet) == 0:
                keepGoing = False
        print("STAGE 1 Ended: Classifiers Remaining = " +str(len(self.pop.popSet))) 
        
        #STAGE 2----------------------------------------------------------------------------------------------------------------------
        retainedClassifiers = []
        RefAccuracy = self.originalTrainAcc
        for i in range(len(self.pop.popSet)): 
            heldClassifier = self.pop.popSet[0]
            del self.pop.popSet[0]
            newAccuracy = self.performanceEvaluation(True) #Perform classifier set training accuracy evaluation
            
            if newAccuracy < RefAccuracy:
                retainedClassifiers.append(heldClassifier)
                RefAccuracy = newAccuracy
                
        self.pop.popSet = retainedClassifiers
        print("STAGE 2 Ended: Classifiers Remaining = " +str(len(self.pop.popSet))) 
        
        #STAGE 3----------------------------------------------------------------------------------------------------------------------
        Sort_popSet = sorted(self.pop.popSet, key = self.numerositySort, reverse = True)
        self.pop.popSet = Sort_popSet[:]
        RefAccuracy = self.performanceEvaluation(True)
        
        if len(self.pop.popSet) == 0: #Stop check
            keepGoing = False
        else:
            keepGoing = True
        
        for i in range(len(self.pop.popSet)): 
            heldClassifier = self.pop.popSet[0]
            del self.pop.popSet[0]
            newAccuracy = self.performanceEvaluation(True) #Perform classifier set training accuracy evaluation
            
            if newAccuracy < RefAccuracy:
                self.pop.popSet.append(heldClassifier)
            else:
                RefAccuracy = newAccuracy

        print("STAGE 3 Ended: Classifiers Remaining = " +str(len(self.pop.popSet))) 


    ############################################################################################################################################################################################
    def Approach_CRA2(self):
        """ This approach is based on Dixon's and Shoeleh's method. For each instance, form a match set and then a correct set. The most useful rule in 
            the correct set is moved into the final ruleset. In this approach, the most useful rule has the largest product of accuracy
            and generality."""    
    
        print("Starting number of classifiers = " + str(len(self.pop.popSet))) 
        print("Original Training Accuracy = " +str(self.originalTrainAcc))
        print("Original Testing Accuracy = " +str(self.originalTestAcc))
        
        retainedClassifiers = []
        self.matchSet = [] 
        self.correctSet = []
        
        cons.amb.startEvaluationMode()
        cons.amb.resetDataRef(True)     
        for j in range(cons.amb.formatData.numTrainInstances):
            state_phenotype = cons.amb.getTrainInstance()
            state = state_phenotype[0]
            phenotype = state_phenotype[1]
            
            #Create MatchSet
            for i in range(len(self.pop.popSet)):
                cl = self.pop.popSet[i]                                 
                if cl.match(state):                                
                    self.matchSet.append(i)
                    
            #Create CorrectSet
            if cons.env.formatData.discretePhenotype:
                for i in range(len(self.matchSet)):
                    ref = self.matchSet[i]
                    if self.pop.popSet[ref].phenotype == phenotype:
                        self.correctSet.append(ref)
            else:
                for i in range(len(self.matchSet)):
                    ref = self.matchSet[i]
                    if float(phenotype) <= float(self.pop.popSet[ref].phenotype[1]) and float(phenotype) >= float(self.pop.popSet[ref].phenotype[0]):
                        self.correctSet.append(ref)
        
            #Find the rule with highest accuracy, generality product
            highestValue = 0
            highestRef = 0
            for i in range(len(self.correctSet)):
                ref = self.correctSet[i]
                product = self.pop.popSet[ref].accuracy * (cons.amb.formatData.numAttributes - len(self.pop.popSet[ref].condition)) / float(cons.amb.formatData.numAttributes)
                if product > highestValue:
                    highestValue = product
                    highestRef = ref
            
            #If the rule is not already in the final ruleset, move it to the final ruleset
            if highestValue == 0 or self.pop.popSet[highestRef] in retainedClassifiers:
                pass
            else:
                retainedClassifiers.append(self.pop.popSet[highestRef])

            #Move to the next instance                
            cons.amb.newInstance(True)
            self.matchSet = [] 
            self.correctSet = []
        cons.amb.stopEvaluationMode()
        
        self.pop.popSet = retainedClassifiers
        print("STAGE 1 Ended: Classifiers Remaining = " +str(len(self.pop.popSet))) 
    
    
    ############################################################################################################################################################################################  
    def Approach_QRC(self):
        """Called QCRA in the paper. It uses fitness to rank rules and guide covering. It's the same as Approach 15, but the code is re-written in 
        order to speed up."""
        
        print("Starting number of classifiers = " + str(len(self.pop.popSet))) 
        print("Original Training Accuracy = " +str(self.originalTrainAcc))
        print("Original Testing Accuracy = " +str(self.originalTestAcc))
        
        #STAGE 1----------------------------------------------------------------------------------------------------------------------
        finalClassifiers = []
        if len(self.pop.popSet) == 0: #Stop check
            keepGoing = False
        else:
            keepGoing = True

        lastGood_popSet = sorted(self.pop.popSet, key = self.accuracySort, reverse = True)
        self.pop.popSet = lastGood_popSet[:]
        
        tempEnv = copy.deepcopy(cons.amb)
        trainingData = tempEnv.formatData.trainFormatted
        
        while len(trainingData) > 0 and keepGoing: 
            newTrainSet = []
            matchedData = 0
            for w in range(len(trainingData)):
                cl = self.pop.popSet[0]
                state = trainingData[w][0]
                doesMatch = cl.match(state)
                if doesMatch:
                    matchedData += 1
                else:
                    newTrainSet.append(trainingData[w])
            if matchedData > 0:
                finalClassifiers.append(self.pop.popSet[0]) #Add best classifier to final list - only do this if there are any remaining matching data instances for this rule!
            #Update classifier list and training set list
            trainingData = newTrainSet
            del self.pop.popSet[0]
            if len(self.pop.popSet) == 0:
                keepGoing = False
           
        self.pop.popSet = finalClassifiers 
        print("STAGE 1 Ended: Classifiers Remaining = " +str(len(self.pop.popSet))) 


    ############################################################################################################################################################################################
    def Approach_PDRC(self):
        """ This approach is based on Dixon's approach, called UCRA in the paper. For each instance, form a match set and then a correct set. 
        The most useful rule in the correct set is moved into the final ruleset. In this approach, the most useful rule has the largest 
        product of accuracy, numerosity and generality.""" 
        
        print("Starting number of classifiers = " + str(len(self.pop.popSet))) 
        print("Original Training Accuracy = " +str(self.originalTrainAcc))
        print("Original Testing Accuracy = " +str(self.originalTestAcc))
        
        
        retainedClassifiers = []
        self.matchSet = [] 
        self.correctSet = []
        
        cons.amb.startEvaluationMode()
        cons.amb.resetDataRef(True)     
        for j in range(cons.amb.formatData.numTrainInstances):
            state_phenotype = cons.amb.getTrainInstance()
            state = state_phenotype[0]
            phenotype = state_phenotype[1]
            
            #Create MatchSet
            for i in range(len(self.pop.popSet)):
                cl = self.pop.popSet[i]                                 
                if cl.match(state):                                
                    self.matchSet.append(i)
                    
            #Create CorrectSet
            if cons.env.formatData.discretePhenotype:
                for i in range(len(self.matchSet)):
                    ref = self.matchSet[i]
                    if self.pop.popSet[ref].phenotype == phenotype:
                        self.correctSet.append(ref)
            else:
                for i in range(len(self.matchSet)):
                    ref = self.matchSet[i]
                    if float(phenotype) <= float(self.pop.popSet[ref].phenotype[1]) and float(phenotype) >= float(self.pop.popSet[ref].phenotype[0]):
                        self.correctSet.append(ref)
            #Find the rule with highest accuracy, generality and numerosity product
            highestValue = 0
            highestRef = 0
            for i in range(len(self.correctSet)):
                ref = self.correctSet[i]
                product = self.pop.popSet[ref].accuracy * (cons.amb.formatData.numAttributes - len(self.pop.popSet[ref].condition)) / float(cons.amb.formatData.numAttributes) * self.pop.popSet[ref].numerosity
                if product > highestValue:
                    highestValue = product
                    highestRef = ref
        
            #If the rule is not already in the final ruleset, move it to the final ruleset
            if highestValue == 0 or self.pop.popSet[highestRef] in retainedClassifiers:
                pass
            else:
                retainedClassifiers.append(self.pop.popSet[highestRef])

            #Move to the next instance                
            cons.amb.newInstance(True)
            self.matchSet = [] 
            self.correctSet = []
        cons.amb.stopEvaluationMode()
        
        self.pop.popSet = retainedClassifiers
        print("STAGE 1 Ended: Classifiers Remaining = " +str(len(self.pop.popSet))) 
        
 
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # FILTER STRATEGIES
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def Approach_QRF(self):
        """ An extremely fast rule compaction strategy. Removes any rule with an accuracy below 50% and any rule that covers only one instance, but specifies more than one attribute
         (won't get rid of rare variant rules)"""
        
        print("Starting number of classifiers = " + str(len(self.pop.popSet))) 
        print("Original Training Accuracy = " +str(self.originalTrainAcc))
        print("Original Testing Accuracy = " +str(self.originalTestAcc))
        
        #STAGE 1----------------------------------------------------------------------------------------------------------------------
        retainedClassifiers = []
        for i in range(len(self.pop.popSet)): 
            if self.pop.popSet[i].accuracy <= 0.5 or (self.pop.popSet[i].correctCover == 1 and len(self.pop.popSet[i].specifiedAttList) > 1):
                pass
            else:
                retainedClassifiers.append(self.pop.popSet[i])
        self.pop.popSet = retainedClassifiers
        print("STAGE 1 Ended: Classifiers Remaining = " +str(len(self.pop.popSet))) 


    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # EVALUTATION METHODS
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def performanceEvaluation(self, isTrain):
        """ Performs Training or Testing Evaluation"""
        if cons.env.formatData.discretePhenotype:
            adjustedBalancedAccuracy = self.doPopEvaluation(isTrain)
        else: #Continuous Phenotype
            print("RuleCompaction - Error: ExSTraCS 2.0 can not handle continuous endpoints.")
            
        return adjustedBalancedAccuracy
    
    
    def doPopEvaluation(self, isTrain):
        """ Performs evaluation of population via the copied environment.  The population is maintained unchanging throughout the evaluation.
        Works on both training and testing data. """
        cons.amb.startEvaluationMode()
        noMatch = 0 #How often does the population fail to have a classifier that matches an instance in the data.
        tie = 0 #How often can the algorithm not make a decision between classes due to a tie.
        cons.amb.resetDataRef(isTrain) #Go to first instance in data set
        phenotypeList = cons.amb.formatData.phenotypeList #shorter reference to phenotypeList - based on training data (assumes no as yet unseen phenotypes in testing data)
        #----------------------------------------------
        classAccDict = {}
        for each in phenotypeList:
            classAccDict[each] = ClassAccuracy()

        #----------------------------------------------
        if isTrain:
            instances = cons.amb.formatData.numTrainInstances
        else:
            instances = cons.amb.formatData.numTestInstances
        #----------------------------------------------------------------------------------------------
        for inst in range(instances):
            if isTrain:
                state_phenotype = cons.amb.getTrainInstance()
            else:
                state_phenotype = cons.amb.getTestInstance()
            #-----------------------------------------------------------------------------
            self.population.makeEvalMatchSet(state_phenotype[0])
            prediction = Prediction(self.population)
            phenotypeSelection = prediction.getDecision() 
            #-----------------------------------------------------------------------------
            
            if phenotypeSelection == None: 
                noMatch += 1
            elif phenotypeSelection == 'Tie':
                tie += 1
            else: #Instances which failed to be covered are excluded from the initial accuracy calculation (this is important to the rule compaction algorithm)
                for each in phenotypeList:
                    thisIsMe = False
                    accuratePhenotype = False
                    truePhenotype = state_phenotype[1]
                    if each == truePhenotype:
                        thisIsMe = True #Is the current phenotype the true data phenotype.
                    if phenotypeSelection == truePhenotype:
                        accuratePhenotype = True
                    classAccDict[each].updateAccuracy(thisIsMe, accuratePhenotype)
                        
            cons.amb.newInstance(isTrain) #next instance
            self.population.clearSets() 

        #Calculate Balanced Accuracy---------------------------------------------
        balancedAccuracy = 0
        for each in phenotypeList: 
            try:
                sensitivity = classAccDict[each].T_myClass / (float(classAccDict[each].T_myClass + classAccDict[each].F_otherClass))
            except:
                sensitivity = 0.0
            try:
                specificity = classAccDict[each].T_otherClass / (float(classAccDict[each].T_otherClass + classAccDict[each].F_myClass))
            except:
                specificity = 0.0
            
            balancedClassAccuracy = (sensitivity + specificity) / 2.0
            balancedAccuracy += balancedClassAccuracy
            
        balancedAccuracy = balancedAccuracy / float(len(phenotypeList))  

        #Adjustment for uncovered instances - to avoid positive or negative bias we incorporate the probability of guessing a phenotype by chance (e.g. 50% if two phenotypes)---------------------------------------
        predictionFail = float(noMatch)/float(instances)
        predictionTies = float(tie)/float(instances)
        predictionMade = 1.0 - (predictionFail + predictionTies)
        
        adjustedBalancedAccuracy = (balancedAccuracy * predictionMade) + ((1.0 - predictionMade) * (1.0 / float(len(phenotypeList))))
        cons.amb.stopEvaluationMode()
        return adjustedBalancedAccuracy
    
    
    def accuracySort(self, cl):
        return cl.accuracy


    def numerositySort(self, cl):
        """ Sorts from smallest numerosity to largest """
        return cl.numerosity