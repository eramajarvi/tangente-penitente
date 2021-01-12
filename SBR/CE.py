# TANGENTE PENITENTE
# CE.py

"""
Un paso de preprocesamiento cuando se activa en Tangente Penitente. Convierte las puntuaciones numéricas del conocimiento experto de cualquier fuente 
en probabilidades para orientar el mecanismo de covering en la determinación de los atributos que se especificarán y los que se generalizarán. Esta 
estrategia fue propuesta y publicada por Ryan Urbanowicz, Delaney Granizo-Mackenzie y Jason Moore en "Using Expert Knowledge to Guide Covering and 
Mutation in a Michigan Style Learning Classifier System to Detecting Epistasis and Heterogeneity". [2012].
"""

from SBR.RBA.relieff import EjecutarReliefF
from SBR.RBA.surfstar import EjecutarSURFStar
from SBR.RBA.multisurf import Ejecutar_MultiSURF
from SBR.RBA.turf_envoltorio import TurfEnvoltorio
import os
import copy
import time
from RBA.multisurf import *
from RBA.relieff import *
from RBA.surf import *
from RBA.surfstar import *
from RBA.turf_envoltorio import *

class ConocimientoExperto:
    def __init__(self, cons):
        """ Inicializacion del Conocimiento Experto - Los puntajes se ordenan segun aparecen en el conjunto de datos """

        self.puntajes = None
        self.rangoCE - None

        if cons.GeneracionInternaCE or cons.soloPuntajesCE:
            print("ConocimientoExperto: Se inicio la generacion interna del CE")
            self.puntajes = self.ejecutarFiltros(cons)

        else:
            print("ConocimientoExperto: Cargando CE externo")
            self.puntajes = self.cargarCE(cons.fuenteCE, cons)

        # Nos aseguramos que los puntajes no sean negativos
        self.ajustarPuntajes(cons)

        # Nuevo protocolo de especificacion
        self.sumaCE = sum(self.puntajes)
        self.rangoCE = []

        CEtemp = copy.deepcopy(self.puntajes)

        for i in range(len(self.puntajes)):
            mejorCE = CEtemp[0]
            mejorC = 0

            for j in range(1, len(CEtemp)):
                if CEtemp[j] > mejorCE:
                    mejorCE = CEtemp[j]
                    mejorC = j

            self.rangoCE.append(mejorC)
            CEtemp[mejorC] = 0

        # Usado para seleccionar atributos para la especificacion en el covering (sin reemplazos)
        self.listaRef = []
        for i in range(len(self.puntajes)):
            self.listaRef.append(i)

        # Convertir la lista de puntajes ajustados en probabilidades
        valorMax = max(self.puntajes)
        listaProb = []

        for i in range(cons.amb.datosFormateados.numAtributos):
            if valorMax == 0.0:
                listaProb.append(0.5)

            else:
                listaProb.append(self.puntajes[i]/float(valorMax + valorMax * 0.01))

        self.listaProbabilidadCE = listaProb

    def ajustarPuntajes(self, cons):
        """ Se asegura que el valor del puntaje minimo sea cero """
        CEmin = min(self.puntajes)

        if CEmin < 0:
            for i in range(len(self.puntajes)):
                # Adicionar 0.01 previene que el atributo con el puntaje mas bajo no tenga un peso nulo
                self.puntajes[i] = self.puntajes[i] - CEmin + cons.aptitudInicial

    def ejecutarFiltros(self, cons):
        """ Ejecuta el algoritmo filtro especificado y crea a la salida un archivo de texto filtro en el mismo formato que el software MDR (Reduccion de dimensionalidad multifactor / multifactor dimmensionality reduction) """
        nombreArchivo = str(cons.nombrearchivoSalidaCE) + '_' + str(cons.algoritmoFiltro) + '_puntajes.txt'

        if not os.path.exists(nombreArchivo):
            referenciaInicioGlobal = time.time()
            nombreEtiqueta = None
            foo = None
            bar = None

            if cons.algoritmoFiltro == "multisurf_turf":
                turf = TurfEnvoltorio(cons.amb, cons.algoritmoFiltro, cons.porcentajeTurf, foo, bar)
                puntajesFiltro = turf.puntajesFiltro
                nombreEtiqueta = 'MultiSURF_TuRF'

            elif cons.algoritmoFiltro == "surfstar_turf":
                turf = TurfEnvoltorio(cons.amb, cons.algoritmoFiltro, cons.porcentajeTurf, cons.fraccionMuestreoRelief, foo)
                puntajesFiltro = turf.puntajesFiltro
                nombreEtiqueta = 'SURFStar_TuRF'

            elif cons.algoritmoFiltro == "surf_turf":
                turf = TurfEnvoltorio(cons.amb, cons.algoritmoFiltro, cons.porcentajeTurf, cons.fraccionMuestreoRelief, foo)
                puntajesFiltro = turf.puntajesFiltro
                nombreEtiqueta = 'SURF_TuRF'

            elif cons.algoritmoFiltro == "relieff_turf":
                turf = TurfEnvoltorio(cons.amb, cons.algoritmoFiltro, cons.porcentajeTurf, cons.fraccionMuestreoRelief, cons.vecinosRelief)
                puntajesFiltro = turf.puntajesFiltro
                nombreEtiqueta = 'ReliefF_TuRF'

            elif cons.algoritmoFiltro == "multisurf":
                puntajesFiltro = Ejecutar_MultiSURF(cons.amb.datosFormateados)
                nombreEtiqueta = 'MultiSURF'

            elif cons.algoritmoFiltro == "surfstar":
                puntajesFiltro = EjecutarSURFStar(cons.amb.datosFormateados, cons.fraccionMuestreoRelief)
                nombreEtiqueta = 'SURFStar'

            elif cons.algoritmoFiltro == "relieff":
                algoritmoFiltro = EjecutarReliefF(cons.amb.datosFormateados, cons.fraccionMuestreoRelief, cons.vecinosRelief)
                nombreEtiqueta = 'ReliefF'

            else:
                print("Conocimiento Experto - ERROR: Algoritmo no encontrado.")

            tiempoGlobal = (time.time() - referenciaInicioGlobal)

            # Salida del archivo de los puntajes de atributos basados en ReliefF

            try:
                filtroSalida = open(nombreArchivo, 'w')

            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('No se puede abrir', nombreArchivo)
                raise

            print(puntajesFiltro)

            filtroSalida.write(str(nombreEtiqueta) + " Analisis completado con Tangente Penitente" + '\n')
            filtroSalida.write("Tiempo de ejecucion [s]:" + str(tiempoGlobal) + '\n')
            filtroSalida.write("=== PUNTAJES ===" + '\n')
            listaPuntajes = []

            for i in range(len(puntajesFiltro)):
                listaPuntajes.append([cons.amb.datosFormateados.listaEncabezadoEntrenamiento[i], puntajesFiltro[i]])

            listraFiltrosOrdenada = sorted(listaPuntajes, key=lambda test:test[1], reverse=True)

            for i in range(len(listraFiltrosOrdenada)):
                filtroSalida.write(str(listraFiltrosOrdenada[i][0]) + '\t')
                filtroSalida.write(str(listraFiltrosOrdenada[i][1]) + '\t')
                filtroSalida.write(str(i + 1) + '\n')

            filtroSalida.close()
            return puntajesFiltro

            # -------------------------------------------------

        # El archivo de puntajes de atributos ya existe - entonces se carga el archivo existente y se procede a volver a ejecutar el algoritmo de puntajes de atributos
        else:
            try:
                listaValoresOrdenados = self.cargarCE(cons.nombreArchivoSalidaCE + '_' + str(cons.algoritmoFiltro) + '_puntajes.txt', cons)

            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('No se pudo abrir', cons.nombreArchivoSalidaCE + '_' + str(cons.algoritmoFiltro) + '_puntajes.txt')

            else:
                return listaValoresOrdenados


    def cargarCE(self, nombreRuta, cons):
        pass
