"""
TANGENTE PENITENTE
Nombre: tp_PresicionClases.py
Descripcion: Se utiliza para evaluaciones globales de la población de reglas 
             de LCS para dominios problemáticos con un fenotipo discreto.  
             Permite el cálculo de una precisión equilibrada cuando un fenotipo 
             discreto incluye dos o más clases posibles.
"""

class PresicionClases:
    def __init__(self):
        """ Initialize the accuracy calculation for a single class """
        self.T_myClass = 0      #true positive for binary class problems
        self.T_otherClass = 0   #true negative for binary class problems
        self.F_myClass = 0      #false positive for binary class problems
        self.F_otherClass = 0   #false negative for binary class problems


    def updateAccuracy(self, thisIsMe, accurateClass):
        """ Increment the appropriate cell of the confusion matrix """
        if thisIsMe and accurateClass:
            self.T_myClass += 1
        elif accurateClass:
            self.T_otherClass += 1
        elif thisIsMe:
            self.F_myClass += 1
        else:
            self.F_otherClass += 1
        
        
    def reportClassAccuracy(self):
        """ Print to standard out, summary on the class accuracy. """
        print("-----------------------------------------------")
        print("TP = "+str(self.T_myClass))
        print("TN = "+str(self.T_otherClass))
        print("FP = "+str(self.F_myClass))
        print("FN = "+str(self.F_otherClass))
        print("-----------------------------------------------")