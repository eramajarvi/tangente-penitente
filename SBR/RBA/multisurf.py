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

    matrizDistancias = calcularMatrizDistancias(x, datos)

    print("Computado")

    limitesMismaClase = datos.DEFenotipo

    D = []
    distanciasPromedio = []

    for i in range(datos.numInstanciasEntrenamiento):
        vectorDistancias = []
        vectorDistancias = obtenerDistanciasIndividuales(i, datos, matrizDistancias)
        distanciasPromedio.append(obtenerPromedio(vectorDistancias))
        desviacionEstandar = obtenerDesviacionEstandar(vectorDistancias, distanciasPromedio[i])
        D.append(desviacionEstandar/2.0)

    # Haciendo un bucle en los atributos
    for k in range(datos.numAtributos):
        if datos.infoAtributos[k][0]: # Atributo continuo
            minA = datos.infoAtributos[k][1][0]
            maxA = datos.infoAtributos[k][1][1]

        conteoCercaDe = 0
        conteoFallidoCercaDe = 0
        conteoLejosDe = 0
        conteoFallidoLejosDe = 0

        diferenciaCercaDe = 0 # Inicializando el puntaje en 0
        diferenciaFallidosCercaDe = 0
        diferenciaLejosDe = 0
        diferenciaFallidosLejosDe = 0

        for i in range(datos.numInstanciasEntrenamiento):
            for j in range(i, datos.numInstanciasEntrenamiento):
                if i != j and x[i][k] != datos.etiquetaDatosFaltantes and x[j][k] != datos.etiquetaDatosFaltantes:
                    localizador = [i, j]
                    localizador = sorted(localizador, reversed = True) # Accede a la mitad correcta de la tabla (resultado de redundancia de la tabla eliminada)
                    d = matrizDistancias[localizador[0]][localizador[1]]

                    # Cercanos
                    if (d < distanciasPromedio[i] - D[i]):
                        # Fenotipo discreto
                        if (datos.fenotipoDiscreto):

                            # El mismo endpoint
                            if y[i] == y[j]:
                                conteoCercaDe += 1

                                if x[i][k] != x [j][k]:
                                    # Atributo continuo (puntajes cercanos de atributo para fenotipos cercanos deben arrojar una penalidad mayor de atributos)
                                    if datos.infoAtributos[k][0]:
                                        diferenciaCercaDe -= (abs(x[i][k] - x[j][k]) / (maxA - minA))
                                    
                                    # Discreto
                                    else:
                                        diferenciaCercaDe -= 1
                            
                            # Diferente endpoint
                            else:
                                conteoFallidoCercaDe += 1

                                if x[i][k] != x[j][k]:
                                    # Atributo continuo (puntajes mas lejanos de atributos para fenotipos diferentes cercanos deben arrojar bonus de atributos mayores)
                                    if datos.infoAtributos[k][0]:
                                        diferenciaFallidosCercaDe += abs(x[i][k] - x[j][k]) / (maxA - minA)

                                    # Discreto
                                    else:
                                        diferenciaFallidosCercaDe += 1

                        # Fenotipo continuo
                        else:
                            if abs(y[i] - y[j]) < limitesMismaClase:
                                conteoCercaDe += 1

                                if x[i][k] != x[j][k]:
                                    # Atributo continuo
                                    if datos.infoAtributos[k][0]:
                                        diferenciaCercaDe -= (abs(x[i][k] - x[j][k]) / (maxA - minA))
                                    
                                    # Discreto
                                    else:
                                        diferenciaCercaDe -= 1

                            else:
                                conteoFallidoCercaDe += 1

                                if x[i][k] != x[j][k]:
                                    # Atributo continuo
                                    if datos.infoAtributos[k][0]:
                                        diferenciaFallidosCercaDe += abs(x[i][k] - x[j][k]) / (maxA - minA)
                                    
                                    # Discreto
                                    else:
                                        diferenciaFallidosCercaDe += 1

                    # Lejanos
                    if (d > distanciasPromedio[i] + D[i]):
                        # Endpoint discreto
                        if datos.fenotipoDiscreto:
                            if y[i] == y [j]:
                                conteoLejosDe += 1

                                # Atributo continuo
                                if datos.infoAtributos[k][0]:
                                    # Atributo siendo similar es mas importante
                                    diferenciaLejosDe -= (abs(x[i][k] - x[j][k])) / (maxA - minA)

                                # Atributo discreo
                                else:
                                    if x[i][k] == x[j][k]:
                                        diferenciaLejosDe -= 1

                            else:
                                conteoFallidoLejosDe += 1

                                # Atributo continuo
                                if datos.infoAtributos[k][0]:
                                    # Atributo siendo similar es mas importante
                                    diferenciaFallidosLejosDe += abs(x[i][k] - x[j][k])/(maxA - minA)

                                # Atributo discreto
                                else:
                                    if x[i][k] == x[j][k]:
                                        diferenciaFallidosLejosDe += 1

                        # Endpoint continuo
                        else:
                            if abs(y[i] - y[j]) < limitesMismaClase:
                                conteoLejosDe += 1

                                # Atributo continuo
                                if datos.infoAtributos[k][0]:
                                    # Atributo siendo similar es mas importante
                                    diferenciaLejosDe -= (abs(x[i][k] - x[j][k])) / (maxA - minA)

                                # Atributo discreto
                                else:
                                    if x[i][j] == x[j][k]:
                                        diferenciaLejosDe -= 1

                            else:
                                conteoFallidoLejosDe += 1

                                # Atributo continuo
                                if datos.infoAtributos[k][0]:
                                    # Atributo siendo similar es mas importante
                                    diferenciaFallidosLejosDe += abs(x[i][k] - x[j][k]) / (maxA - minA)

                                # Atributo discreto
                                else:
                                    if x[i][k] == x[j][k]:
                                        diferenciaFallidosLejosDe += 1

        proporcionCercanos = conteoCercaDe / float(conteoCercaDe + conteoFallidoCercaDe)
        proporcionFallidos = conteoFallidoCercaDe / float(conteoCercaDe + conteoFallidoCercaDe)

        # Aplicando un esquema de pesaje para balancear puntajes
        diferencia = diferenciaCercaDe * proporcionFallidos + diferenciaFallidosCercaDe * proporcionCercanos

        proporcionCercanos = conteoLejosDe / float(conteoLejosDe + conteoFallidoLejosDe)
        proporcionFallidos = conteoFallidoLejosDe / float(conteoLejosDe + conteoFallidoLejosDe)

        # Aplicando un esquema de pesaje para balancear puntajes
        diferencia += diferenciaLejosDe * proporcionFallidos + diferenciaFallidosCercaDe + proporcionCercanos

        listaPuntajes[k] += diferencia

    return listaPuntajes

