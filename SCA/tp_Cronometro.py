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
from tp_Constantes import *
import time
#

class Cronometro:
    def __init__(self):
        """ Inicializa todos los valores de los cronometros para el algoritmo """      
        # Objetos de Tiempo Globales
        self.refInicioGlobal = time.time()
        self.tiempoGlobal = 0.0
        self.tiempoAgregado = 0.0
        
        # Variables de tiempo de Coincidencias
        self.iniciarRefCoincidencia = 0.0
        self.coincidenciaGlobal = 0.0

        # Variables de tiempo de covering
        self.iniciarRefCovering = 0.0
        self.coveringGlobal = 0.0
        
        # Varibales de tiempo de eliminacion
        self.iniciarRefEliminacion = 0.0
        self.eliminacionGlobal = 0.0

        # Variables de tiempo de subsuncion
        self.iniciarRefSubsuncion = 0.0
        self.subsuncionGlobal = 0.0

        # Variables de tiempo de seleccion
        self.iniciarRefSeleccion = 0.0
        self.seleccionGlobal = 0.0
        
        # Variables de tiempo de cruzamiento
        self.iniciarRefCruzamiento = 0.0
        self.cruzamientoGlobal = 0.0
        
        # Variables de tiempo de mutacion
        self.iniciarRefMutacion = 0.0
        self.mutacionGlobal = 0.0
        
        # Seguimiento de atributos y feedback
        self.iniciarRefSA = 0.0
        self.SAGlobal = 0.0

        # Conocimiento Experto (CE)
        self.iniciarRefCE = 0.0
        self.CEGlobal = 0.0

        # Archivo de Salida
        self.iniciarRefArchivoSalida = 0.0
        self.archivoSalidaGlobal = 0.0

        # Inicializacion
        self.iniciarRefInic = 0.0
        self.inicGlobal = 0.0
        
        # Agregar clasificador
        self.iniciarRefAgg = 0.0
        self.aggGlobal = 0.0
        
        # Variables de tiempo de evaluacion
        self.iniciarRefEvaluacion = 0.0
        self.evaluacionGlobal = 0.0  
        
        # Compactacion de reglas
        self.iniciarRefCompReg = 0.0
        self.compRegGlobal = 0.0

        # PRUEBA
        self.iniciarRefPRUEBA = 0.0
        self.PRUEBAGlobal = 0.0
        
        # 
        self.cronometroPRUEBAGlobal = 0
        
    # ------------------------------------------------------------
    def iniciarTiempoCoincidencias(self):
        """ Cuenta el tiempo de coincidencias """
        self.iniciarRefCoincidencia = time.time()
         
    def detenerTiempoCoincidencias(self):
        """ Cuenta el tiempo de coincidencias """
        diff = time.time() - self.iniciarRefCoincidencia
        self.coincidenciaGlobal += diff        

    # ------------------------------------------------------------
    def iniciarTiempoCovering(self):
        """ Cuenta el tiempo del covering """
        self.iniciarRefCovering = time.time()
         
    def detenerTiempoCovering(self):
        """ Cuenta el tiempo del covering """
        diff = time.time() - self.iniciarRefCovering
        self.coveringGlobal += diff        
        
    # ------------------------------------------------------------
    def iniciarTiempoEliminacion(self):
        """ Cuenta el tiempo de eliminacion """
        self.iniciarRefEliminacion = time.time()
        
    def detenerTiempoEliminacion(self):
        """ Cuenta el tiempo de eliminacion """
        diff = time.time() - self.iniciarRefEliminacion
        self.eliminacionGlobal += diff
    
    # ------------------------------------------------------------
    def iniciarTiempoCruzamiento(self):
        """ Cuenta el tiempo del cruzamiento """
        self.iniciarRefCruzamiento = time.time() 
               
    def detenerTiempoCruzamiento(self):
        """ Cuenta el tiempo del cruzamiento """
        diff = time.time() - self.iniciarRefCruzamiento
        self.cruzamientoGlobal += diff
        
    # ------------------------------------------------------------
    def iniciarTiempoMutacion(self):
        """ Cuenta el tiempo de la mutacion """
        self.iniciarRefMutacion = time.time()
        
    def detenerTiempoMutacion(self):
        """ Cuenta el tiempo de la mutacion """
        diff = time.time() - self.iniciarRefMutacion
        self.mutacionGlobal += diff
        
    # ------------------------------------------------------------
    def iniciarTiempoSubsuncion(self):
        """ Cuenta el tiempo de subsuncion """
        self.iniciarRefSubsuncion = time.time()

    def detenerTiempoSubsuncion(self):
        """ Cuenta el tiempo de subsuncion """
        diff = time.time() - self.iniciarRefSubsuncion
        self.globalSubsumption += diff    
        
    # ------------------------------------------------------------
    def iniciarTiempoSeleccion(self):
        """ Cuenta el tiempo de seleccion """
        self.iniciarRefSeleccion = time.time()
        
    def detenerTiempoSeleccion(self):
        """ Cuenta el tiempo de seleccion """
        diff = time.time() - self.iniciarRefSeleccion
        self.globalSelection += diff
    
    # ------------------------------------------------------------
    def iniciarTiempoEvaluacion(self):
        """ Cuenta el tiempo de evaluacion """
        self.iniciarRefEvaluacion = time.time()
        
    def detenerTiempoEvaluacion(self):
        """ Cuenta el tiempo de evaluacion """
        diff = time.time() - self.iniciarRefEvaluacion
        self.globalEvaluation += diff 
    
    # ------------------------------------------------------------
    def iniciarTiempoCompReg(self):
        """ Cuenta el tiempo de compactacion de reglas """
        self.iniciarRefCompReg = time.time()   
         
    def detenerTiempoCompReg(self):
        """ Cuenta el tiempo de compactacion de reglas """
        diff = time.time() - self.iniciarRefCompReg
        self.globalRuleCmp += diff
        
    # ------------------------------------------------------------
    def iniciarTiempoSA(self):
        """ Cuenta el tiempo del seguimiento de atributos """
        self.iniciarRefSA = time.time()   
         
    def detenerTiempoSA(self):
        """ Cuenta el tiempo del seguimiento de atributos """
        diff = time.time() - self.iniciarRefSA
        self.globalAT += diff
        
    # ------------------------------------------------------------
    def iniciarTiempoCE(self):
        """ Cuenta el tiempo de conocimiento experto """
        self.iniciarRefCE = time.time()   
         
    def detenerTiempoCE(self):
        """ Cuenta el tiempo de conocimiento experto """
        diff = time.time() - self.iniciarRefCE
        self.globalEK += diff
        
    # ------------------------------------------------------------
    def iniciarTiempoArchivoSalida(self):
        """ Cuenta el tiempo del archivo de salida """
        self.iniciarRefArchivoSalida = time.time()   
         
    def detenerTiempoArchivoSalida(self):
        """ Cuenta el tiempo del archivo de salida """
        diff = time.time() - self.iniciarRefArchivoSalida
        self.globalOutFile += diff
        
    # ------------------------------------------------------------
    def iniciarTiempoInic(self):
        """ Cuenta el tiempo de inicializacion """
        self.iniciarRefInic = time.time()   
         
    def detenerTiempoInic(self):
        """ Cuenta el tiempo de inicializacion """
        diff = time.time() - self.iniciarRefInic
        self.globalInit += diff
        
    # ------------------------------------------------------------
    def iniciarTiempoAgg(self):
        """ Cuenta el tiempo de agregamiento """
        self.iniciarRefAgg = time.time()   
         
    def detenerTiempoAgg(self):
        """ Cuenta el tiempo de agregamiento """
        diff = time.time() - self.iniciarRefAgg
        self.globalAdd += diff
        
    # ------------------------------------------------------------
    def iniciarTiempoPRUEBA(self):
        """  """
        self.iniciarRefPRUEBA = time.time()   
         
    def detenerTiempoPRUEBA(self):
        """  """
        diff = time.time() - self.iniciarRefPRUEBA
        self.globalTEST += diff
    # ------------------------------------------------------------
    
    def devolverCronometroGlobal(self):
        """ Fija el cronometro final global. Llamado al final de toda la ejecucion """
        self.tiempoGlobal = (time.time() - self.refInicioGlobal) + self.tiempoAgregad
        return self.tiempoGlobal/ 60.0
        
        
    def cronometroPRUEBA(self):
        """ Fija el cronometro final global. Llamado al final de toda la ejecucion """
        self.globalTESTCounter += 1

    
    def fijarReinicioCronometro(self, rehacerArchivo): 
        """ Fija todos los valores de los cronometros a los escritos previamente en el perfil cargado """
        print(rehacerArchivo + "_EstadisticasPoblacion.txt")
        try:
            objetoArchivo = open(rehacerArchivo+"_EstadisticasPoblacion.txt", 'rU')  # abre cada archivo de datos para leerlo
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('No se pudo abrir', rehacerArchivo+"_EstadisticasPoblacion.txt")
            raise 

        refDatosTiempo = 22
        lineaTemp = None

        for i in range(refDatosTiempo):
            lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t')
        self.tiempoAgregado = float(listaTemp[1]) * 60 # tiempo previo global agregado con el reinicio
        
        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.coincidenciaGlobal = float(listaTemp[1]) * 60

        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.coveringGlobal = float(listaTemp[1]) * 60
        
        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.eliminacionGlobal = float(listaTemp[1]) * 60

        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.subsuncionGlobal = float(listaTemp[1]) * 60
        
        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.seleccionGlobal = float(listaTemp[1]) * 60    
 
        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.cruzamientoGlobal = float(listaTemp[1]) * 60

        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.mutacionGlobal = float(listaTemp[1]) * 60

        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.SAGlobal = float(listaTemp[1]) * 60
 
        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.CEGlobal = float(listaTemp[1]) * 60

        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.archivoSalidaGlobal = float(listaTemp[1]) * 60

        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.inicGlobal = float(listaTemp[1]) * 60
        
        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.aggGlobal = float(listaTemp[1]) * 60
        
        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.evaluacionGlobal = float(listaTemp[1]) * 60
                     
        lineaTemp = objetoArchivo.readline()
        listaTemp = lineaTemp.strip().split('\t') 
        self.compRegGlobal = float(listaTemp[1]) * 60
        
        objetoArchivo.close()
        

    def reportarTiempos(self):
        self.devolverCronometroGlobal()
        """ Reporta los resumenes de tiempo para esta ejecucion. Devuelve un string listo para imprimirse """

        tiempoSalida = "Tiempo global\t"+str(self.tiempoGlobal/ 60.0)+ \
        "\nTiempo de Coincidencia\t" + str(self.coincidenciaGlobal/ 60.0)+ \
        "\nTiempo de Covering\t" + str(self.coveringGlobal/ 60.0)+ \
        "\nTiempo de Eliminacion\t" + str(self.eliminacionGlobal/ 60.0)+ \
        "\nTiempo de Subsuncion\t" + str(self.subsuncionGlobal/ 60.0)+ \
        "\nTiempo de Seleccion\t"+str(self.seleccionGlobal/ 60.0)+ \
        "\nTiempo de Cruzamiento\t" + str(self.cruzamientoGlobal/ 60.0)+ \
        "\nTiempo de Mutacion\t" + str(self.mutacionGlobal/ 60.0)+ \
        "\nTiempo de Seguimiento de Atributos/Feedback\t"+str(self.SAGlobal/ 60.0) + \
        "\nTiempo de Conocimiento Experto\t"+str(self.CEGlobal/ 60.0) + \
        "\nTiempo de Archivo de Salida\t"+str(self.archivoSalidaGlobal/ 60.0) + \
        "\nTiempo de Inicializacion\t"+str(self.inicGlobal/ 60.0) + \
        "\nTiempo de Agregar Clasificador\t"+str(self.aggGlobal/ 60.0) + \
        "\nTiempo de Evaluacion\t"+str(self.evaluacionGlobal/ 60.0) + \
        "\nTiempo de Compactacion de Reglas\t"+str(self.compRegGlobal/ 60.0) + "\n" 
        
        return tiempoSalida