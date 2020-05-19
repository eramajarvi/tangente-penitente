%%% Importar datos desde el archivo de Excel al espacio de trabajo en
%%% Matlab
clear all; 
clc;

% Ruta es el nombre del archivo donde están los datos a importar
ruta = 'Datos-10minutos.xlsx';

% Cantidad total del número de días que disponemos en los datos
cantidadDias = 516;

% Cantidad total de datos que se tienen por día
cantidadDatosPorDia = 143;

% Se inicializan las matrices de interés
TemperaturaAmbiente_Matriz = zeros(cantidadDias, cantidadDatosPorDia);
VelocidadViento_Matriz = zeros(cantidadDias, cantidadDatosPorDia);
Irradiancia_Matriz = zeros(cantidadDias, cantidadDatosPorDia);

for i = 1:cantidadDias

    numeroDia = i;
    dia = ['Dia', num2str(i)];
    
    fprintf(['Calculando ' dia '...' '\n'])
    
    TemperaturaAmbiente_Matriz(i, :) = [xlsread(ruta, dia, 'C:C')]';
    VelocidadViento_Matriz(i, :) = [xlsread(ruta, dia, 'D:D')]';
    Irradiancia_Matriz(i, :) = [xlsread(ruta, dia, 'E:E')]';
end

save('MatricesDelArca', 'Irradiancia_Matriz', 'TemperaturaAmbiente_Matriz', 'VelocidadViento_Matriz');
