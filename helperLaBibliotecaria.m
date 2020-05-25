%% La Bibliotecaria
% Extrae un vector de activación de la irrigacion a partir de los perfiles 
% optimos generados por chispa-culpable

clc;
clear all;
close all;

tic
fprintf('La Bibliotecaria está organizando los datos de los perfiles óptimos... \n\n');

cantidadDias = 516;

datasetTodosDias = zeros(cantidadDias * 720, 7);

% Rutas para importar los perfiles optimos de forma recursiva con los datos
% de todos los dias y guardar los datasets generados
rutaCargaPerfiles = 'C:\Users\james\Documents\Github\tp-legacy\perfiles\';
rutaGuardadoDatasets = 'C:\Users\james\Documents\Github\ExctractsBase\Datasets\';

% Funciones anonimas
% Usadas para controlar el indice de asignacion de la matriz dataset que 
% contiene el total de los datos
limiteSuperior = @(n) 720 * n + 1;
limiteInferior = @(m) 720 * m;

for i = 1 : 1 : cantidadDias
    
    numeroDia = i;
        
    nombreArchivo = ['perfil_Dia', num2str(i)];
        
    ruta = [rutaCargaPerfiles, nombreArchivo, '.mat'];
    load(ruta);
    
    activado = find(control == 15); % Encuentra la posicion cuando se activa la irrigacion
    noActivado = find(control == 0);
    horasActivacion = tiempo./3600 + 6; % El rango es de 6:00h a 18:00h, se encuentra la hora exacta de activacion
    
    % Valores de las variables de interes cuando hay activacion de la irrigacion
    entradasDia = [horasActivacion(1:length(Pben)); irradiancia(1:length(Pben));...
        temperaturaAmbiente(1:length(Pben)); velocidadViento(1:length(Pben));...
        temperaturaPanel(1:length(Pben)); Pben];
    
    % dayTargets guarda el control de la irrigacion con dos valores:
    % 0 es cuando el sistema NO esta irrigado
    % 1 cuando SI esta irrigado
    salidasDia = zeros(1, length(Pben));
    salidasDia(1, noActivado) = 0;
    salidasDia(1, activado) = 1;
    
    % Indice de columnas de la matriz de activacion:
    % 1-Horas de activacion
    % 2-Irradiancia
    % 3-Temperatura ambiente
    % 4-Velocidad del viento
    % 5-Temperatura en la superficie del panel
    % 6-Potencia beneficio
    
    % Transpone la matriz individual del dia
    entradasDia = entradasDia';
    salidasDia = salidasDia';
    
    datasetTodosDias(limiteSuperior(i - 1) : limiteInferior(i), :) = [entradasDia salidasDia];
    
    nombreMatrizDatasets = [rutaGuardadoDatasets, 'matrizDataset_Dia', num2str(i)];
    
    % Guarda los datasets generados
    datasetDia = [entradasDia, salidasDia];
    
    %save(nombreMatrizDatasets, 'datasetDia');
    %save([rutaGuardadoDatasets, 'datasetPerfiles'], 'datasetTodosDias');

end

%exportarDataset(rutaGuardadoDatasets, datasetTodosDias);
exportarDatasetMinimo(rutaGuardadoDatasets, datasetTodosDias);

fprintf('La Bibliotecaria ha terminado de analizar %d perfiles óptimos en %f segundos \n\n', cantidadDias, toc);


function exportarDataset(rutaGuardadoDatasets, datasetTodosDias)

    fileID = fopen([rutaGuardadoDatasets, 'datasetsPerfiles.txt'], 'w');
    formatoEncabezado = ['%s %12s %12s %12s %12s %12s %12s\r\n'];
    formatoDatos = ['%.4f %12.4f %12.4f %12.4f %12.4f %12.4f %12.0f\r\n'];


    fprintf(fileID, formatoEncabezado, 'hora','irrad', 'Tamb', 'vient', 'Tpan', 'Pben', 'Irrig');
    fprintf(fileID, formatoDatos, datasetTodosDias');
    fclose(fileID);

end

function exportarDatasetMinimo(rutaGuardadoDatasets, datasetTodosDias)

    fileID = fopen([rutaGuardadoDatasets, 'datasetTPTEST.txt'], 'w');
    formatoEncabezado = ['%s %1s %1s %1s %1s %1s %1s\r\n'];
    formatoDatos = ['%.4f %1.4f %1.4f %1.4f %1.4f %1.4f %1.0f\r\n'];
    
    fprintf(fileID, formatoEncabezado, 'R_0','R_1', 'R_2', 'R_3', 'R_4', 'R_5', 'Class');
    fprintf(fileID, formatoDatos, datasetTodosDias(21601:43200, :)');
    fclose(fileID);
end


