"""
TANGENTE PENITENTE
- Nombre: relieff.py
- Descripcion: El algoritmo RelieF calcula el puntaje de cada atributo
evaluando su fortaleza basada en los k-vecinos mas cercano. Devuelve
una lista de puntajes de atributos.
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

def EjecutarReliefF(datos, fraccionMuestreoRelief, vecinosRelief):
    """ Llamada a ejecutar el algoritmo ReliefF 
    #PARAM x - es una matriz que contiene los atributos de todas las instancias en el conjunto de datos
    #PARAM y - es una matriz que conteiene la clase de una instancia de datos """

    x = [ row[0] for row in datos.entrenamientoFormateados]
    y = [ row[1] for row in datos.entrenamientoFormateados]

    print("Ejecutando algoritmo ReliefF...")

    # Parametro m-numero de iteracion a ejecutar durante el procedimiento ReliefF
    instMax = int(float(fraccionMuestreoRelief) * len(x))
    # Parametro k-numero de vecinos mas cercanos a considerar
    vecinos = int(vecinosRelief)

    puntajes = ReliefF(x, y, instMax, vecinos, datos, fraccionMuestreoRelief)

    print("Ejecucion de ReliefF completada.")

    return puntajes

def ReliefF(x, y, instMax, vecinos, datos, fraccionMuestreoRelief):
    pass

def calcularMatrizDistancias(x, datos, instMax):
    pass

def hacerMapaMulticlases(y, instMax, datos):
    pass

def encontrarVecinosMasCercanos_ReliefFMulticlase(x, y, vecinos, inst, datos, matrizDistancia, instMax, mapaMulticlase):
    pass

def encontrarVecinosMasCercanos_ReliefFContinuo(x, y, vecinos, inst, datos, matrizDistancia, instMax):
    pass

def encontrarVecinosMasCercanos_ReliefFDiscreto(x, y, vecinos, inst, datos, matrizDistancia, instMax):
    pass

def evaluarReliefF(x, y, NN, caracteristica, inst, datos, mapaMulticlase, instMax):
    pass

def encontrarIndiceMax(matriz):
    pass

def calcularDistancia(a, b, datos):
    pass