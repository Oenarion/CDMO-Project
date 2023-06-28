from pulp import *

prob = LpProblem("Problema")

distances = [10,20,30,40]

v0 = LpVariable("v0",lowBound=0,upBound=1,cat=LpInteger)
v1 = LpVariable("v1",lowBound=0,upBound=1,cat=LpInteger)
d = LpVariable("d",lowBound=0,upBound=1,cat=LpInteger)
prob+= v0 == 0
prob+= v1 == 0

# f0 = LpVariable("f0",lowBound=0,upBound=1,cat=LpInteger) #variabili di flag
# f1 = LpVariable("f1",lowBound=0,upBound=1,cat=LpInteger)

variabile1 = LpVariable("variabile1",lowBound=0,upBound=None,cat=LpInteger)
# variabile2 = LpVariable("variabile2",lowBound=0,upBound=None,cat=LpInteger)

#prob+=variabile1==((f0 * f1)) #somma f0 tot volte quanto in rage f1
# prob+=lpSum([lpSum([tours[i][j][k] for j in range(second_dimension)])*s[k-1] for k in range(1,n+1)])<=l[i]

def forceAnd(prob,v0,v1):
    d = LpVariable("d",lowBound=0,upBound=1,cat=LpInteger) # risultato
    prob += d<=v0
    prob += d<=v1
    prob += d>= v0+v1-1
    prob += d>=0
    return d


prob += variabile1 == (forceAnd(prob,v0,v1)*distances[1])

prob.solve()


#Stampa i valori delle variabili
for var in prob.variables():
    print(f"{var.name} = {var.varValue}",type(var.varValue))
       #if "distance_of_tours" in var.name:
       #    print(f"{var.name} = {var.varValue}")
        
