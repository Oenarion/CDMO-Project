#-m- corrieri
#-m- capacità
#-n- pacchi
#griglia di distanze fra endpoint e punti di consegna
#--> minimizzare la distanza

"""
2
6
15 10
3 2 6 5 4 4
0 3 4 5 6 6 2 
3 0 1 4 5 7 3 
4 1 0 5 6 6 4 
4 4 5 0 3 3 2 
6 7 8 3 0 2 4 
6 7 8 3 2 0 4 
2 3 4 3 4 4 0 
"""
# --Each courier must have a total weight of items lesser or equal to the total
# weight he can carry.
# --Each courier must start from the origin point.
# --Given the tours matrix, if we have the value of a point i, j where j > 2
# and toursi,j is equal to the origin point, than every value of that row must
# be equal to the origin point, because the courier ended its tour.
# --Every item that has to be delivered, must be present exactly one time in
# the tours matrix, leaving us with ((n − m + 3) ∗ m) − n times the origin
# points in the matrix.
# --The ith element of distance of tours must be the sum of every element
# present in the ith row of the tours matrix.
# --In the tours matrix, each element in the position i, 2 must be different
# from the origin point, because we have that the number of items is always
# greater than or equal to the number of couriers, so to obtain a fair division
# is better to assign to each courier at least an item.


#function that takes as input n,m and returns empty list of b
# c1 = [0,0,0,0] #-> queste tutte da assegnare
# c2 = [0,0,0,0]

# c1 = [1,2,5][4,3,#][-,-,-]
# c2 = [4,3] 

#p1=0,p2=1,3,4, -> pacchi

# c1 = [-,-,-][-,-,-][-,-,-]
# c2 = [-,-,-]
# c3 = [-,-,-]

# pacco_1 = lpvariable (0->8)
# ...
# pacco_m
# somma(valori pacchi) = 1+2+3..+7 == somma teorica senza duplicati

#0-8 in assegnamento
#3 pacchi -> 1,2,3 -> somma 6 #una volta fatto assegnamento, elimino duplicati, se assegnamento ok bene
#3 pacchi -> 6,7,8 -> somma 21
#[-,-,-][-,-,-][-,-,-]

# [p4,-,p1] #possiamo fare un compattamento verso sx (ma si creano tante soluzioni equivalenti...)
# [-,-,p2]
# [-,-,p3]


#----
#nxmxm terza dimensione = numero del pacco (NON IN BINARIO)


#[1,2,0,0] -> indici con conversione binario-intero 
#[3,0,0,0]
#[4,0,0,0]

#calcolo peso con interi
#calcolo distanza con interi
#objective function con interi minimizza(minima somma)




#pesi = 

#c10*pesi0 + jdjdjdjdj ... < capacità-c-esima

#_________________________________________

from pulp import *

m = 3 #couriers
n = 7 #items
l = [15, 10, 7] #max load per courier
s= [3,2, 6, 8, 5, 4, 4] #weight of each itemreversed_enc
D = [[0, 3, 3, 6, 5, 6, 6, 2], #distances
    [3, 0, 4, 3, 4, 7, 7, 3],
    [3, 4, 0, 7, 6, 3, 5, 3],
    [6, 3, 7, 0, 3, 6, 6, 4],
    [5, 4, 6, 3, 0, 3, 3, 3],
    [6, 7, 3, 6, 3, 0, 2, 4],
    [6, 7, 5, 6, 3, 2, 0, 4],
    [2, 3, 3, 4, 3, 4, 4, 0]]

# Crea un problema
prob = LpProblem("Problema", LpMinimize)

second_dimension = n-m+3

# Crea le variabili del problema -> parallelepipedo 3 dimensioni (n+1 per via di starting point)
tours = [[[LpVariable(f"tour{i}_{j}_{k}",lowBound=0, upBound=1, cat=LpInteger) for k in range(n+1)] for j in range(second_dimension)] for i in range(m)]

#vincolo di exactly one per ogni piano di una cella. un indice di consegna deve comparire exactly once
#saltiamo il primo piano perchè è starting point (=0)
for z in range(1,n+1):
    #vado a sommare tutto il piano
    prob += lpSum([tours[i][j][z] for j in range(second_dimension) for i in range(m)])==1


# Aggiungi il constraint "all different"
prob += lpSum(tours) == sum([i for i in range(n+1)])
#lpSum(set(tuple(tours)))

uno = LpVariable("uno",lowBound=1,upBound=3,cat=LpInteger)
due = LpVariable("due",lowBound=1,upBound=3,cat=LpInteger)
tre = LpVariable("tre",lowBound=1,upBound=3,cat=LpInteger)

lista = [uno,due,tre]

prob += lpSum(lista) == 6

# Risolvi il problema
prob.solve()







# Stampa i valori delle variabili
for var in prob.variables():
    print(f"{var.name} = {var.varValue}")