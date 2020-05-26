"""
TANGENTE PENITENTE
Nombre: multisurf.py
Descripcion: 
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

def Ejecutar_MultiSURF(datos):
    """ Se llama para ejecutar el algoritmo MultiSURF. \n
    PARAM x - es una matriz que contiene los atributos de todas las instancias en el conjunto de datos \n
    PARAM y - es una matriz que contiene la clase de una instancia de datos"""

    x = [row[0] for row in datos.entrenamientoFormateados]
    y = [row[1] for row in datos.entrenamientoFormateados]

    print("Ejecutando algoritmo MultiSURF...")

    puntajes = MultiSURF(x, y, datos)

    print("Ejecucion de MultiSURF completada")

    return puntajes

def MultiSURF(x, y, datos):
    """ Controla el principal bucle del MultiSURF """

    listaPuntajes = []

    # Inicializa los puntajes de los atributos en 0
    for i in range(datos.numAtributos):
        listaPuntajes.append(0)

    #Precomputa las distancias entre todos los pares de instancias unicas dentro del conjunto de datos
    print("Pre-computando la matriz de distancias...")
    
def multiClaseMultiSURF(x, y, datos):
    pass

def obtenerDesviacionEstandar(vectorDistancias, promedio):
    pass

def obtenerPromedio(vectorDistancias):
    pass

def obtenerDistanciasIndividuales(i, datos, matrizDistancias):
    pass

def calcularMatrizDistancias(x, datos):
    pass

def hacerMapaMultiClase(y, datos):
    pass

def haceMapaParClase(mapaMulticlase):
    pass

def calcularDistancia(a, b, datos):
    pass