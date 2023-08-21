include "globals.mzn";
include "chuffed.mzn";

int: m; % couriers
int: n; % items

set of int: NUMBER_OF_COURIERS = 1..m; 
array[NUMBER_OF_COURIERS] of int: l; % Resource capacities

set of int: NUMBER_OF_PACKAGES = 1..n; 
array[NUMBER_OF_PACKAGES] of int: s; % Weights

set of int: DISTANCES = 1..n+1;
array[DISTANCES, DISTANCES] of int: D; % Distances

% Domains
int: lastElement = n-m+3; % second dimension of the matrix "tours"

set of int: TOUR_DOMAIN = 1..n+1; 
set of int: TOUR_SIZE = 1..lastElement;
set of int: CHECK_HOME = 3..lastElement-1;
set of int: SUM_DOMAIN = 1..lastElement-1;

% Variables
array[NUMBER_OF_COURIERS, TOUR_SIZE] of var TOUR_DOMAIN: tours;
% in each row there is the path of the courier
% [
% 	3 1 3 3
% 	3 2 3 3
% ]

% Constraints
% each item must be present only one time
% constraint alldifferent([tours[i,j] | i in NUMBER_OF_COURIERS, j in TOUR_SIZE where tours[i,j]!=n+1]);

%constraint on the size of the vehicle
constraint forall(i in NUMBER_OF_COURIERS)(
  sum([s[tours[i,j]] |  j in TOUR_SIZE where tours[i,j] != n+1]) <= l[i]
);


constraint forall(i in NUMBER_OF_COURIERS)(
  tours[i,1] = n+1 % each courier start from the origin point
);


% if there is the home, then all the number after it must be n+1, because he have terminated the journey
constraint forall(i in NUMBER_OF_COURIERS)(
  forall(j in CHECK_HOME)(
    tours[i,j] == n+1 -> tours[i,j+1] = n+1
   )
);



% constraint on the numbers in the matrix:
% each item must be present only one time
% each "home" must be present (n+2)*m-2 times
constraint global_cardinality_low_up(tours, TOUR_DOMAIN, [1 | i in NUMBER_OF_PACKAGES]++[lastElement*m-n], [1 | i in NUMBER_OF_PACKAGES]++[lastElement*m-n]);
%[1,2,3,4,..,11] tour_domain
%[1,1,1,1,..,50] lower bound of each value
%[1,1,1,1,..,50] upper bound of each value


% compute the distances
set of int: DISTANCE_OF_COURIER = 0..sum([D[i,length(s)+1] | i in DISTANCES]) + sum([D[length(s)+1, i] | i in DISTANCES]);
% this is the worst distance that the courier could do, because he delivers a package and then goes home, he takes another package and he delivers it...

% array[NUMBER_OF_COURIERS] of var DISTANCE_OF_COURIER: distances_of_tours;
% constraint forall(i in NUMBER_OF_COURIERS)(
%   distances_of_tours[i] = sum([D[tours[i,k], tours[i,k+1]] | k in SUM_DOMAIN])
% );

var DISTANCE_OF_COURIER: max_distance_of_tours = max([sum([D[tours[i,k], tours[i,k+1]] | k in SUM_DOMAIN]) | i in NUMBER_OF_COURIERS]);
  


% To achieve a fair division among drivers, each courier must have at least an item (because n>=m)
constraint forall(i in NUMBER_OF_COURIERS)(
%   if n>m
%   then length([tours[i,j] | j in TOUR_SIZE where tours[i,j] != n+1])>0
%   endif
  % n>m -> distances_of_tours[i]>0
  tours[i,2] != n+1 
);

constraint forall(i,j in NUMBER_OF_COURIERS)(
%forall(j in NUMBER_OF_COURIERS)(
%   if j > i /\ l[i] == l[j] 
%   then lex_lesseq([tours[i,k] | k in TOUR_SIZE], [tours[j,t] | t in TOUR_SIZE])
%   endif
  j > i /\ l[i] == l[j] -> lex_lesseq([tours[i,k] | k in TOUR_SIZE], [tours[j,t] | t in TOUR_SIZE])
);

ann:search_ann;
search_ann = int_search(tours, input_order, indomain_min);
% % search_ann = int_search(tours, input_order, indomain_random);
% % search_ann = int_search(tours, first_fail, indomain_min);
% % search_ann = int_search(tours, first_fail, indomain_random);
% % search_ann = int_search(tours, dom_w_deg, indomain_min);
%search_ann = int_search(tours, dom_w_deg, indomain_random);

solve :: search_ann
% minimize max(distances_of_tours);
minimize max_distance_of_tours;

int: digs = ceil(log(10.0,int2float(n+1))); % digits for output
output["tours: \n"] ++
  [ show_int(digs,tours[i,j]) ++ " " ++ 
    if j == lastElement then "\n" else "" endif |
    i in NUMBER_OF_COURIERS, j in TOUR_SIZE ] ++ 
  ["max distance: \(max_distance_of_tours)"];
