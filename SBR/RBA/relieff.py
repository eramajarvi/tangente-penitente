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
    """ Encuentra el numero de clases en el conjunto de datos y
    los guarda en el mapa """

    mapaMulticlases = {}

    for i in range(instMax):
        if (y[i] not in mapaMulticlases):
            mapaMulticlases[y[i]] = 0

        else:
            mapaMulticlases[y[i]] += 1

    # Para cada clase guardar su probabilida de ocurrencia en el 
    # conjunto de datos
    for each in datos.listaFenotipos:
        mapaMulticlases[each] = mapaMulticlases[each] / float(instMax)

    return mapaMulticlases

def encontrarVecinosMasCercanos_ReliefFMulticlase(x, y, vecinos, inst, datos, matrizDistancia, instMax, mapaMulticlase):
    """ Metodo que encuentra los vecinos mas cercanos en todo el
    conjunto de datos basado ya sea en una metrica de distancia
    o en una especificacion de los k-vecinos mas proximos
    # PARAM x- matriz que contiene los atributos de todos las instancias de datos
    # PARAM y- matriz que contiene las etquetas de clase de todas las instancias de datos
    # PARAM k- un numero entero que denota el numero de vecinos cercanos a considerar
    # PARAM r- Ninguno si el usuario quiere vecinos cercanos de todas las instancias de datos o indice si una instancia de datos que el usuario quiere considerar
    """

    NN = []

    # Encontrarndo los k-mas cercanos y los k-fallidos
    D_correctos = [] # Matriz de los mas cercanos - mide distancias
    indiceMinCorrectos = []

    almacenFallidos = {}

    for each in mapaMulticlase:
        # Se guarda todas las clases fallidas
        if each != y[inst]:
            almacenFallidos[each] = [[], []] # Guarda D_fallidos e indiceMinFallidos

            for n in range(vecinos):
                almacenFallidos[each][0].append(None)
                almacenFallidos[each][1].append(None)

    for n in range(vecinos):
        D_correctos.append(None)
        indiceMinCorrectos.append(None)

    for j in range(instMax):
        if inst != j:
            ubicador = [inst, j]
            # Acceder a la mitad correcta de la tabla
            ubicador = sorted(ubicador, reverse = True)

            d = matrizDistancia[ubicador[0]][ubicador[1]]

            # Correctos
            if y[j] == y[inst]:
                indiceMax = encontrarIndiceMax(D_correctos)

                # Si una distancia mas cercana es descubierta,
                # se hace una sustitucion
                if D_correctos[indiceMax] == None or d < D_correctos[indiceMax]:
                    D_correctos[indiceMax] = d
                    indiceMinCorrectos[indiceMax] = j

            # Fallidos
            else:
                for each in almacenFallidos:
                    if y[j] == each:
                        indiceMax = encontrarIndiceMax(almacenFallidos[each][0])

                        if almacenFallidos[each][0][indiceMax] == None or d < almacenFallidos[each][0][indiceMax]:
                            almacenFallidos[each][0][indiceMax] == d # D_fallidos
                            almacenFallidos[each][1][indiceMax] == j #indiceMinFallidos

    # Guardar los k-correctos mas cercanos
    for k in range(vecinos):
        if indiceMinCorrectos[k] != None:
            NN.append(indiceMinCorrectos[k])

    for each in almacenFallidos:
        for k in range(vecinos):
            if almacenFallidos[each][1][k] != None:
                NN.append(almacenFallidos[each][1][k])

    return NN

