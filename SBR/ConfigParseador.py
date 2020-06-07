# TANGENTE PENITENTE
# ConfigParseador.py

"""
Maneja el archivo de configuración cargando, analizando y 
pasando sus valores a Constantes. También incluye un método para 
generar conjuntos de datos para la validación cruzada.
"""

from Constantes import *
import os
import copy
import random

class ConfigParseador:
    def __init__(self, nombreArchivo):
        
        # Siempre se usa la misma semilla aqui, de tal forma que
        # los mismos conjuntos de datos de VC seran generados si se
        # ejecuta de nuevo
        random.seed(1)

        self.carComentario = '#'
        self.carParametro = '='
        
        # Parsea el archivo de configuracion y obtiene todos los
        # parametros
        self.parametros = self.parsearConfiguracion(nombreArchivo)
        
        # Construye la clase Constantes usando los parametros del
        # archivo de configuracion
        cons.fijarConstantes(self.parametros)

        if cons.validacionCruzadaInterna == 0 or cons.validacionCruzadaInterna == 1:
            pass
        
        # Hacer VC interna
        else:
            self.PartVC()

    def parsearConfiguracion(self, nombreArchivo):
        """ Parsear el archivo de configuracion """
        parametros = {}

        try:
            a = open(nombreArchivo, 'rU')

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('No se pudo abrir', nombreArchivo)
            raise
            
        else:
            for linea in a:
                # Primero eliminar los comentarios:
                if self.carComentario in linea:
                    # Separar el caracter de comentarios, guardar
                    # solo la parte de despues
                    linea, comentario = linea.split(self.carComentario, 1)

                # Segundo encontrar lineas con un parametro = valor
                if self.carParametro in linea:
                    # Separar el caracter de parametro:
                    parametro, valor = linea.split(self.carParametro, 1)

                    # Eliminar espacios:
                    parametro = parametro.strip()
                    valor = valor.strip()

                    # Guardar el diccionario:
                    parametros[parametro] = valor

            a.close()

        return parametros

    def PartVC(self):
        """ Dado un conjunto de datos, partCV lo particiona 
        aleatoriamente en X particiones aleatorias balanceadas
        para validacion cruzada que son guardadas en el archivo
        especificado.
        #PARAM rutaArchivo - especifica la ruta y el nombre de
        los nuevos conjuntos de datos"""

        numParticiones = cons.validacionCruzadaInterna
        nombreCarpeta = copy.deepcopy(cons.archivoEntrenamiento)
        nombreArchivo = nombreCarpeta.split('\\')
        nombreArchivo = nombreArchivo[len(nombreArchivo) - 1]
        rutaArchivo = nombreCarpeta + '\\' + nombreArchivo

        # Hacer carpeta para conjuntos de datos para VC
        if not os.path.exists(nombreCarpeta):
            os.mkdir(nombreCarpeta)

        # Abrir el archivo de datos especificado
        try:
            a = open(cons.archivoEntrenamiento + '.txt', 'rU')

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('No se pudo abrir', cons.archivoEntrenamiento + '.txt')
            raise

        else:
            listaConjuntoDatos = []
            # Remover la primera fila (encabezados)
            listaEncabezados = a.readline().rstrip('\n').split('\t')

            for linea in a:
                listaLineas = linea.strip('\n').split('\t')
                listaConjuntoDatos.append(listaLineas)

            a.close()

        longitudDatos = len(listaConjuntoDatos)

        # Caracterizar el fenotipo 
        fenotipoDiscreto = True

        if cons.etiquetaFenotipo in listaEncabezados:
            refFenotipo = listaEncabezados.index(cons.etiquetaFenotipo)

        else:
            print('ConfigParseador - Error: No se encuentra la etiqueta del fenotipo.')

            inst = 0
            diccionarioClases = {}

            # Revisa que discriminar entre atributos discretos y
            # continuos
            while len(list(diccionarioClases.keys())) <+ cons.limiteAtributoDiscreto and inst < longitudDatos:
                objetivo = listaConjuntoDatos[inst][refFenotipo]

                # Revisa si ya se ha visto antes este estado de
                # atributo
                if objetivo in list(diccionarioClases.keys()):
                    diccionarioClases[object] += 1

                else:
                    diccionarioClases[objetivo] = 1

                inst += 1

            if (len(list(diccionarioClases.keys))) > cons.limiteAtributoDiscreto:
                fenotipoDiscreto = False

            else:
                pass

            # Guarda todas las particiones
            listaVC = []

            for x in range(numParticiones):
                listaVC.append([])

            if fenotipoDiscreto:
                listaMaestra = []
                llavesClase = list(diccionarioClases.keys())

                for i in range(len(llavesClase)):
                    listaMaestra.append([])

                for i in listaConjuntoDatos:
                    noEncontrado = True
                    j = 0

                    while noEncontrado:
                        if i[refFenotipo] == llavesClase[j]:
                            listaMaestra[j].append(i)
                            noEncontrado = False
                        
                        j += 1

                # Aleatoriza instancias de clase antes de particionar
                from random import shuffle

                for i in range(len(llavesClase)):
                    shuffle(listaMaestra[i])

                for claseActual in listaMaestra:
                    partActual = 0
                    contador = 0

                    for x in claseActual:
                        listaVC[partActual].append(x)
                        contador += 1
                        partActual = contador % numParticiones

                self.hacerParticiones(listaVC, numParticiones, rutaArchivo, listaEncabezados)

            # Atributo continuo
            else:
                from random import shuffle
                shuffle(listaConjuntoDatos)

                partActual = 0
                contador = 0

                for x in listaConjuntoDatos:
                    listaVC[partActual].append(x)
                    contador += 1
                    partActual = contador % numParticiones

                self.hacerParticiones(listaVC, numParticiones, rutaArchivo, listaEncabezados)

    def hacerParticiones(self, listaVC, numParticiones, rutaArchivo, listaEncabezados):
        # Construye archivos de VC
        for part in range(numParticiones):
            if not os.path.exists(rutaArchivo + '_VC_' + str(part) + '_Entrenamiento.txt') or not os.path.exists(rutaArchivo + '_VC_' + str(part) + '_Prueba.txt'):
                print("Haciendo nuevos archivos de VC: " + rutaArchivo + '_VC_' + str(part))
                archivoEntrenamiento = open(rutaArchivo + '_VC_' + str(part) + '_Entrenamiento.txt', 'w')
                archivoPrueba = open(rutaArchivo + '_VC_' + str(part) + '_Prueba.txt', 'w')

                for i in range(len(listaEncabezados)):
                    if i < len(listaEncabezados) - 1:
                        archivoPrueba.write(listaEncabezados[i] + "\t")
                        archivoEntrenamiento.write(listaEncabezados[i] + "\t")

                    else:
                        archivoPrueba.write(listaEncabezados[i] + "\n")
                        archivoEntrenamiento.write(listaEncabezados[i] + "\n")

                listaPrueba = listaVC[part]
                listaEntrenamiento = []
                listaTemp = []

                for x in range(numParticiones):
                    listaTemp.append(x)

                listaTemp.pop(part)

                # Para cada iteracion de aprendizaje
                for v in listaTemp:
                    listaEntrenamiento.extend(listaVC[v])

                # Escribir a un archivo de Prueba
                for i in listaPrueba:
                    stringTemp = ''

                    for punto in range(len(i)):
                        if punto < len(i) - 1:
                            stringTemp = stringTemp + str(i[punto]) + "\t"

                        else:
                            stringTemp = stringTemp + str(i[punto]) + "\n"

                    archivoPrueba.write(stringTemp)

                # Escribir a un archivo de Entrenamiento
                for i in listaEntrenamiento:
                    stringTemp = ''

                    for punto in range(len(i)):
                        if punto < len(i) - 1:
                            stringTemp = stringTemp + str(i[punto]) + "\t"

                        else:
                            stringTemp = stringTemp + str(i[punto]) + "\n"

                    archivoEntrenamiento.write(stringTemp)

                archivoEntrenamiento.close()
                archivoPrueba.close()