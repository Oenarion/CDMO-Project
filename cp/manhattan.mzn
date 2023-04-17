set of int: NUMBER_OF_COURIERS = 1..m; 
array[NUMBER_OF_COURIERS] of int: l; % Resource capacities

set of int: NUMBER_OF_PACKAGES = 1..n; 
array[NUMBER_OF_PACKAGES] of int: s; % Weights

int: n = 7;
int: m = 3;

% function array[int] of int: rimuovi_zeri(array_input) =
% function array[int] of int: rimuovi_zeri(array_input) =
%   let {
%     % Determina la lunghezza dell'array di input
%     int: n = length(array_input);

%     % Filtra l'array originale per rimuovere gli zeri
%     array[1..count(i in 1..n)(array_input[i] != 0)] of int: array_filtrato =
%       [array_input[i] | i in 1..n where array_input[i] != 0];
%   } in
%     % Ritorna l'array filtrato
%     array_filtrato;

% function set of (int,int): array_to_parset(array[int] of int: a) =
%   set { i -> a[i] | i in index_set(a) };

function var int: manhattan(array[NUMBER_OF_PACKAGES] of var int: x) =
    let{
    array[1..count(i in 1..n)(array_input[i] != 0)] of int: array_filtrato =
      [length(x)+1] ++ [x[i] | i in 1..n where x[i] != 0] ++ [length(x)+1];
    }
    in
    sum ([D[array_filtrato[i], array_filtrato[i+1]] | i in 1..length(array_filtrato)]);


% Definisci un array di interi
array[1..n] of int: array_input = [0, 5, 0, 3, 0, 1];

% Determina la lunghezza dell'array di input
int: lengtharray = length(array_input);

% Filtra l'array originale per rimuovere gli zeri
array[1..count(i in 1..lengtharray)(array_input[i] != 0)] of int: array_filtrato =
  [array_input[i] | i in 1..lengtharray where array_input[i] != 0];
       
array[NUMBER_OF_PACKAGES] of int: aaa = [1,0,0,4,7,0,0];  
         
set of int: DISTANCES = 1..n+1;
array[DISTANCES, DISTANCES] of int: D;
D = 
[|0, 3, 3, 6, 5, 6, 6, 2
|3, 0, 4, 3, 4, 7, 7, 3
|3, 4, 0, 7, 6, 3, 5, 3
|6, 3, 7, 0, 3, 6, 6, 4
|5, 4, 6, 3, 0, 3, 3, 3
|6, 7, 3, 6, 3, 0, 2, 4
|6, 7, 5, 6, 3, 2, 0, 4
|2, 3, 3, 4, 3, 4, 4, 0|];
         
output[ show(manhattan(aaa))
]