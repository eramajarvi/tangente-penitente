# TANGENTE PENITENTE
# PrecisionClases.py

"""
Se utiliza para evaluaciones globales de la población de reglas 
de LCS para dominios problemáticos con un fenotipo discreto. 
Permite el cálculo de una precisión equilibrada cuando un 
fenotipo discreto incluye dos o más clases posibles.
"""

class PrecisionClases:
    def __init__(self):
        """ Inicializar el calculo de la precicison para
        una sola clase """
        # Verdadero y positivo/negativo para problemas de clase binario
        self.V_miClase = 0
        self.V_otraClase = 0
        # Falso y positivo/negativo para problemas de clase binaria
        self.F_miClase = 0
        self.F_otraClase = 0

    def actualizarPrecision(self, soyYo, clasePrecisa):
        """ Incrementa la celula apropiada
        de la matriz de confusion """

        if soyYo and clasePrecisa:
            self.V_miClase += 1

        elif clasePrecisa:
            self.V_otraClase += 1

        elif soyYo:
            self.F_miClase += 1

        else:
            self.F_otraClase += 1

    def reportarPrecisionClases(self):
        """ Imprime el resumen de la precision de las clases """
        print(" ----------------------------------------------- ")
        print("VP = " + str(self.V_miClase))
        print("VN = " + str(self.V_otraClase))
        print("FP = " + str(self.F_miClase))
        print("FN = " + str(self.F_otraClase))
        print(" ----------------------------------------------- ")