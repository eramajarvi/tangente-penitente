"""
TANGENTE PENITENTE
- Nombre: turf_envoltorio.py
- Descripcion: El algoritmo turf itera sobre algun otro algoritmo basado en Relief (RBA), cada vez filtrando
un porcentaje dado de atributos restantes. Esto permite que los puntajes de algoritmos basados en Relief
sean reajustados despues de filtrar probales atributos ruidosos.
---------------------------------------------------------------------------------------------------------------------------------------------------
ReBATE v1.0: incluye un código Python autónomo para ejecutar cualquiera de los algoritmos basados en Relief incluidos/disponibles diseñados para 
el filtrado/clasificación de atributos. Estos algoritmos son una forma rápida de identificar los atributos en el conjunto de datos que pueden ser 
más importantes para predecir algún endpoint fenotípico. Estos scripts producen un conjunto ordenado de nombres de atributos, junto con sus 
respectivas puntuaciones (determinadas de forma única por el algoritmo particular seleccionado). Ciertos algoritmos requieren que se especifiquen 
los parámetros clave de ejecución. Este código se basa en gran medida en los algoritmos basados en Relief implementados en el software de reducción 
de la dimensionalidad multifactorial (MDR). Sin embargo, estas implementaciones se han ampliado para dar cabida a los atributos continuos 
(y a los atributos continuos mezclados con los atributos discretos) así como a un endpoint continuo. Este código también tiene en cuenta los puntos
de datos que faltan. Construido en este código, hay una estrategia para detectar automáticamente a partir de los datos cargados, estas 
características relevantes.
---------------------------------------------------------------------------------------------------------------------------------------------------------
"""

from relieff import *
from surf import *
from surfstar import *
from multisurf import *

class TurfEnvoltorio:
    def __init__(self, amb, algoritmo, porcentajeTurf, fraccionMuestreoRelief, vecinosRelief):
        self.datos = amb.datosFormateados
        self.algoritmo = algoritmo
        self.fraccionMuestreoRelief = fraccionMuestreoRelief
        self.vecinosRelief = vecinosRelief

        self.filtroPuntajes = []
        self.conservarMantenimiento = True
        self.conservarAlgoritmosCorriendo = True
        self.porcentajeTurf = porcentajeTurf
        self.N = int(1/float(porcentajeTurf)) # Numero de iteraciones

        print("Ejecutando turf para " + str(self.N) + " iteraciones.")

        self.datos.guardarDatosTurf()
        self.EjecutarTurf()
        self.datos.devolverDatosCompletos()
        amb.resetearRefDAtos(True)

    def EjecutarTurf(self):
        
        i = 0

        while i < self.N - 1 and self.conservarAlgoritmosCorriendo:
            # Escoger y ejecutar el algoritmo deseado
            if self.algoritmo == "multisurf_turf":
                self.filtroPuntajes = Ejecutar_MultiSURF(self.datos)

            elif self.algoritmo == "surfstar_turf":
                self.filtroPuntajes = EjecutarSURFStar(self.datos, self.fraccionMuestreoRelief)

            elif self.algoritmo == "surf_turf":
                self.filtroPuntajes = EjecutarSURF(self.datos, self.fraccionMuestreoRelief)

            elif self.algoritmo == "relieff_turf":
                self.filtroPuntajes = EjecutarReliefF(self.datos, self.fraccionMuestreoRelief)

            else:
                print("ERROR: Algoritmo no encontrado.")

            if not self.conservarMantenimiento:
                self.conservarAlgoritmosCorriendo = False

            # Filtrar los datos, todos menos la ultima iteracion
            if self.conservarMantenimiento and not iter == (self.N - 1):
                self.conservarMantenimiento = self.datos.gestionDatosTurf(self.filtroPuntajes, self.porcentajeTurf)

            i += 1

        # Encontrar puntaje bajo
        puntajeBajo = min(self.filtroPuntajes)
        puntajeMaximo = max(self.filtroPuntajes)

        esteRango = puntajeMaximo - puntajeBajo

        reduccionPuntajeEmpate = 0.01 * esteRango

        # Definir puntajes de empate (puntaje unico para todos los atributos
        # eliminados en un empate especifico)

        puntajesEmpate = []

        for k in range(len(self.datos.listaEmpates)):
            puntajesEmpate.append(puntajeBajo - (reduccionPuntajeEmpate * (k + 1)))

        # Se voltea porque el peor puntaje fue el primero en la lista de empates
        puntajesEmpate.reverse()

        # Ciclo a traves de la lista original de encabezados 
        # (todos los atributos y construye un nuevo puntajefiltro 
        # desde 0)
        puntajesFinalesFiltro = []

        # Todos los atributos originales
        for j in range(len(self.datos.listaEncabezadosTurf)):
            # Encontrar donde este atributo esta (lista puntaje final
            # o uno de los empates eliminados)
            if self.datos.listaEncabezadosTurf[j] in self.datos.listaEncabezadosEntrenamiento:
                puntajeID = self.datos.listaEncabezadosEntrenamiento.index(self.datos.listaEncabezadosTurf[j])
                puntajesFinalesFiltro.append(self.filtroPuntajes[puntajeID])

            # Filtrados
            else:
                for k in range(len(self.datos.listaEmpates)):
                    if self.datos.listaEncabezadosTurf[j] in self.datos.listaEmpates[k]:
                        puntajesFinalesFiltro.append(puntajesEmpate[k])

        print(puntajesFinalesFiltro)
        self.filtroPuntajes = puntajesFinalesFiltro
