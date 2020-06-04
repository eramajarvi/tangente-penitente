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
    """ Contra el principal bucle de ReliefF """

    listaPuntajes = []

    # Inicializando puntajes de los atributos en 0
    for i in range(datos.numAtributos):
        listaPuntajes.append(0)

    # Precalculas distancias entre todas los pares unicos de instancias
    # dentro del conjunto de datos.
    print("Precalculando matriz de distancias...")
    matrizDistancias = calcularMatrizDistancias(x, datos, instMax)
    print("Calculada")

    # Solo para matrices multiclases
    mapaMulticlases = None

    if datos.fenotipoDiscreto and len(datos.listaFenotipos) > 2:
        mapaMulticlases = hacerMapaMulticlases(y, instMax, datos)

    # Evaluando cada atributo sobre ejecutarIter
    for inst in range(instMax):
        if datos.fenotipoDiscreto: # Si es discreto
            if len(datos.listaFenotipos) > 2:
                # Se encuentra sus vecinos mas cercanos
                NN = encontrarVecinosMasCercanos_ReliefFMulticlase(x, y, vecinos, inst, datos, matrizDistancias, instMax, mapaMulticlases)

            else:
                # Se encuentra sus vecinos mas cercanos
                NN = encontrarVecinosMasCercanos_ReliefFDiscreto(x, y, vecinos, inst, datos, matrizDistancias, instMax)

        else:
            # Se encuentra sus vecinos mas cercanos
            NN = encontrarVecinosMasCercanos_ReliefFContinuo(x, y, vecinos, inst, datos, matrizDistancias, instMax)

        # Promediando los puntajes (Tal vez se necesite normalizar
        # antes para permitir ajustes de datos faltantes)
        for j in range(datos.numAtributos):
            listaPuntajes[j] = listaPuntajes[j] / (float(instMax) * vecinos)

        return listaPuntajes

def calcularMatrizDistancias(x, datos, instMax):
    # Hace un contenedor vacio para la matriz de distancias
    # (Solo se llenara la mitad no redundante de la matriz)
    matrizDistancias = []

    for i in range(instMax):
        matrizDistancias.append([])

        for j in range(instMax):
            matrizDistancias[i].append(None)

    for i in range(1, instMax):
        for j in range(0, i):
            matrizDistancias[i][j] = calcularDistancia(x[i], x[j], datos)

    return matrizDistancias

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