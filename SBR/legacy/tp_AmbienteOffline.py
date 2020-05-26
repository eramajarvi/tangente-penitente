"""
TANGENTE PENITENTE
Nombre: tp_AmbienteOffline.py
Descripcion: En el contexto de las tareas de extracción y clasificación de datos, 
             el "entorno" de Tangente Penitente es un conjunto de datos con un número 
             limitado de instancias con cierto número de atributos y un único endpoint 
             (típicamente un fenotipo o clase discreta) de interés. Este módulo gestiona 
             el paso de Tangente Penitente por las iteraciones de aprendizaje, y las 
             instancias de datos respectivamente. Se incluyen métodos especiales para 
             pasar del aprendizaje a la evaluación de un conjunto de datos de capacitación.
"""

# Importar modulos requeridos
from tp_Datos import GestionDatos
from tp_Constantes import * 
import sys
# 

class AmbienteOffline:
    def __init__(self):

        # Inicializar variables globales
        self.refDatos = 0
        self.guardarDatosRef = 0
        self.datosFormateados = GestionDatos(cons.archivoEntrenamiento, cons.archivoPrueba)
        
        self.estadoEntrenamientoActual = self.datosFormateados.entrenamientoFormateados[self.refDatos][0]
        self.fenotipoEntrenamientoActual = self.datosFormateados.entrenamientoFormateados[self.refDatos][1]

        if cons.archivoPrueba == 'None':
            pass

        else:
            self.estadoPruebaActual = self.datosFormateados.pruebaFormateados[self.refDatos][0]
            self.fenotipoPruebaActual = self.datosFormateados.pruebaFormateados[self.refDatos][1]
        

    def obtenerInstanciaEntrenamiento(self):
        """ Devuelve la instancia actual de entrenamiento """
        return [self.instanciaEntrenamientoActual, self.fenotipoEntrenamientoActual] # Devuelve los datos de entrenamiento sin alterar
        
        
    def obtenerInstanciaPrueba(self):
        """ Returns the current training instance. """
        return [self.estadoPruebaActual, self.fenotipoPruebaActual]
    
    
    def nuevaInstancia(self, esEntrenamiento): 
        """ Cambia el ambiente a la siguiente instancia en los datos """
        #-------------------------
        # Datos de entrenamiento
        #-------------------------
        if esEntrenamiento: 
            if self.dataRef < (self.datosFormateados.numInstanciasEntrenamiento - 1):
                self.dataRef += 1
                self.estadoEntrenamientoActual = self.datosFormateados.entrenamientoFormateados[self.refDatos][0]
                self.fenotipoEntrenamientoActual = self.datosFormateados.entrenamientoFormateados[self.refDatos][1]

            else: # Una vez el aprendizaje completa una epoca (esto es, iteraciones de aprendizaje a traves de todo el conjunto de datos) empieza de nuevo con la primera instancia en los datos             
                self.resetearDataRef(esEntrenamiento)

        #------------------
        # Datos de prueba
        #------------------
        else: 
            if self.dataRef < (self.datosFormateados.numInstanciasPrueba - 1):
                self.dataRef += 1
                self.estadoPruebaActual = self.datosFormateados.pruebaFormateados[self.refDatos][0]
                self.fenotipoPruebaActual = self.datosFormateados.pruebaFormateados[self.refDatos][1]
      
      
    def resetearDataRef(self, esEntrenamiento):
        """ Restablece el conteo de iteraciones a través del conjunto de datos actuales """
        self.refDatos = 0 

        if esEntrenamiento:
            self.estadoEntrenamientoActual = self.datosFormateados.entrenamientoFormateados[self.refDatos][0]
            self.fenotipoEntrenamientoActual = self.datosFormateados.entrenamientoFormateados[self.refDatos][1]

        else:
            self.currentTestState = self.datosFormateados.pruebaFormateados[self.refDatos][0]
            self.currentTestPhenotype = self.datosFormateados.pruebaFormateados[self.refDatos][1]


    def iniciarModoEvaluacion(self):
        """ Turns on evaluation mode.  Saves the instance we left off in the training data. Also important when using RAIN."""
        self.guardarDatosRef = self.refDatos
        
        
    def detenerModoEvaluacion(self):
        """ Turns off evaluation mode.  Re-establishes place in dataset."""
        self.refDatos = self.guardarDatosRef