def multiClaseMultiSURF(x, y, datos):
    """ Controla bucles principales del MultiSURF """

    listaPuntajes = []

    # Inicializando puntajes de los atributos en 0
    for i in range(datos.numAtributos):
        listaPuntajes.append(0)

    # Pre-calcular distancias entre todos los pares de identificadores
    # unicos dentro del conjunto de datos
    print("Precalculando matriz de distancias...")
    matrizDistancias = calcularMatrizDistancias(x, datos)
    print("Calculado.")

    # Solo para matrices multiclase
    mapaMulticlase = None

    if datos.fenotipoDiscreto and len(datos.listaFenotipos) > 2:
        mapaMulticlase = hacerMapaMultiClase(y, datos)

    D = []
    distanciasPromedio = []

    for i in range(datos.numInstanciasEntrenamiento):
        vectorDistancias = []
        vectorDistancias = obtenerDistanciasIndividuales(i, datos, matrizDistancias)
        distanciasPromedio.append(obtenerPromedio(vectorDistancias))
        desviacionEstandar = obtenerDesviacionEstandar(vectorDistancias, distanciasPromedio[i])
        D.append(desviacionEstandar / 2.0)

    # Haciendo bucle a traves de los atributos
    for k in range(datos.numAtributos):
        
        # Atributo continuo
        if datos.infoAtributos[k][0]:
            minA = datos.infoAtributos[k][1][0]
            maxA = datos.infoAtributos[k][1][1]

        conteoCercaDe = 0
        conteoFallidosCerca = 0
        conteoLejos = 0
        conteoFallidosLejos = 0

        # Inicializando el puntaje en 0
        diferenciaCerca = 0
        diferenciaFallidosCerca = 0
        diferenciaLejos = 0
        diferenciaFallidosLejos = 0

        almacenClasesCerca = hacerMapaParClase(mapaMulticlase)
        almacenClasesLejos = hacerMapaParClase(mapaMulticlase)

        for i in range(datos.numInstanciasEntrenamiento):
            for j in range(i, datos.numInstanciasEntrenamiento):
                if i != j and x[i][k] != datos.etiquetaDatosFaltantes and x[j][k] != datos.etiquetaDatosFaltantes:

                    ubicador = [i, j]

                    # Acceder a la mitad correcta de la tabla
                    ubicador = sorted(ubicador, reverse = True)

                    d = matrizDistancias[ubicador[0]][ubicador[1]]

                    # Cerca
                    if (d < distanciasPromedio[i] - D[i]):

                        if y[i] == y[j]:
                            conteoCercaDe += 1

                            if x[i][k] != x[j][k]:

                                # Atributo continuo
                                if datos.infoAtributos[k][0]:
                                    diferenciaCerca -= abs(x[i][k] - x[j][k]) / (maxA - minA)

                                # Atributo discreto
                                else:
                                    diferenciaCerca -= 1

                        else:
                            conteoFallidosCerca += 1
                            ubicador = [y[i], y[j]]
                            ubicador = sorted(ubicador, reverse = True)

                            textoTemp = str(ubicador[0]) + str(ubicador[1])
                            almacenClasesCerca[textoTemp][0] += 1

                            if x[i][k] != x[j][k]:
                                # Atributo continuo
                                if datos.infoAtributos[k][0]:
                                    almacenClasesCerca[textoTemp][1] += abs(x[i][k] - x[j][k]) / (maxA - minA)

                                # Atributo discreto
                                else:
                                    almacenClasesCerca[textoTemp][1] += 1

                    # Lejos
                    if (d > distanciasPromedio[i] + D[i]):

                        if y[i] == y[j]:
                            conteoLejos += 1

                            # Atributo continuo
                            if datos.infoAtributos[k][0]:
                                # Atributo siendo similar es mas importante
                                diferenciaLejos -= (1 - abs(x[i][k] - x[j][k])) / (maxA - minA)

                            # Atributo discreto
                            else:
                                if x[i][k] == x[j][k]:
                                    diferenciaLejos -= 1

                        else:
                            conteoFallidosLejos += 1
                            ubicador = [y[i], y[j]]
                            ubicador = sorted(ubicador, reverse = True)

                            textoTemp = str(ubicador[0]) + str(ubicador[1])
                            almacenClasesLejos[textoTemp][0] += 1

                            # Atributo continuo
                            if datos.infoAtributos[k][0]:
                                # Atributo siendo similar es mas importante
                                almacenClasesLejos[textoTemp][1] += abs(x[i][k] - x[j][k]) / (maxA - minA)

                            # Atributo discreto 
                            else:
                                if x[i][k] == x[j][k]:
                                    almacenClasesLejos[textoTemp][1] += 1

        # Cerca
        sumaFallidos = 0

        for each in almacenClasesCerca:
            sumaFallidos += almacenClasesCerca[each][0]

        # Corrigiendo para datos faltantes
        proporcionCorrectos = conteoCercaDe / float(conteoCercaDe + conteoFallidosCerca)
        proporcionFallidos = conteoFallidosCerca / float(conteoCercaDe + conteoFallidosCerca)

        for each in almacenClasesCerca:
            diferenciaFallidosCerca += (almacenClasesCerca[each][0] / float(sumaFallidos)) * almacenClasesCerca[each][1]

        diferenciaFallidosCerca = diferenciaFallidosCerca * float(len(almacenClasesCerca))

        diferencia = diferenciaFallidosCerca * proporcionCorrectos + diferenciaCerca * proporcionFallidos

        # Lejos
        sumaFallidos = 0

        for each in almacenClasesLejos:
            sumaFallidos += almacenClasesLejos[each][0]

        # Corrigiendo para datos faltantes
        proporcionCorretos = conteoLejos / float(conteoLejos + conteoFallidosLejos)
        proporcionFallidos = conteoFallidosLejos / float(conteoLejos + conteoFallidosLejos)

        for each in almacenClasesLejos:
            diferenciaFallidosLejos += (almacenClasesLejos[each][0] / float(sumaFallidos)) * almacenClasesLejos[each][1]

        diferenciaFallidosLejos = diferenciaFallidosLejos * float(len(almacenClasesLejos))

        diferencia += diferenciaFallidosLejos * proporcionCorrectos + diferenciaLejos * proporcionFallidos

        listaPuntajes[k] += diferencia

    return listaPuntajes

