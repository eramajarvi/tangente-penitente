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
                            pass

                        # Endpoint continuo
                        else:
                            pass

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