def encontrarVecinosMasCercanos_ReliefFContinuo(x, y, vecinos, inst, datos, matrizDistancia, instMax):
    """ Metodo que encuentra los vecinos mas cercanos en todo el
    conjunto de datos basado ya sea en una metrica de distancia o
    una especificacion de los k-vecinos mas cercanos.
    #PARAM x- matriz que contiene los atributos de todos los datos instancias
    #PARAM y- matriz que contiene las etiquetas de clase de todos los datos instancias
    #PARAM k- un numero entero que denota el numero de los vecinos mas cercanos a considerar
    #PARAM r- Ninguno si el usuario quiere los vecinos mas cercanos de todos los datos instancias o el indice de una instancia de datos que el usuario quiere considerar
    # """

    NN =[]

    # Limite para determinar similaridad entre clases de atributos continuos
    # DE = Desviacion Estandar
    limiteMismaClase = datos.DEFenotipo

    # Encontrar los k-correctos y k-fallidos mas cercanos
    D_correctos = [] # Matriz para correctos mas cercanos - mide distancias
    indiceMinCorrectos = []
    D_fallidos = [] # Matriz para fallidos mas cercanos - mide distancias
    indiceMinFallidos = []

    for n in range(vecinos):
        D_correctos.append(None)
        indiceMinCorrectos(None)
        D_fallidos.append(None)
        indiceMinFallidos.append(None)

    for j in range(instMax):
        if inst != j:
            ubicador = [inst, j]
            # Acceder a la mitad correcta de la tabla
            ubicador = sorted(ubicador, reverse = True)

            d = matrizDistancia[ubicador[0]][ubicador[1]]

            if abs(y[j] - y[inst]) < limiteMismaClase:
                indiceMax = encontrarIndiceMax(D_correctos)

                # Si se encuentra una distancia mas cercana, se
                # hace una sustitucion
                if D_correctos[indiceMax] == None or d < D_correctos[indiceMax]:
                    D_correctos[indiceMax] = d
                    indiceMinCorrectos[indiceMax] = j

            else:
                indiceMax = encontrarIndiceMax(D_fallidos)

                # Si se encuentra una distancia mas cercana, se
                # hace una sustitucion
                if D_fallidos[indiceMax] == None or d< D_fallidos[indiceMax]:
                    D_fallidos[indiceMax] = d
                    indiceMinFallidos[indiceMax] = j

    # Guardar los k-correctos mas cercanos
    for k in range(vecinos):
        if indiceMinCorrectos[k] != None:
            NN.append(indiceMinCorrectos[k])

        if indiceMinFallidos[k] != None:
            NN.append(indiceMinFallidos[k])

    return NN


def encontrarVecinosMasCercanos_ReliefFDiscreto(x, y, vecinos, inst, datos, matrizDistancia, instMax):
    """ Metodo que encuentra los vecinos mas cercanos en todo el
    conjunto de datos basado ya sea en una metrica de distancia
    o en una especificacion de los k-vecinos mas proximos
    # PARAM x- matriz que contiene los atributos de todos las instancias de datos
    # PARAM y- matriz que contiene las etquetas de clase de todas las instancias de datos
    # PARAM k- un numero entero que denota el numero de vecinos cercanos a considerar
    # PARAM r- Ninguno si el usuario quiere vecinos cercanos de todas las instancias de datos o indice si una instancia de datos que el usuario quiere considerar
    """

    pass

def evaluarReliefF(x, y, NN, caracteristica, inst, datos, mapaMulticlase, instMax):
    pass

def encontrarIndiceMax(matriz):
    valorMax = None
    indiceMax = None

    for i in range(len(matriz)):
        if matriz[i] == None:
            indiceMax = i
            return indiceMax

        else:
            if (valorMax == None) or (matriz[i] > valorMax):
                valorMax = matriz[i]
                indiceMax = i
            
    return indiceMax

def calcularDistancia(a, b, datos):
    """ Calcula la distancia entre dos clases en el conjunto de
    datos. Maneja atributos continuos y discretos. Los atributos
    continuos son acomodados al escalar la diferencia de distancia
    dentro del contexto del rango del atributo observado. Si un
    respectivo punto de datos esta faltando de cualquier instancia,
    es dejado por fuera de los calculos de distancia """

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
                # "Handling continuous attributes" - "Manejando atributos discretos"
                d += abs(float(a[i]) - float(b[i])) / float(limiteMax - limiteMin)
    
    return d