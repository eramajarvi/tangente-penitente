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
        pass

    def EjecutarTurf(self):
        pass