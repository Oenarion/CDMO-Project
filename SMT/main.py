import numpy as np
from z3 import *
from printer import printer

m = 3 #couriers
n = 7 #items
l = [15, 10, 7] #max load per courier
s = [3,2, 6, 8, 5, 4, 4] #weight of each itemreversed_enc
D = [[0, 3, 3, 6, 5, 6, 6, 2], #distances
    [3, 0, 4, 3, 4, 7, 7, 3],
    [3, 4, 0, 7, 6, 3, 5, 3],
    [6, 3, 7, 0, 3, 6, 6, 4],
    [5, 4, 6, 3, 0, 3, 3, 3],
    [6, 7, 3, 6, 3, 0, 2, 4],
    [6, 7, 5, 6, 3, 2, 0, 4],
    [2, 3, 3, 4, 3, 4, 4, 0]]

#refactor dei pesi per comodità ma è SUPER IMPORTANTE PER DOPO
s.insert(0,0) #inserisco in posizione 0 un peso nullo... comodo per fare il calcolo con starting point

#--SUPER IMPORTANTE!!!!--------
    #preprocessing of D, we need to have the origin as first row/column for our algorithm to work correctly
    #--SUPER IMPORTANTE!!!!--------

D.insert(0,D[-1])
D.pop()
D=np.array(D)
D=np.insert(D,0,D[:,-1],axis=1)
D=D[:,:-1]

#calcolo valore di upper-bound per la funzione di max
upper_bound_distances = sum(D[0,:]) + sum(D[:,0]) 
#print(upper_bound_distances)

D=D.tolist()
#print(D)

second_dimension = n-m+3
third_dimension=[i for i in range(n+1)]
numberOfCouriers=[i for i in range(m)]
numberOfPosition=[i for i in range(second_dimension)]

#solver di SMT
solver = Solver()

#tours = LpVariable.dicts("tours", (numberOfCouriers, numberOfPosition, third_dimension), lowBound=0.0, upBound=1.0, cat=const.LpInteger)
#tours = [[Bool(f"capacity{i}_{j}") for j in range(depth_capacity)] for i in range(m)]
#since we have number, la terza dimensione non ci serve --> tours = 2D matrix
tours = [[Int(f"tours{i}_{j}")for j in range(second_dimension)]for i in range(m)] #- questo funzionava
#tours = [IntVector(f"tours_{i}", second_dimension) for i in range(m) ]

"""
la tours sarà costruita così
c0 = [0,1,2,0]
c1 = [0,3,0,0]
c2 = [0,4,0,0]
"""



print(type(tours[0][0]))

#tutti i valori assegnati devono essere nel range 0-n
for i in range(m):
    solver.add(tours[i][0]==0) #tutti devono partire da starting point
    solver.add(tours[i][1]>0) #tutti devono avere almeno 
    solver.add(tours[i][second_dimension-1]==0) #tutti devono terminare in end/start point
    for j in range(second_dimension):
        solver.add(tours[i][j]<=n) #dominio 0-n
        solver.add(tours[i][j]>=0)

#prima colonna tutti distinti
listSecondColumn = []
for i in range(m):
    listSecondColumn.append(tours[i][1])

solver.add(Distinct(listSecondColumn))

#questa la usiamo per indicare che ogni numero (indice di consegna) deve apparire una sola volta!!!
for k in range(1,n+1):
    #ricordarsi che indice poi sarà n+1 (posizione 0 non usata)

    number_of_pack_const = [tours[i][j] == k for j in range(second_dimension) for i in range(m)] + [1]

    solver.add(AtLeast(number_of_pack_const))
    solver.add(AtMost(number_of_pack_const))

#----- no hole
# constraint if there is the origin point, then all the number after it must be n+1
# because he have terminated the journey
for i in range(m):
    for j in range(2, second_dimension-1):
        solver.add(Implies(tours[i][j]==0, tours[i][j+1]==0))

#---gestione pesi
capacities = [Int(f"capacities{i}")for i in range(m)] #conversione capacità in array Z3
weights = [Int(f"capacities{i}")for i in range(n+1)] #accumulatore pesi Z3

for i in range(n+1):
    solver.add(weights[i]==s[i]) #assegno i pesi all'array z3



for i in range(m):
    solver.add(capacities[i]==l[i])#imposto l'uguaglianza forzata con il valore dato

    inter_weight = 0
    for j in range(second_dimension):
        #inter_weight += weights[]
        continue

    #definiamo qui lista z3 in cui imponiamo assegnamenti
    w_sum = [Int(f"w_sum{i}_{j}")for j in range(n+1)] #accumulatore pesi Z3

   #solver.add(Sum() <= capacities[i])
    #solver.add(capacities[i]==s[i])) #imposto l'uguaglianza forzata con il valore dato




#solver.add(capacities == K(IntSort(), s))

"""
def countOccurrencies(elem,matrix,i_size,j_size):
    counter = 0
    for i in range(i_size):
        for j in range(j_size):
            m = matrix[i][j]
            if m == elem:
                counter += 1
    return counter
    

counter = [Int(f"counter{i}")for i in range(second_dimension)] #serve come contatore per il numero di occorrenze dei delvery points
print(len(counter))
#l'array lo faccio che conta anche lo zero (0) e arriva a (second_dimension+1)
for i in range(second_dimension):
    solver.add(counter[i] == countOccurrencies(i,tours,m,second_dimension))
    
    if(i != 0 or i!=second_dimension-1):
        solver.add(counter[i] == 1)

"""




"""
print('ciaoooo')

from z3 import *
x, y = Reals('x y')
z = Int('z')

A1, A2 = Bools('A1 A2')

solver.add
solver.add(z>5)
solver.add(Or(Not(A1), 2*x + y >= -2))
solver.add(Or(A1, x + y >= 3))
solver.add(Or(Not(A2), 4*x - y >= -4))
solver.add(Or(A2, 2*x - y >= -6))
z = s.minimize(x)
print(s.check())
print(s.model())
print(z.value())
"""

print(solver.check())
#print(s.model())
mod = solver.model()
print(mod)


#per il printer: ricostruire matrice
matrix = printer(mod,"tours",m,second_dimension)
print(matrix)







#s = Solver
#s.to_smt2()