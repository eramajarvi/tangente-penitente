# TANGENTE PENITENTE
# Salida.py

"""
Este módulo contiene los métodos para generar los diferentes archivos de salida generados por Tangente Penitente. Estos archivos se generan en 
cada punto de control de aprendizaje, y en la última iteración. Estos incluyen: 
    writePopStats: Resumen de las estadísticas de población
    writePop: Produce una instantánea de toda la población de reglas, incluyendo las condiciones de los clasificadores, las clases y los parámetros.
    attCo_Ocurrence: Calcula y produce puntuaciones de co-ocurrencia para cada par de atributos en el conjunto de datos.
"""

from Constantes import *
from SA import *
import copy

class GestorSalida:
    def escribirEstadisticasPoblacion(self, archivoSalida, evalEntrenamiento, evalPrueba, iterExploracion, pob, correcto):
        """ Crea un archivo de texto de salida que incluye todos los
        parametros usados en la ejecucion, asi como tambien todos los
        estadisticos de evaluacion. """

        if cons.salidaResumen:
            try:
                # Escribir las estadisticas de ejecucion de la poblacion
                salidaEstadisticasPoblacion = open(archivoSalida + '_' + str(iterExploracion) + '_EstadisticasPoblacion.txt', 'w')

            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('No se pudo abrir', archivoSalida + '_' + str(iterExploracion) + '_EstadisticasPoblacion.txt')
                raise

            else:
                print("Escribiendo archivo de resumen de las estadisticas de la poblacion...")

            # Evaluacion de la poblacion
            salidaEstadisticasPoblacion.write("Estadisticas de rendimiento: --------- \n")
            salidaEstadisticasPoblacion.write("Precision de entrenamiento\tPrecision de prueba\tCubrimiento de entrenamiento\tCubrimiento de prueba")

            if cons.archivoPrueba != 'None':
                salidaEstadisticasPoblacion.write(str(evalEntrenamiento[0]) + "\t")
                salidaEstadisticasPoblacion.write(str(evalPrueba[0]) + "\t")
                salidaEstadisticasPoblacion.write(str(evalEntrenamiento[1]) + "\t")
                salidaEstadisticasPoblacion.write(str(evalPrueba[1]) + "\n\n")

            elif cons.archivoEntrenamiento != 'None':
                salidaEstadisticasPoblacion.write(str(evalEntrenamiento[0]) + "\t")
                salidaEstadisticasPoblacion.write("NA\t")
                salidaEstadisticasPoblacion.write(str(evalEntrenamiento[1]) + "\t")
                salidaEstadisticasPoblacion.write("NA\n\n")

            else:
                salidaEstadisticasPoblacion.write("NA\t")
                salidaEstadisticasPoblacion.write("NA\t")
                salidaEstadisticasPoblacion.write("NA\t")
                salidaEstadisticasPoblacion.write("NA\n\n")

            salidaEstadisticasPoblacion.write("Caracterizacion de la poblacion: --------- \n")
            salidaEstadisticasPoblacion.write("TamanoPobMacro\tTamanoPobMicro\tGeneralidad\n")
            salidaEstadisticasPoblacion.write(str(len(pob.tamanoConjunto)) + "\t" + str(pob.tTamanoPobMicro) + "\t" + str(pob.generalidadPromedio) + "\n\n")

            salidaEstadisticasPoblacion.write("Suma Especificacion: --------- \n")
            listaEncabezados = cons.amb.datosFormateados.listaEncabezadosEntrenamiento

            for i in range(len(listaEncabezados)):
                if i < len(listaEncabezados) - 1:
                    salidaEstadisticasPoblacion.write(str(listaEncabezados[i]) + "\t")

                else:
                    salidaEstadisticasPoblacion.write(str(listaEncabezados[i]) + "\n")

            # Imprime la suma de especificacion para cada atributo
            for i in range(len(pob.listaEspecAtributo)):
                if i < len(pob.listaEspecAtributo) - 1:
                    salidaEstadisticasPoblacion.write(str(pob.listaEspecAtributo[i]) + "\t")

                else:
                    salidaEstadisticasPoblacion.write(str(pob.listaEspecAtributo[i]) + "\n")

            salidaEstadisticasPoblacion.write("\nSumaPrecision: --------- \n")

            for i in range(len(listaEncabezados)):
                if i < len(listaEncabezados) -  1:
                    salidaEstadisticasPoblacion.write(str(listaEncabezados[i]) + "\t")

                else:
                    salidaEstadisticasPoblacion.write(str(listaEncabezados[i]) + "\n")

            # Imprime el conteo de especificacion de precision balanceado
            # para cada atributo
            for i in range(len(pob.listaAccAtributo)):
                if i < len(pob.listaAccAtributo) - 1:
                    salidaEstadisticasPoblacion.write(str(pob.listaAccAtributo[i]) + "\t")

                else:
                    salidaEstadisticasPoblacion.write(str(pob.listaAccAtributo[i]) + "\n")

            # Cuando es solo CR, no hay suma global de seguimiento de atributos
            if cons.soloCR:
                salidaEstadisticasPoblacion.write("\nSumaGlobalSeguimientoAtributos: --------- SOLO Compactacion de Reglas, no se cargo el Seguimiento de Atributos --------- \n")

                for i in range(len(listaEncabezados)):
                    if i < len(listaEncabezados) - 1:
                        salidaEstadisticasPoblacion.write(str(listaEncabezados[i]) + "\t")

                    else:
                        salidaEstadisticasPoblacion.write(str(listaEncabezados[i]) + "\n")

                for i in range(len(listaEncabezados)):
                    if i < len(listaEncabezados) - 1:
                        salidaEstadisticasPoblacion.write(str(0.0) + "\t")

                    else:
                        salidaEstadisticasPoblacion.write(str(0.0) + "\n")

            elif cons.hacerSeguimientoAtributos:
                salidaEstadisticasPoblacion.write("\nSumaGlobalSeguimientoAtributos: --------- \n")

                for i in range(len(listaEncabezados)):
                    if i < len(listaEncabezados) - 1:
                        salidaEstadisticasPoblacion.write(str(listaEncabezados[i]) + "\t")

                    else:
                        salidaEstadisticasPoblacion.write(str(listaEncabezados[i]) + "\n")

                sumaGlobalSA = cons.SA.sumaSeguimientoAtributosGlobal()

                for i in range(len(sumaGlobalSA)):
                    if i < len(sumaGlobalSA) - 1:
                        salidaEstadisticasPoblacion.write(str(sumaGlobalSA[i]) + "\t")

                    else:
                        salidaEstadisticasPoblacion.write(str(sumaGlobalSA[i]) + "\n")

            else:
                salidaEstadisticasPoblacion.write("\nSumaGlobalSeguimientoAtributos: --------- No se aplico seguimiento --------- \n")

                for i in range(len(listaEncabezados)):
                    if i < len(listaEncabezados) - 1:
                        salidaEstadisticasPoblacion.write(str(listaEncabezados[i]) + "\t")

                    else:
                        salidaEstadisticasPoblacion.write(str(listaEncabezados[i]) + "\n")
                
                for i in range(len(listaEncabezados)):
                    if i < len(listaEncabezados) - 1:
                        salidaEstadisticasPoblacion.write(str(0.0) + "\t")

                    else:
                        salidaEstadisticasPoblacion.write(str(0.0) + "\n")

            # Seguimiento del tiempo
            salidaEstadisticasPoblacion.write("\nTiempo de ejecucion (en minutos): --------- \n")
            salidaEstadisticasPoblacion.write(cons.cronometro.reportarTiempos())
            salidaEstadisticasPoblacion.write("\nGuardadoSeguimientoCorrectos: --------- \n")

            for i in range(len(correcto)):
                salidaEstadisticasPoblacion.write(str(correcto[i]) + "\t")

            salidaEstadisticasPoblacion.close()

        else:
            pass

    def escribirPob(self, archivoSalida, iterExploracion, pob):
        """ Escribe un archivo de texto especificando la poblacion 
        de reglas evolucionada, incluyendo condiciones, fenotipos
        y todos los parametros de las reglas"""

        if cons.salidaPoblacion:
            try:
                salidaPoblacion = open(archivoSalida + '_' + str(iterExploracion) + '_PoblacionReglas.txt', 'w')

            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('No se pudo abrir', archivoSalida + '_' + str(iterExploracion) + '_PoblacionReglas.txt')
                raise

            else:
                print("Escribiendo poblacion como archivo de texto...")

            salidaPoblacion.write("Especificado\tCondicion\tFenotipo\tAptitud\tNumerosidad\tTamanoPromConjuntoCoinc\tEstampaTiempoAG\tEstampaTiempoInic\tEspecificacion\tProbEliminacion\tConteoCorrectos\tCubrimientoCorrecto\tCubrimientoCoinc\tEpocaCompletada\n")

            # Escribir cada clasificador
            for cl in pob.conjuntoPob:
                salidaPoblacion.write(str(cl.imprimirClasificador()))

            salidaPoblacion.close()

        else:
            pass

    def coocurrenciaAtt(self, archivoSalida, iterExploracion, pob):
        """ Calcula la co-ocurrencia de los atributos en toda
        la poblacion de reglas. """

        if cons.salidaAttCoOccur:
            print("Calculando puntajes de co-ocurrencia de los atributos... ")
            enlaceDatos = cons.amb.datosFormateados
            dim = enlaceDatos.numAtributos
            atributosMax = 50
            listaAtributos = []

            # Identifica los atributos para evaluacion de co-ocurrencia
            if dim <= atributosMax:
                for i in range(0, dim):
                    listaAtributos.append(i)

            else:
                listaTemp = copy.deepcopy(pob.listaEspecAtributo)
                listaTemp = sorted(listaTemp, reverse = True)

                valorMax = listaTemp[atributosMax]
                sobrecarga = []

                for i in range(0, dim):
                    if pob.listaEspecAtributo[i] >= valorMax:
                        listaAtributos.append(i)

                        if pob.listaEspecAtributo[i] == valorMax:
                            sobrecarga.append(i)

                while len(listaAtributos) > atributosMax:
                    objetivo = random.choice(sobrecarga)
                    listaAtributos.remove(objetivo)
                    sobrecarga.remove(objetivo)

            # Evaluacion de la co-ocurrencia
            listaCombo = []
            # Atrib1, Atrib2, Especificacion, EspecificacionPrecisionBalanceada
            listaCast = [None, None, 0, 0]
            conteo = 0
            dim = enlaceDatos.numAtributos

            # Especificar todos los pares de atributos
            for i in range(0, len(listaAtributos) - 1):
                for j in range(i + 1, len(listaAtributos)):
                    listaCombo.append(copy.deepcopy(listaCast))
                    listaCombo[conteo][0] = enlaceDatos.listaEncabezadosEntrenamiento[listaAtributos[i]]
                    listaCombo[conteo][0] = enlaceDatos.listaEncabezadosEntrenamiento[listaAtributos[j]]
                    conteo += 1

            for cl in pob.conjuntoPob:
                conteo = 0

                for i in range(len(listaAtributos) - 1):
                    for j in range(i + 1, len(listaAtributos)):
                        if listaAtributos[i] in cl.listaEspecAtributo and listaAtributos[j] in cl.listaEspecAtributo:
                            listaCombo[conteo][2] += cl.numerosidad
                            listaCombo[conteo][3] += cl.numerosidad * cl.precision

                        conteo += 1

            listaTuplas = []

            for i in listaCombo:
                listaTuplas.append((i[0], i[1], i[2], i[3]))

            listaComboOrganizada = sorted(listaTuplas, key = lambda test: test[3], reverse = True)

            print("Escribiendo puntajes de co-ocurrencia como archivo de texto...")

            try:
                a = open(archivoSalida + '_' + str(iterExploracion) + '_CO.txt', 'w')

            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('No se pudo abrir', archivoSalida + '_' + str(iterExploracion) + '_CO.txt')

            else:
                for i in range(len(listaComboOrganizada)):
                    for j in range(len(listaComboOrganizada[0])):
                        if j < len(listaComboOrganizada[0]) - 1:
                            a.write(str(listaComboOrganizada[i][j]) + '\t')

                        else:
                            a.write(str(listaComboOrganizada[i][j]) + '\n')

                a.close()

        else:
            pass

    def guardarSeguimiento(self, iterExploracion, archivoSalida):
        """" Imprime los puntajes del seguimiento de atributos en
        un archivo de texto"""

        if cons.hacerSeguimientoAtributos:
            try:
                a = open(archivoSalida + '_' + str(iterExploracion + 1) + '_SeguimientoAtributos.txt', 'w')

            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('No se pudo abrir', archivoSalida + '_' + str(iterExploracion + 1) + '_SeguimientoAtributos.txt')
                raise

            else:
                print("Escribiendo seguimiento de atributos como archivo de texto...")

            sumasSeguimiento = cons.SA.sumaPrecisionAtributos

            a.write(str(cons.etiquetaIDInstancia) + '\t')

            for att in cons.amb.datosFormateados.listaEncabezadosEntrenamiento:
                a.write(str(att) + '\t')

            a.write(str(cons.etiquetaFenotipo) + '\n')

            for i in range(len(sumasSeguimiento)):
                listaSeguimiento = sumasSeguimiento[i]

                a.write(str(cons.amb.datosFormateados.entrenamientoFormateado[i][2]) + '\t')

                for att in listaSeguimiento:
                    a.write(str(att) + '\t')

                a.write(str(cons.amb.datosFormateados.entrenamientoFormateado[i][1]) + '\n')

            a.close()
        