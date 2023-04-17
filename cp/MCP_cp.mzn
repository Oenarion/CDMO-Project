include "globals.mzn";

int: m; % couriers
int: n; % items

set of int: NUMBER_OF_COURIERS = 1..m; 
array[NUMBER_OF_COURIERS] of int: l; % Resource capacities

set of int: NUMBER_OF_PACKAGES = 1..n; 
array[NUMBER_OF_PACKAGES] of int: s; % Weights

set of int: DISTANCES = 1..n+1;
array[DISTANCES, DISTANCES] of int: D;

% Variables
% array of the size of the packages for which each element is assigned to the courier 
array[NUMBER_OF_PACKAGES] of var NUMBER_OF_COURIERS: assignment_of_packages; 

% constarint on the size of the truck
constraint forall(i in NUMBER_OF_COURIERS) ( % for all couriers
   sum([s[j] | j in NUMBER_OF_PACKAGES where assignment_of_packages[j] == i]) <= l[i] 
);


% matrix where each row represent the packages that a courier will deliver
% if a courier don't deliver an item then I will have a zero in that position
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
set of int: DISTANCE_OF_COURIER = 0..2*sum([D[i,length(s)] | i in DISTANCES]); 
% this is the worst distance that the courier could do, because he delivers a package and then goes home, he takes another package and he delivers it...
array[NUMBER_OF_COURIERS] of var DISTANCE_OF_COURIER: distances_of_tours; 

constraint forall(i in NUMBER_OF_COURIERS)(
  % the distance of the i-th courier is equal to the sum of the D[i,j]
  % the D[i,j] are obtained using the courier_tour matrix without the zeros
  % the indexes of D are obtained using courier_tour_no_zero[i, k] and courier_tour_no_zero[i, k+1] such that is used the distance between the item k and the item k+1 that the courier will deliver
  distances_of_tours[i] = sum([
    D[[courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0][k],
    [courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0][k+1]]
    | k in 1..length([courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0])-1
    ])
);


% let {distances_of_tours = [sum([ D[[courier_tour[i,j] | j in NOP where courier_tour[i, j]!=0][k], [courier_tour[i,j] | j in NOP where courier_tour[i, j]!=0][k+1]] | k in 1…length([courier_tour[i,j] | j in NOP where courier_tour[i, j]!=0])-1 ]) | i in NOC]} in output[show(distances_of_tours)];

% let {array[NUMBER_OF_COURIERS] of var DISTANCE_OF_COURIER: distances_of_tours = [sum([ D[[courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0][k], [courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0][k+1]] | k in 1..length([courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0])-1 ]) | i in NUMBER_OF_COURIERS]} 
% in distances_of_tours

%solve minimize sum([distances_of_tours[i]^2 | i in NUMBER_OF_COURIERS]);
solve minimize max(distances_of_tours);


% distances_of_tours = [sum([
%     D[[courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0][k],
%     [courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0][k+1]]
%     | k in 1..length([courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0])-1
%     ]) | i in NUMBER_OF_COURIERS];

% ann:search_ann;
% search_ann = int_search(assignment_of_packages, input_order, indomain_random);
% solve :: search_ann
% minimize assignment_of_packages[2];

output[show(
[sum([
    D[[courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0][k],
    [courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0][k+1]]
    | k in 1..length([courier_tour[i,j] | j in NUMBER_OF_PACKAGES where courier_tour[i, j]!=0])-1
    ]) | i in NUMBER_OF_COURIERS]
), "\n", 
show(courier_tour), "\n",
show(distances_of_tours)
];
