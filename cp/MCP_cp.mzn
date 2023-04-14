include "globals.mzn";

int: m;
int: n;

set of int: RESOURCES = 1..m; 
array[RESOURCES] of int: l; % Resource capacities

set of int: WEIGHT = 1..n; 
array[WEIGHT] of int: s; % Weights

set of int: DISTANCES = 1..n+1;

array[DISTANCES, DISTANCES] of int: D;

% Variables
% array of the size of the packages for which each element is assigned to the courier 
array[WEIGHT] of var RESOURCES: assignment_of_packages; 

% array of courier that represent the actual weight
%array[RESOURCES] of var int: weight_courier;

%array[1..2] of int: zero = [0,0];


constraint forall(i in RESOURCES) ( % for all couriers
   sum([s[j] | j in WEIGHT where assignment_of_packages[j] == i]) <= l[i] 
);



% int: maxDist = 0..50; %sum(D[n-1][i] |);
% set of int: DISTANCE_OF_COURIER = 1..maxDist;
% array [RESOURCES] of var DISTANCE_OF_COURIER: distances_of_couriers;




% solve minimize max(distances_of_couriers)


% output [
%     "ciao"
% ];