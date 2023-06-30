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

def getMax(prob,name,lowerbound,upperbound,distances):

    y = LpVariable(name,lowBound=lowerbound,upBound=upperbound,cat=LpInteger) # risultato

    ds = []

    counter = 0
    for elem in distances:
        d = LpVariable(f"d_{counter}_{name}",lowBound=0,upBound=1,cat=LpInteger) # variabile di appoggio
        print(d)
        #prob += d
        ds.append(d)
        prob += y >= elem
        #prob += y <= elem + (upperbound - lowerbound)*d
        prob += y <= elem + (upperbound - lowerbound)*(1-d)
        
        
        counter += 1 
    
    prob += lpSum(ds) == 1

    return y

def getMax2(prob,name,lowerbound,upperbound,distances):

    ys = []
    ds = []

    ds.append(LpVariable(f"d_{0}_{name}",lowBound=0,upBound=1,cat=LpInteger)) # variabile di appoggio

    for index in range(1,len(distances)):
        ys.append(LpVariable(f"y_{index}_{name}",lowBound=lowerbound,upBound=upperbound,cat=LpInteger)) # risultato
        ds.append(LpVariable(f"d_{index}_{name}",lowBound=0,upBound=1,cat=LpInteger)) # variabile di appoggio

        prob += ys[-1] >= distances[index-1]
        prob += ys[-1] <= distances[index-1] + (upperbound - lowerbound)*ds[index]
        prob += ys[-1] <= distances[index] + (upperbound - lowerbound)*(1-ds[-2])
        
    prob += lpSum(ds) == 1

    return ys[-1]

prob += variabile1 == (forceAnd(prob,v0,v1)*distances[1])




lista = [5,15,8,10,60,4,0,120]
massimo = getMax(prob,"mmm",0,1000,lista)

prob.solve()
for var in prob.variables():
        if not re.match("(^[0-9]_[0-9]_[0-9]_[0-9]_[0-9]$)", var.name): #elimino variabili superflue
            print(f"{var.name} = {var.varValue}",type(var.varValue))

exit(1)


prob.solve()


#Stampa i valori delle variabili
for var in prob.variables():
    print(f"{var.name} = {var.varValue}",type(var.varValue))
       #if "distance_of_tours" in var.name:
       #    print(f"{var.name} = {var.varValue}")
        
