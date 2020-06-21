# TANGENTE PENITENTE
# Prediccion.py

"""
Basándose en un determinado conjunto de coincidencias, este módulo utiliza un esquema de votación para seleccionar la predicción del fenotipo para 
Tangente Penitente.
"""

from Constantes import *
import random

class Prediccion:
    def __init__(self, poblacion):
        """ Construye la matriz de votos y determina la decision de
        la prediccion
        """

        self.decision = None

        # ---------------------------------------------------------
        # FENOTIPO DISCRETO
        # ---------------------------------------------------------
        if cons.amb.datosFormateados.fenotipoDisreto:
            self.voto = {}
            self.empate_Numerosidad = {}
            self.empate_EstampaTiempo = {}

            for cadaClase in cons.amb.datosFormateados.listaFenotipos:
                self.voto[cadaClase] = 0.0
                self.empate_Numerosidad[cadaClase] = 0.0
                self.empate_EstampaTiempo[cadaClase] = 0.0

            for ref in poblacion.conjuntoCoincidencias:
                cl = poblacion.conjuntoPoblacion[ref]
                self.voto[cl.fenotipo] += cl.aptitud * cl.numerosidad * cons.amb.datosFormateados.pesosPrediccionClases[cl.fenotipo]
                self.empate_Numerosidad[cl.fenotipo] += cl.numerosidad
                self.empate_EstampaTiempo[cl.fenotipo] += cl.estampaTiempoInic

            valorAlto = 0.0
            mejorClase = []

            for estaClase in cons.amb.datosFormateados.listaFenotipos:
                if self.voto[estaClase] == valorAlto:
                    mejorClase.append(estaClase)

            if valorAlto == 0.0:
                self.decision = None

            elif len(mejorClase) > 1:
                mejorNum = 0
                nuevaMejorClse = []

                for estaClase in mejorClase:
                    if self.empate_Numerosidad[estaClase] >= mejorNum:
                        mejorNum = self.empate_Numerosidad[estaClase]

                for estaClase in mejorClase:
                    if self.empate_Numerosidad[estaClase] == mejorNum:
                        nuevaMejorClse.append(estaClase)

                # ------------------------------------------------------

                if len(nuevaMejorClse) > 1:
                    mejorEstampa = 0
                    nuevaNuevaMejorClase = []

                    for estaClase in nuevaMejorClse:
                        if self.empate_EstampaTiempo[estaClase] >= mejorEstampa:
                            mejorEstampa = self.empate_EstampaTiempo[estaClase]

                    for estaClase in nuevaMejorClse:
                        if self.empate_EstampaTiempo[estaClase] == mejorEstampa:
                            nuevaNuevaMejorClase.append(estaClase)

                    # ----------------------------------------------------
                    if len(nuevaNuevaMejorClase) > 1:
                        self.decision = 'Empate'
                
                else:
                    self.decision = nuevaMejorClse[0]

            # ---------------------------------------------------------
            # FENOTIPO CONTINUO
            # ---------------------------------------------------------

            else:
                print("Prediccion - Error: Tangente Penitente no puede manejar endpoints continuos.")

    def obtenerSumaAptitud(self, poblacion, bajo, alto):
        """Obtiene la suma de aptitud de reglas en el conjunto de
        reglas. Para prediccion de fenotipo continuo. """

        sumaApt = 0

        for ref in poblacion.conjuntoCoincidencias:
            cl = poblacion.conjuntoPoblacion[ref]

            if cl.fenotipo[0] <= bajo and cl.fenotipo[1] >= alto:
                sumaApt += cl.aptitud

        return sumaApt

    def obtenerDecision(self):
        pass

    def obtenerConjunto(self):
        pass