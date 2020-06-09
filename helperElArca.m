%% EL ARCA
%%% Importa datos desde el archivo de Excel al espacio de trabajo en
%%% Matlab
clear all; 
clc;

tic

% Ruta es el nombre del archivo donde están los datos a importar
ruta = 'Datos-10minutos.xlsx';

% Cantidad total del número de días que disponemos en los datos
cantidadDias = 588;

% Cantidad total de datos que se tienen por día de 6AM a 6PM
% en 12 horas, cada 10 minutos, se tienen 73
cantidadDatosPorDia = 73;

diasCreados = 0;

% Se inicializan las matrices de interés
TemperaturaAmbiente_Matriz = zeros(cantidadDias, cantidadDatosPorDia);
VelocidadViento_Matriz = zeros(cantidadDias, cantidadDatosPorDia);
Irradiancia_Matriz = zeros(cantidadDias, cantidadDatosPorDia);

for i = 1:cantidadDias

    numeroDia = j;
    dia = ['Dia', num2str(i)];
    
    Hora_temp = xlsread(ruta, dia, 'B:B');
    Hora_temp = Hora_temp(find(Hora_temp == 0.25):find(Hora_temp == 0.75));
    
    fprintf(['Calculando ' dia '...' '\n'])
    
    if length(Hora_temp) == 73
        fprintf('Calculando dia %d...\n', j)
        
        % Lee del archivo de Excel los datos
        TemperaturaAmbiente_Matriz(j, :) = xlsread(ruta, dia, 'C37:C109')';
        VelocidadViento_Matriz(j, :) = xlsread(ruta, dia, 'D37:D109')';
        Irradiancia_Matriz(j, :) = xlsread(ruta, dia, 'E37:E109')';
   
        diasCreados = diasCreados + 1;
    end
    
    j = j + 1;
    
end

%% Limpiar la matriz de las filas vacias
TemperaturaAmbiente_Matriz( ~any(TemperaturaAmbiente_Matriz, 2), : ) = [];
VelocidadViento_Matriz( ~any(VelocidadViento_Matriz, 2), : ) = [];
Irradiancia_Matriz( ~any(Irradiancia_Matriz, 2), : ) = [];

%% Guardar datos

save('MatricesDelArca', 'Irradiancia_Matriz', 'TemperaturaAmbiente_Matriz', 'VelocidadViento_Matriz');
fprintf('El Arca construyo %d dias de los %d disponibles en %f segundos.\n', diasCreados, toc, cantidadDias);

