"""
TANGENTE PENITENTE
Nombre: tp_Salida.py
Descripcion: Este módulo contiene los métodos para generar los diferentes archivos 
             de salida generados por Tangente Penitente. Estos archivos se generan 
             en cada punto de control de aprendizaje, y en la última iteración. 
             Estos incluyen: 
             writePopStats: Resumen de las estadísticas de población
             writePop: Produce una instantánea de toda la población de reglas, incluyendo las condiciones de los clasificadores, las clases y los parámetros.
             attCo_Ocurrence: Calcula y produce puntuaciones de co-ocurrencia para cada par de atributos en el conjunto de datos.
"""

# Importar modulos requeridos
from tp_Constantes import *
from tp_SA import *
import copy
#

class AdminSalida:     

    def escribirEstadisticasPob(self, archivoSalida, evailEntrena, evalPrueba, exploreIter, pob, correcto):
        """ Hace un archivo de texto de salida que incluye todos los ajustes de los parámetros utilizados en la ejecución, así como todas las estadísticas de evaluación, incluyendo la salida del seguimiento de tiempo. """

        if cons.salidaResumen:
            try:  
                salidaEstadsPob = open(archivoSalida + '_' + str(exploreIter) + '_EstadisticasPob.txt','w') # Saca las estadisticas de ejecucion de la poblacion

            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('No se pudo abrir', archivoSalida + '_' + str(exploreIter) + '_EstadisticasPob.txt')
                raise

            else:
                print("Escribiendo archivo de resumen estadistico de la poblacion")
            
            #Evaluacion de la poblacion
            salidaEstadsPob.write("Estadisticas de rendimiento: \n")
            salidaEstadsPob.write("Precision entrnamiento\tPrecision prueba\tCubrimiento entrenamiento\tCubrimiento de prueba\n")
            
            if cons.archivoPrueba != 'None':
                salidaEstadsPob.write(str(evailEntrena[0])+"\t")
                salidaEstadsPob.write(str(evalPrueba[0])+"\t")
                salidaEstadsPob.write(str(evailEntrena[1]) +"\t")
                salidaEstadsPob.write(str(evalPrueba[1])+"\n\n")

            elif cons.archivoEntrenamiento != 'None':
                salidaEstadsPob.write(str(evailEntrena[0])+"\t")
                salidaEstadsPob.write("NA\t")
                salidaEstadsPob.write(str(evailEntrena[1]) +"\t")
                salidaEstadsPob.write("NA\n\n")

            else:
                salidaEstadsPob.write("NA\t")
                salidaEstadsPob.write("NA\t")
                salidaEstadsPob.write("NA\t")
                salidaEstadsPob.write("NA\n\n")
            
            salidaEstadsPob.write("Caracterizacion de la poblacion: \n")  
            salidaEstadsPob.write("TamanoMacroPob\tTamanoMicroPob\tGeneralidad\n") 
            salidaEstadsPob.write(str(len(pob.ConjuntoPob)) + "\t" + str(pob.tamanoMicroPob) + "\t" + str(pob.generalidadProm)+"\n\n")
    
            salidaEstadsPob.write("Suma de especifidad: \n")       
            listaEncabezad = cons.amb.datosFormateados.listaEncabezadoEntrenamiento # Preserva el orden del conjunto de datos original
    
            for i in range(len(listaEncabezad)): 
                if i < len(listaEncabezad)-1:
                    salidaEstadsPob.write(str(listaEncabezad[i])+"\t")

                else:
                    salidaEstadsPob.write(str(listaEncabezad[i])+"\n")
                    
            # Imprime la suma de especifidad para cada atributo
            for i in range(len(pob.listaEspecAtributo)):
                if i < len(pob.listaEspecAtributo) - 1:
                    salidaEstadsPob.write(str(pob.listaEspecAtributo[i]) + "\t")

                else:
                    salidaEstadsPob.write(str(pob.listaEspecAtributo[i]) + "\n")  
                          
            salidaEstadsPob.write("\nSuma precision: \n")

            for i in range(len(listaEncabezad)): 
                if i < len(listaEncabezad) - 1:
                    salidaEstadsPob.write(str(listaEncabezad[i]) + "\t")
                     
                else:
                    salidaEstadsPob.write(str(listaEncabezad[i]) + "\n")
                    
            # Imprime el recuento de la especificación ponderada de precisión para cada atributo
            for i in range(len(pob.listaPrecisionAtributo)):
                if i < len(pob.listaPrecisionAtributo) - 1:
                    salidaEstadsPob.write(str(pob.listaPrecisionAtributo[i]) + "\t")

                else:
                    salidaEstadsPob.write(str(pob.listaPrecisionAtributo[i]) + "\n")    
                    
            if cons.soloCR: # Cuando es soloCR, no hay AttributeTrackingGlobalSums
                salidaEstadsPob.write("\nSumasGlobalesSeguimientoAtributos: --Solo compactacion de reglas, Seguimiento de Atributos no se carga --\n")

                for i in range(len(listaEncabezad)): 
                    if i < len(listaEncabezad)-1:
                        salidaEstadsPob.write(str(listaEncabezad[i])+"\t")

                    else:
                        salidaEstadsPob.write(str(listaEncabezad[i])+"\n")

                for i in range(len(listaEncabezad)): 
                    if i < len(listaEncabezad)-1:
                        salidaEstadsPob.write(str(0.0)+"\t")

                    else:
                        salidaEstadsPob.write(str(0.0)+"\n")

            elif cons.hacerSeguimientoAtributos:
                salidaEstadsPob.write("\nSumasGlobalesSeguimientoAtributos: -----------------")
                for i in range(len(listaEncabezad)): 
                    if i < len(listaEncabezad)-1:
                        salidaEstadsPob.write(str(listaEncabezad[i])+"\t")

                    else:
                        salidaEstadsPob.write(str(listaEncabezad[i])+"\n")
                        
                sumaGlobalSeguimientoAtt = cons.AT.sumaGlobalSeguimientoAtt()        
                for i in range(len(sumaGlobalSeguimientoAtt)):
                    if i < len(sumaGlobalSeguimientoAtt)-1:
                        salidaEstadsPob.write(str(sumaGlobalSeguimientoAtt[i]) + "\t")

                    else:
                        salidaEstadsPob.write(str(sumaGlobalSeguimientoAtt[i]) + "\n")

            else:
                salidaEstadsPob.write("\nSumasGlobalesSeguimientoAtributos:----Seguimiento no aplicado---\n")
                for i in range(len(listaEncabezad)): 
                    if i < len(listaEncabezad)-1:
                        salidaEstadsPob.write(str(listaEncabezad[i]) + "\t")

                    else:
                        salidaEstadsPob.write(str(listaEncabezad[i]) + "\n")

                for i in range(len(listaEncabezad)): 
                    if i < len(listaEncabezad)-1:
                        salidaEstadsPob.write(str(0.0) + "\t")

                    else:
                        salidaEstadsPob.write(str(0.0) + "\n")
                      
            # Seguimiento tiempo     
            salidaEstadsPob.write("\nTiempo de ejecucion (en minutos):---\n") 
            salidaEstadsPob.write(cons.cronometro.reportarTiempos())
            salidaEstadsPob.write("\nRastreosCorrectosGuardados:---\n")

            for i in range(len(correcto)):
                salidaEstadsPob.write(str(correcto[i])+"\t")
                    
            salidaEstadsPob.close()

        else:
            pass
        
    
    def escribirPob(self, outFile, exploreIter, pob):
        """ Escribe un archivo de texto especificando la poblacion de reglas evolucionada, incluyendo condicion, fenotipos y todos los parametros de las reglas"""
        
        if cons.salidaPoblacion:
            try:  
                salidaPobReglas = open(outFile + '_'+ str(exploreIter)+'_PobReglas.txt','w') # Escribe archivo de texto de la poblacion de reglas y sus respectivas estadisticas

            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('No se pudo abrir', outFile + '_'+ str(exploreIter)+'_PobReglas.txt')
                raise 

            else:
                print("Escribiendo poblacion como archivo de datos...")
                
            salidaPobReglas.write("Especificado\tCondicion\tFenotipo\tAptitud\tPrecision\tNumerosidad\tTamanoPromConjCoincid\tEstampaTiempoAG\tEstampaTiempoInic\tEspecifidad\tProbEliminacion\tConteoCorrectos\tConteoCoincidencias\tCubrimCorrec\tCubrimCoinc\tEpocaCompleta\n")
    
            #Escribir cada clasificador 
            for cl in pob.ConjuntoPob:
                salidaPobReglas.write(str(cl.imprimirClasificador())) 
                
            salidaPobReglas.close() 

        else:
            pass

  
    def occurenciaAttCo(self, archivoSalida, exploreIter, pop):
        """ Calcula la co-ocurrencia de atributos por pares a través de todas las reglas de la población"""

        if cons.salidaAttCoOccur:
            print("Calculando puntajes de co-ocurrencia de atributos...")
            vinculoDatos = cons.amb.datosFormateados
            dim = vinculoDatos.numAtributos
            maxAtributos = 50  # Prueba 10
            attLista = []

            #-------------------------------------------------------
            # IDENTIFICAR ATRIBUTOS PARA EVALUACION DE CO-OCURRENCIA
            #-------------------------------------------------------
            if dim <= maxAtributos:
                for i in range(0,dim):
                    attLista.append(i)
            else:
                tempList = copy.deepcopy(pop.listaEspecAtributo)
                tempList = sorted(tempList,reverse=True)
                maxVal = tempList[maxAtributos]
                overflow = []
                for i in range(0,dim):
                    if pop.listaEspecAtributo[i] >= maxVal: #get roughly the top 50 specified attributes. (may grab some extras, depending on 
                        attLista.append(i)
                        if pop.listaEspecAtributo[i] == maxVal:
                            overflow.append(i)
                while len(attLista) > maxAtributos:
                    target = random.choice(overflow)
                    attLista.remove(target)
                    overflow.remove(target)
                    #print(attList)
                    
            #-------------------------------------------------------
            # CO-OCCRRENCE EVALUATION
            #-------------------------------------------------------   
            comboList = []
            castList = [None,None,0,0] #att1, att2, Specificity, Accuracy Weighted Specificity
            count = 0
            dim = vinculoDatos.numAttributes
            #Specify all attribute pairs.
            for i in range(0, len(attLista)-1):
                for j in range(i+1,len(attLista)):
                    comboList.append(copy.deepcopy(castList))
                    comboList[count][0] = vinculoDatos.trainHeaderList[attLista[i]]
                    comboList[count][1] = vinculoDatos.trainHeaderList[attLista[j]]   
                    count += 1
    
            for cl in pop.popSet:
                count = 0
                for i in range(len(attLista)-1):
                    for j in range(i+1,len(attLista)):
                        if attLista[i] in cl.specifiedAttList and attLista[j] in cl.specifiedAttList:
                            comboList[count][2] += cl.numerosity
                            comboList[count][3] += cl.numerosity * cl.accuracy
                        count += 1
            
            tupleList = []
            for i in comboList:
                tupleList.append((i[0],i[1],i[2],i[3]))
            sortedComboList = sorted(tupleList,key=lambda test: test[3], reverse=True)
            print("Writing Attribute Co-occurence scores as data file...")
            try:
                f = open(archivoSalida + '_'+ str(exploreIter)+ '_CO.txt', 'w')
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open', archivoSalida + '_'+ str(exploreIter)+ '_CO.txt')
                raise 
            else:
                for i in range(len(sortedComboList)):
                    for j in range(len(sortedComboList[0])): #att1, att2, count, AWcount
                        if j < len(sortedComboList[0])-1:
                            f.write(str(sortedComboList[i][j])+'\t')
                        else:
                            f.write(str(sortedComboList[i][j])+'\n')
                f.close()
        else:
            pass


    def guardarSeguimiento(self, exploreIter, outFile):
        if cons.doAttributeTracking:
            """ Prints out Attribute Tracking scores to txt file. """    
            try:  
                f = open(outFile + '_'+ str(exploreIter + 1)+'_AttTrack.txt','w') # Outputs tab delimited text file of rule population and respective rule stats
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open', outFile + '_'+ str(exploreIter + 1)+'_AttTrack.txt')
                raise 
            else:
                print("Writing Attribute Tracking as Data File...")
            
            trackingSums = cons.AT.attAccuracySums
            #-------------------------------------------------------------------
            f.write(str(cons.labelInstanceID) + '\t') #Write InstanceID label
            for att in cons.amb.formatData.trainHeaderList:
                f.write(str(att) + '\t')
            f.write(str(cons.labelPhenotype)+ '\n') #Write phenotype label
            #---------------------------------------------------------------
            for i in range(len(trackingSums)):
                trackList = trackingSums[i]
                f.write(str(cons.amb.formatData.trainFormatted[i][2])+ '\t') #Write InstanceID
                for att in trackList:
                    f.write(str(att) + '\t')
                f.write(str(cons.amb.formatData.trainFormatted[i][1]) +'\n') #Write phenotype
    
            f.close()


    def escribirPredicciones(self, exploreIter, outFile, predictionList, realList, predictionSets):
        if cons.outputTestPredictions:
            """ Prints out the Testing Predictions to txt file."""
            try:  
                f = open(outFile + '_'+ str(exploreIter + 1)+'_Predictions.txt','w') # Outputs tab delimited text file of rule population and respective rule stats
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print('cannot open', outFile + '_'+ str(exploreIter + 1)+'_Predictions.txt')
                raise 
            else:
                print("Writing Predictions to File...")

            f.write(str(cons.labelInstanceID) + '\t'+'Endpoint Predictions'+'\t' + 'True Endpoint')
            if cons.env.formatData.discretePhenotype:
                for eachClass in cons.amb.formatData.phenotypeList:
                    f.write('\t'+ str(eachClass))
            f.write('\n')
            
            for i in range(len(predictionList)):
                f.write(str(cons.amb.formatData.testFormatted[i][2])+ '\t') #Write InstanceID
                f.write(str(predictionList[i])+'\t'+str(realList[i]))
                if cons.env.formatData.discretePhenotype:
                    propList = []
                    for eachClass in cons.amb.formatData.phenotypeList:
                        propList.append(predictionSets[i][eachClass])
                    for each in propList:
                        f.write('\t'+ str(each))
                f.write('\n')
            f.close()
            
    def editarEstadsPob(self, testEval):
        """ Takes an existing popStatsFile and edits it to report Testing Accuracy performance, and Testing coverage on a specified testing dataset. """
        try:
            fileObject = open(cons.popRebootPath+"_PopStats.txt", 'rU')  # opens each datafile to read.
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', cons.popRebootPath+"_PopStats.txt")
            raise 
        #Grab the existing file information (only a couple items will change, i.e. testing acccuracy and testing coverage)
        fileStorage = []
        for each in fileObject:
            fileStorage.append(each)
            
        fileObject.close()
  
        
        try:  
            popStatsOut = open(cons.popRebootPath+'_PopStats_Testing.txt','w') # Outputs Population run stats
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', cons.popRebootPath+'_PopStats_Testing.txt')
            raise 
        else:
            print("Writing Population Statistical Summary File...")
        
        for i in range(2):
            popStatsOut.write(fileStorage[i])
        
        tempList = fileStorage[2].strip().split('\t')
        popStatsOut.write(str(tempList[0])+"\t")
        popStatsOut.write(str(testEval[0])+"\t")
        popStatsOut.write(str(tempList[2]) +"\t")
        popStatsOut.write(str(testEval[1])+"\n\n") 
        
        for i in range(4,36):
            popStatsOut.write(fileStorage[i])
      
        popStatsOut.close()
  