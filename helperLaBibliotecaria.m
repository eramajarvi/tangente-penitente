%% La Bibliotecaria
% Extrae un vector de activación de la irrigacion a partir de los perfiles 
% optimos generados por chispa-culpable

clc;
clear all;
close all;

tic
fprintf('La Bibliotecaria está organizando los datos de los perfiles óptimos... \n\n');

cantidadDias = 516;
datasetTodosDias = zeros(cantidadDias * 143, 4);

% Rutas para importar los perfiles optimos de forma recursiva con los datos
% de todos los dias y guardar los datasets generados
load('MatricesDelArca.mat');
rutaGuardadoDatasets = 'C:\Users\james\Documents\Github\tangente-penitente\datasets\';

% Funciones anonimas
% Usadas para controlar el indice de asignacion de la matriz dataset que 
% contiene el total de los datos
limiteSuperior = @(n) 143 * n + 1;
limiteInferior = @(m) 143 * m;

% Matriz de 'control' vacia
control = zeros(1, 143);

for i = 1 : 1 : cantidadDias
    
    numeroDia = i;
    
    Irradiancia = Irradiancia_Matriz(i, :);
    TemperaturaAmbiente = TemperaturaAmbiente_Matriz(i, :);
    VelocidadViento = VelocidadViento_Matriz(i, :);
    
    entradasDia = [Irradiancia; TemperaturaAmbiente; VelocidadViento];
    
    % Indice de columnas de la matriz de activacion:
    % 1-Irradiancia
    % 2-Temperatura ambiente
    % 3-Velocidad del viento
    
    % Transpone la matriz individual del dia
    entradasDia = entradasDia';
    salidasDia = control';
    
    datasetTodosDias(limiteSuperior(i - 1) : limiteInferior(i), :) = [entradasDia salidasDia];
    
    nombreMatrizDatasets = [rutaGuardadoDatasets, 'matrizDataset_Dia', num2str(i)];
    
    % Guarda los datasets generados
    datasetDia = [entradasDia, salidasDia];
    
    %save(nombreMatrizDatasets, 'datasetDia');
    %save([rutaGuardadoDatasets, 'datasetPerfiles'], 'datasetTodosDias');

end

%% Preparacion para exportar
% Editar las siguientes dos lineas la cantidad de dias deseados en el
% conjunto de datos resultante:
cantidadDiasEntrenamiento = 1;
cantidadDiasPrueba = 1;

cantidadDiasExportar = cantidadDiasEntrenamiento + cantidadDiasPrueba;
diasExportar = randperm(cantidadDias, cantidadDiasExportar);

diasEntrenamiento = diasExportar(1 : cantidadDiasEntrenamiento);
diasPrueba = diasExportar(cantidadDiasEntrenamiento + 1 : end);

% Exportar dias especificos de prueba: descomentar la siguiente linea
%diasPrueba = [1];

datasetEntrenamiento = seleccionDias(diasEntrenamiento, datasetTodosDias);
datasetPrueba = seleccionDias(diasPrueba, datasetTodosDias);

% -------------------------------------------------------------------------
%% Llamada a las funciones de exportacion
%exportarDatasetCompleto(rutaGuardadoDatasets, datasetTodosDias);

%exportarDatasetEntrenamiento(rutaGuardadoDatasets, datasetEntrenamiento, diasEntrenamiento);
exportarDatasetPrueba(rutaGuardadoDatasets, datasetPrueba, diasPrueba);
% -------------------------------------------------------------------------
fprintf('La Bibliotecaria ha terminado de analizar %d perfiles óptimos en %f segundos \n\n', cantidadDias, toc);

%% Seleccion de dias de entrenamiento/prueba desde el conjunto de datos
function dataset = seleccionDias(dias, datasetTodosDias)

    limiteSuperior = @(n) 143 * n + 1;
    limiteInferior = @(m) 143 * m;

    cantidadDias = length(dias);
    dataset = zeros(cantidadDias * 143, 4);

    for i = 1 : cantidadDias
        dataset(limiteSuperior(i - 1) : limiteInferior(i), :) = datasetTodosDias(limiteSuperior(dias(i) - 1) : limiteInferior(dias(i)), :);
    end

end

%% Exportar conjuntos de datos
function exportarDatasetCompleto(rutaGuardadoDatasets, datasetTodosDias)
%%exportarDatasetCompleto
% Exporta todos los datos disponibles en un unico archivo

    fileID = fopen([rutaGuardadoDatasets, 'datasetsPerfiles.txt'], 'w');
    formatoEncabezado = ['%s %12s %12s %12s \r\n'];
    formatoDatos = ['%.4f %12.4f %12.4f %12.0f\r\n'];

    fprintf(fileID, formatoEncabezado, 'irrad', 'Tamb', 'vient', 'Irrig');
    fprintf(fileID, formatoDatos, datasetTodosDias');
    fclose(fileID);
    
    fprintf('La Bibliotecaria ha exportado todos los perfiles como un conjunto de datos en %s\n', rutaGuardadoDatasets);

end

function exportarDatasetEntrenamiento(rutaGuardadoDatasets, datasetDiasEntrenamiento, diasEntrenamiento)
%% exportarDatasetEntrenamiento
% Exporta solo los dias de entrenamiento indicados en un archivo

    fileID = fopen([rutaGuardadoDatasets, 'datasetTP.txt'], 'w');
    formatoEncabezado = ['%s %1s %1s %1s\r\n'];
    formatoDatos = ['%.4f %1.4f %1.4f %1.0f\r\n'];
    
    fprintf(fileID, formatoEncabezado, 'R_0','R_1', 'R_2', 'Class');
    fprintf(fileID, formatoDatos, datasetDiasEntrenamiento');
    fclose(fileID);
    
    fprintf('\nLa Bibliotecaria ha exportado los perfiles de entrenamiento en un conjunto de datos en %s de los siguientes dias: \n', rutaGuardadoDatasets);
    disp(diasEntrenamiento);
    
end

function exportarDatasetPrueba(rutaGuardadoDatasets, datasetDiasPrueba, diasPrueba)
%% exportarDatasetMinimo
% Exporta solo los dias de prueba indicados en un archivo

    fileID = fopen([rutaGuardadoDatasets, 'datasetTP_PRUEBA.txt'], 'w');
    formatoEncabezado = ['%s %1s %1s %1s\r\n'];
    formatoDatos = ['%.4f %1.4f %1.4f %1.0f\r\n'];
    
    fprintf(fileID, formatoEncabezado, 'R_0','R_1', 'R_2', 'Class');
    fprintf(fileID, formatoDatos, datasetDiasPrueba');
    fclose(fileID);
    
    fprintf('La Bibliotecaria ha exportado los perfiles de prueba en un conjunto de datos en %s de los siguientes dias: \n', rutaGuardadoDatasets);
    disp(diasPrueba);
end

