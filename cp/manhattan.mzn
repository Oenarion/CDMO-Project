set of int: NUMBER_OF_COURIERS = 1..m; 
array[NUMBER_OF_COURIERS] of int: l; % Resource capacities

set of int: NUMBER_OF_PACKAGES = 1..n; 
array[NUMBER_OF_PACKAGES] of int: s; % Weights

int: n = 7;
int: m = 3;

function var int: manhattan(array[NUM] of var int: x) =
         %x[0];
         sum([D[i][i+1] | i in 1..length(x)]);
%          forall(i in x)(
%           sum(D[i][i+1])
%          )
       
array[NUMBER_OF_PACKAGES] of int: aaa = [1,4,7];  
         
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
         
output[ manhattan
]