"""
TANGENTE PENITENTE
- Nombre: surf.py
- Descripcion: El algoritmo SURFStar calcula el puntaje de cada atributo evaluando
su fuerza basado en los vecinos mas cercanos y mas lejanos. Devuelve una lista de
puntajes de atributos.
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

def EjecutarSURFStar(datos, fraccionMuestreoRelief):
    pass

def SURFStar(x, y, instMax, datos, fraccionMuestreoRelief):
    pass

def calcularMatrizDistancia(x, datos, instMax):
    pass

def hacerMapaMulticlases(y, instMax, datos):
    pass

def encontrarInstanciasDatos(distanciaPromedio, inst, matrizDistancias, instMax):
    pass

def evaluarSURF(x, y, NN, caracteristica, inst, datos, hacerMapaMulticlases, instMax):
    pass

def calcularDistancia(a, b, datos):
    pass