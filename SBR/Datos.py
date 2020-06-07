# TANGENTE PENITENTE
# Datos.py

"""
Carga el conjunto de datos, caracteriza y almacena las 
características críticas de los conjuntos de datos (incluyendo 
los atributos discretos frente a los continuos y el fenotipo), 
maneja los datos que faltan y, finalmente, da formato a los 
datos para que puedan ser convenientemente utilizados por 
Tangente Penitente.
"""

import math
import random
import sys
from Constantes import *

class GestionDatos:
    def __init__(self, archivoEntrenamiento, archivoPrueba, listaInfo = None):
        # Fijar la semilla aleatoria si se especifica
        if cons.usarSemilla:
            random.seed(cons.semillaAleatoria)

        else:
            random.seed(None)

        if cons.datosOffline:
            # Inicializar variables globales
            self.numAtributos = None
            self.sonIDsIntancia = False
            self.refIDInstancia = None
            self.refFenotipo = None
            self.fenotipoDiscreto = True

            # Se guarda discreto (0) vs. continuo (1)
            self.infoAtributos = []
            # Se guarda valores del fenotipo discreto O para fenotipos continuos, valores max y min
            self.listaFenotipos = []
            # Se usa para aproximar la seleccion de la precision de un fenotipo aleatorio
            self.seleccionAleatoriaFenotipo = None
            self.rangoFenotipo = None
            self.DEFenotipo = None
            self.etiquetaDatosFaltantes = cons.etiquetaDatosFaltantes
            self.listaEndpointsFaltantes = []

            # Especifico para prueba / entrenamiento
            self.listaEncabezadoEntrenamiento = []
            self.listaEncabezadoPrueba = []
            self.numInstanciasEntrenamiento = None
            self.numInstanciasPrueba = None
            self.conteoEstadosPromedio = None

            self.conteoDiscreto = 0
            self.conteoContinuo = 0
            self.conteoClases = {}
            self.pesosPrediccionClases = {}

            # Detectar caracteristicas de los datos de entrenamiento
            print("-----------------------------------------------------")
            print("Ambiente: Formateando datos...")

            # Carga los datos crudos
            datosEntrenamientoCrudos = self.cargarDatos(archivoEntrenamiento + '.txt', True)

            # Detecta el numero de atributos, instancias y ubicaciones de referencia
            self.caracterizarConjuntoDatos(datosEntrenamientoCrudos)

            # Si no hay datos de prueba disponibles, el formateo recae
            # solamente en los datos de entrenamiento
            if cons.archivoPrueba == 'None':
                datosParaFormatear = datosEntrenamientoCrudos

            else:
                # Carga los datos crudos
                datosPruebaCrudos = self.cargarDatos(archivoPrueba + '.txt', False)
                # Se asegura que las caracteristicas principales
                # entre entre los datos de entrenamiento y de 
                # prueba sean las mismas
                self.compararConjuntoDatos(datosPruebaCrudos)

            # Determina si el fenotipo es discreto o continuo
            self.discriminarFenotipo(datosEntrenamientoCrudos)

            if self.fenotipoDiscreto:
                # Detecta el numero de identificadores unicos
                # del fenotipo
                self.discriminarClases(datosEntrenamientoCrudos)

            else:
                print("GestionDatos - Error: Tangente Penitente no puede manejar endpoints continuos")

            # Detecta si los atributos son discretos o continuos
            self.discriminarAtributos(datosEntrenamientoCrudos)
            # Detecta estados o rangos potenciales de los atributos
            self.caracterizarAtributos(datosEntrenamientoCrudos)

            # Limite Especificacion de Reglas (RSL/LER)
            if cons.RSL_Override > 0:
                self.limiteEspec = cons.RSL_Override

            else:
                # Calcula el LER
                print("GestionDatos: Estimando el limite de especificacion de los clasificadores...")

                i = 1
                combinacionesUnicas = math.pow(self.conteoEstadosPromedio, i)

                while combinacionesUnicas < self.numInstanciasEntrenamiento:
                    i += 1
                    combinacionesUnicas = math.pow(self.conteoEstadosPromedio, i)

                self.limiteEspec = i

                # No permitir nunca que el limite de especifiaccion sea mas grande
                # que el numero de atributos en el conjunto de datos
                if self.numAtributos < self.limiteEspec:
                    self.limiteEspec = self.numAtributos

            print("GestionDatos: Limite de Especificacion = " + str(self.limiteEspec))

            # Formatear y barajear el conjunto de datos
            if cons.archivoPrueba != 'None':
                # Se guarda el conjunto de datos de prueba formateado
                # usado en todo el algoritmo
                self.pruebaFormateados = self.formatearDatos(datosPruebaCrudos, False)
                
            # Se guarda el conjunto de datos de entrenamiento formateado
            # usado en todo el algoritmo
            self.entrenamientoFormateados = self.formatearDatos(datosEntrenamientoCrudos, True)

            print("-----------------------------------------------------")

        else:
            # Inicializar variables globales
            self.numAtributos = listaInfo[0]
            self.sonIDsIntancia = False
            self.refIDInstancia = None
            self.refFenotipo = None
            self.fenotipoDiscreto = listaInfo[1]
            self.infoAtributos = listaInfo[2] # Guarda discretos (0) vs continuos (1)
            self.listaFenotipos = listaInfo[3] # Guarda valores del fenotipo discreto O para fenotipos continuos, valores max y min
            self.rangoFenotipo = listaInfo[4]
            self.listaEncabezadoEntrenamiento = listaInfo[5]
            self.numInstanciasEntrenamiento = listaInfo[6]
            self.limiteEspec = 7

    def cargarDatos(self, archivoDatos, hacerEntrenamiento):
        """ Carga el archivo de datos. """

        print("GestionDatos: Cargando datos... " + str(archivoDatos))
        listaConjuntoDatos = []

        try:
            a = open(archivoDatos, 'rU')

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('No se pudo abrir', archivoDatos)

            raise

        else:
            if hacerEntrenamiento:
                self.listaEncabezadoEntrenamiento = a.readline().rstrip('\n').split(' ')

            else:
                self.listaEncabezadoPrueba = a.readline().rstrip('\n').split(' ')

            for linea in a:
                listaLineas = linea.strip('\n').split(' ')
                listaConjuntoDatos.append(listaLineas)

            a.close()

        return listaConjuntoDatos

    def caracterizarConjuntoDatos(self, datosEntrenamientoCrudos):
        """ Detecta parametros basicos del conjunto de datos"""

        # Detecta IDs de instancias y guarda su ubicacion si existen
        if cons.etiquetaIDInstancia in self.listaEncabezadoEntrenamiento:
            self.sonIDsIntancia = True
            self.refIDInstancia = self.listaEncabezadoEntrenamiento.index(cons.etiquetaIDInstancia)
            print("GestionDatos: Ubicacion de la columna de IDs de instancia = " + str(self.refIDInstancia))

            # Una columna para IDs de instancia y otra para el fenotipo
            self.numAtributos = len(self.listaEncabezadoEntrenamiento) - 2

        else:
            self.numAtributos = len(self.listaEncabezadoEntrenamiento) - 1

        if cons.etiquetaFenotipo in self.listaEncabezadoEntrenamiento:
            self.refFenotipo = self.listaEncabezadoEntrenamiento.index(cons.etiquetaFenotipo)

            print("GestionDatos: Ubicacion de la columna del fenotipo = " + str(self.refFenotipo))

        else:
            print("GesitonDatos - Error: No se encontro la columna del fenotipo. Revisa el conjunto de datos para asegurarse que exista una etiqueta de columna de fenotipo correcta.")

        if self.sonIDsIntancia:
            if self.refFenotipo > self.refIDInstancia:
                self.listaEncabezadoEntrenamiento.pop(self.refFenotipo)
                self.listaEncabezadoEntrenamiento.pop(self.refIDInstancia)

            else:
                self.listaEncabezadoEntrenamiento.pop(self.refIDInstancia)
                self.listaEncabezadoEntrenamiento.pop(self.refFenotipo)

        else:
            self.listaEncabezadoEntrenamiento.pop(self.refFenotipo)

        self.numInstanciasEntrenamiento = len(datosEntrenamientoCrudos)

        print("GestionDatos: Numero de atributos = " + str(self.numAtributos))
        print("GestionDatos: Numero de instancias = " + str(self.numInstanciasEntrenamiento))

    def discriminarFenotipo(self, datosCrudos):
        """ Determina si el fenotipo es discreto o continuo """

        print("GestionDatos: Analizando fenotipo...")
        inst = 0
        diccionarioClases = {}

        # Revisa que discrimina entre atirbutos discretos y continuos
        while len(list(diccionarioClases.keys())) <= cons.limiteAtributoDiscreto and inst < self.numInstanciasEntrenamiento:
            objetivo = datosCrudos[inst][self.refFenotipo]

            # Revisa si este estado del atributo se ha visto antes
            if objetivo in list(diccionarioClases.keys()):
                diccionarioClases[objetivo] += 1

            elif objetivo == cons.etiquetaDatosFaltantes:
                self.listaEndpointsFaltantes.append(inst)

            else:
                diccionarioClases[objetivo] = 1

            inst += 1

        if len(list(diccionarioClases.keys())) > cons.limiteAtributoDiscreto:
            self.fenotipoDiscreto = False
            self.listaFenotipos = [float(objetivo), float(objetivo)]
            print("GestionDatos: Fenotipo detectado como continuo.")

        else:
            print("GestionDatos: Fenotipo detectado como discreto")    

    def discriminarClases(self, datosCrudos):
        pass

    def compararConjuntoDatos(self, datosPruebaCrudos):
        pass

    def discriminarAtributos(self, datosCrudos):
        pass

    def caracterizarAtributos(self, datosCrudos):
        pass

    def calcularDE(self, listaFenotipos):
        pass

    def formatearDatos(self, datosCrudos, entrenamiento):
        pass

    def guardarDatosTurfTemp(self):
        pass

    def regresarDatosCompletos(self):
        pass

    def gestionDatosTurf(self, puntajesFiltro, porcentajeTurf):
        pass

    def hacerConjuntoDatosFiltrado(self, atributosEnDatos, nombreArchivo, puntajesFiltro):
        pass