int: m;
int: n;

set of int: DISTANCES = 1..n+1;
set of int: DISTANCE_DOMAIN = 0..20;
array[DISTANCES, DISTANCES] of var DISTANCE_DOMAIN: D; % Distances

constraint forall(i in DISTANCES) (
  D[i,i] = 0
);

constraint forall(i in DISTANCES) (
  forall(j in DISTANCES) (
    forall(k in DISTANCES) (
      D[i,k] + D[k,j] >= D[i,j]
    )
  )
);


ann:search_ann;
% search_ann = int_search(D, input_order, indomain_random);
% search_ann = int_search(D, first_fail, indomain_random);
search_ann = int_search(D, dom_w_deg, indomain_random);

solve :: search_ann satisfy;
