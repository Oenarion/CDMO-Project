include "globals.mzn";

int: m; % couriers
int: n; % items

set of int: NUMBER_OF_COURIERS = 1..m; 
array[NUMBER_OF_COURIERS] of int: l; % Resource capacities

set of int: NUMBER_OF_PACKAGES = 1..n; 
array[NUMBER_OF_PACKAGES] of int: s; % Weights

set of int: DISTANCES = 1..n+1;
array[DISTANCES, DISTANCES] of int: D; % Distances

% Domains
set of int: TOUR_DOMAIN = 1..n+1; 
set of int: TOUR_SIZE = 1..n+2;
set of int: CHECK_HOME = 2..n+1;

% Variables
array[NUMBER_OF_COURIERS, TOUR_SIZE] of var TOUR_DOMAIN: tours;
% in each row there is the path of the courier
% [
% 	8 1 8 8
% 	8 2 8 8
% ]

% Constraints
% each item must be present only one time
% constraint alldifferent([tours[i,j] | i in NUMBER_OF_COURIERS, j in TOUR_SIZE where tours[i,j]!=n+1]);
constraint forall(i in NUMBER_OF_COURIERS)(
  tours[i,1] = n+1 % each courier start from the home
);

% each item must be in the matrix
% constraint forall(e in NUMBER_OF_PACKAGES)(
% %   has_element(i, tours)
%   % exists(k in index_set(NUMBER_OF_PACKAGES)) ([tours[i,j] | i in NUMBER_OF_COURIERS, j in TOUR_SIZE where tours[i,j]!=n+1][k] == e)
%   [tours[i,j] | i in NUMBER_OF_COURIERS, j in TOUR_SIZE where tours[i,j] == e][1] == e
% );
% constraint sort([tours[i,j] | i in NUMBER_OF_COURIERS, j in TOUR_SIZE where tours[i,j]!=n+1]) == [i | i in NUMBER_OF_PACKAGES];


% if there is the home, then all the number after it must be n+1, because he have terminated the journey
constraint forall(i in NUMBER_OF_COURIERS)(
  forall(j in CHECK_HOME)(
%        if tours[i,j] == n+1
%        then tours[i,j+1] = n+1
%        else true
%        endif
    tours[i,j] == n+1 -> tours[i,j+1] = n+1
   )
);

%constraint on the size of the truck
constraint forall(i in NUMBER_OF_COURIERS)(
  sum([s[tours[i,j]] |  j in TOUR_SIZE where tours[i,j] != n+1]) <= l[i]
);

% constraint forall(e in NUMBER_OF_PACKAGES)(
%   sum([tours[i,j] | i in NUMBER_OF_COURIERS, j in CHECK_HOME where tours[i,j] == e]) > 0
% );
% constraint on the numbers in the matrix:
% each item must be present only one time
% each "home" must be present (n+2)*m-2 times
constraint global_cardinality_low_up(tours, TOUR_DOMAIN, [1 | i in NUMBER_OF_PACKAGES]++[(n+2)*m-n], [1 | i in NUMBER_OF_PACKAGES]++[(n+2)*m-n]);


% compute the distances
set of int: DISTANCE_OF_COURIER = 0..2*sum([D[i,length(s)+1] | i in DISTANCES]);
% this is the worst distance that the courier could do, because he delivers a package and then goes home, he takes another package and he delivers it...
array[NUMBER_OF_COURIERS] of var DISTANCE_OF_COURIER: distances_of_tours;
constraint forall(i in NUMBER_OF_COURIERS)(
  distances_of_tours[i] = sum([D[tours[i,k], tours[i,k+1]] | k in TOUR_DOMAIN])
);

solve minimize max(distances_of_tours)
% output[show([tours[i,j] | i in NUMBER_OF_COURIERS, j in TOUR_SIZE where tours[i,j] == 8][0])]

