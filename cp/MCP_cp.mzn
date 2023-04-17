include "globals.mzn";

int: m;
int: n;

set of int: NUMBER_OF_COURIERS = 1..m; 
array[NUMBER_OF_COURIERS] of int: l; % Resource capacities

set of int: NUMBER_OF_PACKAGES = 1..n; 
array[NUMBER_OF_PACKAGES] of int: s; % Weights

set of int: DISTANCES = 1..n+1;

array[DISTANCES, DISTANCES] of int: D;

% Variables
% array of the size of the packages for which each element is assigned to the courier 
array[NUMBER_OF_PACKAGES] of var NUMBER_OF_COURIERS: assignment_of_packages; 

% array of courier that represent the actual weight
%array[NUMBER_OF_COURIERS] of var int: weight_courier;

%array[1..2] of int: zero = [0,0];

% constarint on the size of the truck
constraint forall(i in NUMBER_OF_COURIERS) ( % for all couriers
   sum([s[j] | j in NUMBER_OF_PACKAGES where assignment_of_packages[j] == i]) <= l[i] 
);

% matrix where each row represent the packages that a courier will deliver
% at the end there will be zero
set of int: PLACE = 0..n; 
array[NUMBER_OF_COURIERS, NUMBER_OF_PACKAGES] of var PLACE: courier_tour;

constraint forall(i in NUMBER_OF_COURIERS) (
   forall(j in NUMBER_OF_PACKAGES) (
      if assignment_of_packages[j] == i 
        then courier_tour[i,j] = j %assignment_of_packages[j]
      else courier_tour[i,j] = 0
      endif
   )
);





% compute the distances
set of int: DISTANCE_OF_COURIER = 2*sum([D[i,length(s)] | i in DISTANCES]); 
% this is the worst distance that the courier could do, because he delivers a package and then goes home, he takes another package and he delivers it...
array[NUMBER_OF_COURIERS] of var DISTANCE_OF_COURIER: distances_of_tours; 
constraint forall(i in NUMBER_OF_COURIERS)(
  distances_of_tours[i] = sum([courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0])
)

[courier_tour[i] | if courier_tour[i]!=0]

% int: maxDist = 0..50; %sum(D[n-1][i] |);
% set of int: DISTANCE_OF_COURIER = 1..maxDist;
% array [NUMBER_OF_COURIERS] of var DISTANCE_OF_COURIER: distances_of_couriers;




% solve minimize max(distances_of_couriers)

% ann:search_ann;
% search_ann = int_search(assignment_of_packages, input_order, indomain_random);
% solve :: search_ann
% minimize assignment_of_packages[2];

% output [ if fix(q[j]) == i then "Q" else "." endif ++
%          if j == n then "\n" else "" endif | i,j in 1..n, 
% ]