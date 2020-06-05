"""
TANGENTE PENITENTE
- Nombre: surf.py
- Descripcion: El algoritmo Surf calcula el puntaje de cada atributo evaluando su fortaleza basada en los vecinos mas cercanos.
Devuelve una lista de puntajes de atributos.
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

def EjecutarSURF(datos, fraccionMuestreoRelief):
    """ Llamado para ejecutar el algoritmo SURF 
    #PARAM x - es una matriz que contiene los atributos de todas las instancias en el conjunto de datos
    #PARAM y - es una matriz que contiene la clase de una instancia de datos """

    x = [ row[0] for row in datos.entrenamientoFormateados]
    y = [ row[1] for row in datos.entrenamientoFormateados]

    print("Ejecutando algoritmo SURF...")

    # Parametro m-numero de iteracion a ejecutar durante el procedimiento de relieff
    instMax = int(float(fraccionMuestreoRelief) * len(x))
    puntajes = SURF(x, y, instMax, datos, fraccionMuestreoRelief)

    print("Ejecucion de SURF completada.")

    return puntajes

def SURF(x, y, instMax, datos, fraccionMuestreoRelief):
    """ Controla el principal bucle del SURF """
    listaPuntajes = []

    for i in range(datos.numAtributos):
        # Inicializando puntajes de los atributos en 0
        listaPuntajes.append(0)

    # Precalcular distancias entre pares unicos de instancias
    # dentro del conjunto de datos
    print("Precalculando matriz de distancias")
    objetoDistancia = calcularMatrizDistancias(x, datos, instMax)
    matrizDistancias = objetoDistancia[0]
    distanciaPromedio = objetoDistancia[1]
    print("Calculado.")

    # Solo para matrices multiclases
    mapaMulticlases = None

    if datos.fenotipoDiscreto and len(datos.listaFenotipos) > 2:
        mapaMulticlases = hacerMapaMulticlases(y, instMax, datos)

    # Evaluar cada atributo sobre ejecucion
    for inst in range(instMax):
        NN = encontrarVecinosMasCercanos_SURF(distanciaPromedio, inst, matrizDistancias, instMax)

        if len(NN) > 0:
            for j in range(datos.numAtributos):
                listaPuntajes[j] += evaluarSURF(x, y, NN, j, inst, datos, mapaMulticlases, instMax)

    return listaPuntajes

def calcularMatrizDistancias(x, datos, instMax):
    """ En SURF este metodo precalcula la matriz de distancias y la distancia promedio """
    # Hacer contenedor vacio de matriz de distancias
    matrizDistancias = []
    distanciaPromedio = 0
    conteo = 0

    for i in range(instMax):
        matrizDistancias.append([])

        for j in range(instMax):
            matrizDistancias[i].append(None)

    for i in range(1, instMax):
        for j in range(0, i):
            matrizDistancias[i][j] = calcularDistancia(x[i], x[j], datos)
            conteo += 1
            distanciaPromedio += matrizDistancias[i][j]

    distanciaPromedio = distanciaPromedio / float(conteo)
    objetoDevuelto = [matrizDistancias, distanciaPromedio]

    return objetoDevuelto

def hacerMapaMulticlases(y, instMax, datos):
    # Encontrar el numero de clases en el conjunto de datos y los
    # guarda en el mapa

    mapaMulticlases = {}

    for i in range(instMax):
        if (y[i] not in mapaMulticlases):
            mapaMulticlases[y[i]] = 0

        else:
            mapaMulticlases[y[i]] += 1

    # Para cada clase guardar la probabilidad de la ocurrencia de 
    # la clase en el conjunto de datos
    for each in datos.listaFenotipos:
        mapaMulticlases[each] = mapaMulticlases[each] / float(instMax)

    return mapaMulticlases

def encontrarVecinosMasCercanos_SURF(distanciaPromedio, inst, matrizDistancias, instMax):
    """ Metodo para encontrar los vecinos mas cercanos en todo el conjunto de datos, basado
    ya sea en una metrica de distancia o en una especificacion de los k-vecinos mas cercanos.
    #PARAM x - matriz que contiene los atributos de todas las instancias de datos
    #PARAM y - matriz que contiene las etiquetas de clases de todos las isntancias datos
    #PARAM k - un numero entero que denota el numero de vecinos mas cercanos a considerar
    #PARAM r - Ninguno si el suario quiere los vecinos mas cercanos de todas las instancias de datos
    o  indice si es una instancia de datos que el usuario quiere considerar """

    NN = []
    indicesMin = []

    for j in range(instMax):
        if inst != j:
            ubicador = [inst, j]
            ubicador = sorted(ubicador, reverse = True)
            d = matrizDistancias[ubicador[0]][ubicador[1]]

            if d < distanciaPromedio:
                indicesMin.append(j)

    for j in range(len(indicesMin)):
        NN.append(indicesMin[j])

    return NN

def evaluarSURF(x, y, NN, caracteristica, inst, datos, mapaMulticlase, instMax):
    pass

def calcularDistancia(a, b, datos):
    """ Calcula la distancia entre dos intancias en el conjunto de
    datos. Maneja atributos discretos y continuos. Atributos continuos
    son acomodados al escalar la diferencia de distancia dentro del contexto
    del rango del atributo observado. Si un respectivo punto de datos
    falta de cualquier instancia, se deja por fuera del calculo de distancia. """

    # Distancia
    d = 0

    for i in range(datos.numAtributos):
        if a[i] != datos.etiquetaDatosFaltantes and b[i] != datos.etiquetaDatosFaltantes:
            # Atributo discreto
            if not datos.infoAtributos[i][0]:
                if a[i] != b[i]:
                    d += 1

            # Atributo continuo
            else:
                limiteMin = float(datos.infoAtributos[i][1][0])
                limiteMax = float(datos.infoAtributos[i][1][1])
                # Kira & Rendell, 1992
                # "Handling continuous attributes"
                d += abs(float(a[i]) - float(b[i])) / float(limiteMax - limiteMin)

    return d