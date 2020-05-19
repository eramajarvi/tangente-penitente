"""
TANGENTE PENITENTE
Nombre: tp_Cronometro.py
Descripcion: La función de este módulo es en gran medida para fines 
             de desarrollo y evaluación. Específicamente rastrea no 
             sólo el tiempo de ejecución global de Tangente Penitente, 
             sino que también rastrea el tiempo utilizado por los diferentes 
             mecanismos clave del algoritmo. Este seguimiento probablemente
             desperdicia un poco de tiempo de ejecución, así que para un rendimiento 
             óptimo comprueba que todos los comandos 'cons.cronometro.iniciarXXXX', 
             y 'cons.cronometro.detenerXXXX' están comentados dentro de TangentePenitente_Main, 
             tp_Algoritmo, y tp_ConjuntoClasificadores.
"""

# Importar modulos requeridos
from exstracs_constants import *
import time
#

class Timer:
    def __init__(self):
        """ Initializes all Timer values for the algorithm """        
        # Global Time objects
        self.globalStartRef = time.time()
        self.globalTime = 0.0
        self.addedTime = 0.0
        
        # Match Time Variables
        self.startRefMatching = 0.0
        self.globalMatching = 0.0

        # Covering Time Variables
        self.startRefCovering = 0.0
        self.globalCovering = 0.0
        
        # Deletion Time Variables
        self.startRefDeletion = 0.0
        self.globalDeletion = 0.0

        # Subsumption Time Variables
        self.startRefSubsumption = 0.0
        self.globalSubsumption = 0.0

        # Selection Time Variables
        self.startRefSelection = 0.0
        self.globalSelection = 0.0
        
        # Crossover Time Variables
        self.startRefCrossover = 0.0
        self.globalCrossover = 0.0
        
        # Mutation Time Variables
        self.startRefMutation = 0.0
        self.globalMutation = 0.0
        
        # Attribute Tracking and Feedback
        self.startRefAT = 0.0
        self.globalAT = 0.0

        # Expert Knowledge (EK)
        self.startRefEK = 0.0
        self.globalEK = 0.0

        # OutFile
        self.startRefOutFile = 0.0
        self.globalOutFile = 0.0

        # Initialization
        self.startRefInit = 0.0
        self.globalInit = 0.0
        
        # Add Classifier
        self.startRefAdd = 0.0
        self.globalAdd = 0.0
        
        # Evaluation Time Variables
        self.startRefEvaluation = 0.0
        self.globalEvaluation = 0.0  
        
        # Rule Compaction
        self.startRefRuleCmp = 0.0
        self.globalRuleCmp = 0.0

        # Rule Compaction
        self.startRefTEST = 0.0
        self.globalTEST = 0.0
        
        #Debug Counter
        self.globalTESTCounter = 0
        
    # ************************************************************
    def startTimeMatching(self):
        """ Tracks MatchSet Time """
        self.startRefMatching = time.time()
         
    def stopTimeMatching(self):
        """ Tracks MatchSet Time """
        diff = time.time() - self.startRefMatching
        self.globalMatching += diff        

    # ************************************************************
    def startTimeCovering(self):
        """ Tracks MatchSet Time """
        self.startRefCovering = time.time()
         
    def stopTimeCovering(self):
        """ Tracks MatchSet Time """
        diff = time.time() - self.startRefCovering
        self.globalCovering += diff        
        
    # ************************************************************
    def startTimeDeletion(self):
        """ Tracks Deletion Time """
        self.startRefDeletion = time.time()
        
    def stopTimeDeletion(self):
        """ Tracks Deletion Time """
        diff = time.time() - self.startRefDeletion
        self.globalDeletion += diff
    
    # ************************************************************
    def startTimeCrossover(self):
        """ Tracks Crossover Time """
        self.startRefCrossover = time.time() 
               
    def stopTimeCrossover(self):
        """ Tracks Crossover Time """
        diff = time.time() - self.startRefCrossover
        self.globalCrossover += diff
        
    # ************************************************************
    def startTimeMutation(self):
        """ Tracks Mutation Time """
        self.startRefMutation = time.time()
        
    def stopTimeMutation(self):
        """ Tracks Mutation Time """
        diff = time.time() - self.startRefMutation
        self.globalMutation += diff
        
    # ************************************************************
    def startTimeSubsumption(self):
        """Tracks Subsumption Time """
        self.startRefSubsumption = time.time()

    def stopTimeSubsumption(self):
        """Tracks Subsumption Time """
        diff = time.time() - self.startRefSubsumption
        self.globalSubsumption += diff    
        
    # ************************************************************
    def startTimeSelection(self):
        """ Tracks Selection Time """
        self.startRefSelection = time.time()
        
    def stopTimeSelection(self):
        """ Tracks Selection Time """
        diff = time.time() - self.startRefSelection
        self.globalSelection += diff
    
    # ************************************************************
    def startTimeEvaluation(self):
        """ Tracks Evaluation Time """
        self.startRefEvaluation = time.time()
        
    def stopTimeEvaluation(self):
        """ Tracks Evaluation Time """
        diff = time.time() - self.startRefEvaluation
        self.globalEvaluation += diff 
    
    # ************************************************************
    def startTimeRuleCmp(self):
        """  """
        self.startRefRuleCmp = time.time()   
         
    def stopTimeRuleCmp(self):
        """  """
        diff = time.time() - self.startRefRuleCmp
        self.globalRuleCmp += diff
        
    # ***********************************************************  
    def startTimeAT(self):
        """  """
        self.startRefAT = time.time()   
         
    def stopTimeAT(self):
        """  """
        diff = time.time() - self.startRefAT
        self.globalAT += diff
        
    # ***********************************************************
    def startTimeEK(self):
        """  """
        self.startRefEK = time.time()   
         
    def stopTimeEK(self):
        """  """
        diff = time.time() - self.startRefEK
        self.globalEK += diff
        
    # ***********************************************************
    def startTimeOutFile(self):
        """  """
        self.startRefOutFile = time.time()   
         
    def stopTimeOutFile(self):
        """  """
        diff = time.time() - self.startRefOutFile
        self.globalOutFile += diff
        
    # ***********************************************************
    def startTimeInit(self):
        """  """
        self.startRefInit = time.time()   
         
    def stopTimeInit(self):
        """  """
        diff = time.time() - self.startRefInit
        self.globalInit += diff
        
    # ***********************************************************
    def startTimeAdd(self):
        """  """
        self.startRefAdd = time.time()   
         
    def stopTimeAdd(self):
        """  """
        diff = time.time() - self.startRefAdd
        self.globalAdd += diff
        
    # ***********************************************************
    def startTimeTEST(self):
        """  """
        self.startRefTEST = time.time()   
         
    def stopTimeTEST(self):
        """  """
        diff = time.time() - self.startRefTEST
        self.globalTEST += diff
    # ***********************************************************
    
    def returnGlobalTimer(self):
        """ Set the global end timer, call at very end of algorithm. """
        self.globalTime = (time.time() - self.globalStartRef) + self.addedTime #Reports time in minutes, addedTime is for population reboot.
        return self.globalTime/ 60.0
        
        
    def TESTCounter(self):
        """ Set the global end timer, call at very end of algorithm. """
        self.globalTESTCounter += 1

    
    def setTimerRestart(self, remakeFile): 
        """ Sets all time values to the those previously evolved in the loaded popFile.  """
        print(remakeFile+"_PopStats.txt")
        try:
            fileObject = open(remakeFile+"_PopStats.txt", 'rU')  # opens each datafile to read.
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', remakeFile+"_PopStats.txt")
            raise 

        timeDataRef = 22
        tempLine = None
        for i in range(timeDataRef):
            tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t')
        self.addedTime = float(tempList[1]) * 60 #previous global time added with Reboot.
        
        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalMatching = float(tempList[1]) * 60

        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalCovering = float(tempList[1]) * 60
        
        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalDeletion = float(tempList[1]) * 60

        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalSubsumption = float(tempList[1]) * 60
        
        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalSelection = float(tempList[1]) * 60    
 
        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalCrossover = float(tempList[1]) * 60

        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalMutation = float(tempList[1]) * 60

        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalAT = float(tempList[1]) * 60
 
        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalEK = float(tempList[1]) * 60

        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalOutFile = float(tempList[1]) * 60

        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalInit = float(tempList[1]) * 60
        
        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalAdd = float(tempList[1]) * 60
        
        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalEvaluation = float(tempList[1]) * 60
                     
        tempLine = fileObject.readline()
        tempList = tempLine.strip().split('\t') 
        self.globalRuleCmp = float(tempList[1]) * 60
        
        fileObject.close()
        

    def reportTimes(self):
        self.returnGlobalTimer()
        """ Reports the time summaries for this run. Returns a string ready to be printed out."""
        outputTime = "Global Time\t"+str(self.globalTime/ 60.0)+ \
        "\nMatching Time\t" + str(self.globalMatching/ 60.0)+ \
        "\nCovering Time\t" + str(self.globalCovering/ 60.0)+ \
        "\nDeletion Time\t" + str(self.globalDeletion/ 60.0)+ \
        "\nSubsumption Time\t" + str(self.globalSubsumption/ 60.0)+ \
        "\nSelection Time\t"+str(self.globalSelection/ 60.0)+ \
        "\nCrossover Time\t" + str(self.globalCrossover/ 60.0)+ \
        "\nMutation Time\t" + str(self.globalMutation/ 60.0)+ \
        "\nAttribute Tracking-Feedback Time\t"+str(self.globalAT/ 60.0) + \
        "\nExpert Knowledge Time\t"+str(self.globalEK/ 60.0) + \
        "\nOutput File Time\t"+str(self.globalOutFile/ 60.0) + \
        "\nInitialization Time\t"+str(self.globalInit/ 60.0) + \
        "\nAdd Classifier Time\t"+str(self.globalAdd/ 60.0) + \
        "\nEvaluation Time\t"+str(self.globalEvaluation/ 60.0) + \
        "\nRule Compaction Time\t"+str(self.globalRuleCmp/ 60.0) + "\n" 
        
        return outputTime