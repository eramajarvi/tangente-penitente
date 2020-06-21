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
        