def obtenerDesviacionEstandar(vectorDistancias, promedio):
    suma = 0

    for i in range(len(vectorDistancias)):
        suma += (vectorDistancias[i] - promedio) ** 2

    suma = suma / float(len(vectorDistancias))

    return (suma ** 0.5)

def obtenerPromedio(vectorDistancias):
    suma = 0

    for i in range(len(vectorDistancias)):
        suma += vectorDistancias[i]

    return suma / float(len(vectorDistancias))

def obtenerDistanciasIndividuales(i, datos, matrizDistancias):
    D = []

    for j in range(datos.numInstanciasEntrenamiento):
        if (i != j):
            ubicador = [i, j]

            # Acceder a la mitad correcta de la tabla
            # (resultado de renundancia de la tabla eliminada)
            ubicador = sorted(ubicador, reverse = True)

            D.append(matrizDistancias[ubicador[0]][ubicador[1]])

    return D

def calcularMatrizDistancias(x, datos):
    # Hacer un contenedor vacio para la matriz de distancias
    # (Solo llenaremos la mitad no redundante de la matriz)
    matrizDistancias = []

    for i in range(datos.numInstanciasEntrenamiento):
        matrizDistancias.append([])

        for j in range(datos.numInstanciasEntrenamiento):
            matrizDistancias[i].append(None)

    for i in range(1, datos.numInstanciasEntrenamiento):
        for j in range(0, i):
            matrizDistancias[i][j] = calcularDistancia(x[i], x[j], datos)

    return matrizDistancias

def hacerMapaMultiClase(y, datos):
    # Encontrar numero de clases en el conjunto de datos y
    # guardarlos en el mapa

    mapaMultiClase = {}

    for i in range(datos.numInstanciasEntrenamiento):
        if (y[i] not in mapaMultiClase):
            mapaMultiClase[y[i]] = 0

        else:
            mapaMultiClase[y[i]] += 1

    # Para cada clase guardar su probabilidad de ocurrencia en el
    # conjunto de datos
    for each in datos.listaFenotipos:
        mapaMultiClase[each] = mapaMultiClase[each] / float(datos.numInstanciasEntrenamiento)

    return mapaMultiClase

def hacerMapaParClase(mapaMulticlase):
    """ Encuentra el numero de clases en el conjunto de datos y lo guarda en el mapa """

    mapaParClase = {}

    for each in mapaMulticlase:
        for otro in mapaMulticlase:
            if each != otro:
                ubicador = [each, otro]
                ubicador = sorted(ubicador, reverse = True)
                
                textoTemp = str(ubicador[0]) + str(ubicador[1])

                if (textoTemp not in mapaParClase):
                    mapaParClase[textoTemp] = [0, 0]

    return mapaParClase

def calcularDistancia(a, b, datos):
    """ Calcula la distancia entre dos instancias en el conjunto
    de datos. Maneja atributos discretos y continuos. Atributos
    continuos son acomodados al escalar la diferencia de distancia
    dentro del contexto del rango del atributo observado. Si un
    respectivo punto de datos esta faltando en cualquier instancia,
    se deja por fuera en los calculos de distancia"""

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
                # "Handling continuous attributes" - "Manejando atributos continuos"
                d += abs(float(a[i]) - float(b[i])) / float(limiteMax - limiteMin)
    
    return d