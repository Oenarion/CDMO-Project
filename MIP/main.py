import numpy as np
from pulp import *
import re #string mather
import sys





# solver_list = listSolvers()

# print(solver_list)
# exit(1)

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

# Aggiungi il constraint "all different"
#prob += lpSum(tours) == sum([i for i in range(n+1)])
#lpSum(set(tuple(tours)))

# uno = LpVariable("uno",lowBound=1,upBound=3,cat=LpInteger)
# due = LpVariable("due",lowBound=1,upBound=3,cat=LpInteger)
# tre = LpVariable("tre",lowBound=1,upBound=3,cat=LpInteger)

# lista = [uno,due,tre]

# prob += lpSum(lista) == 6


#pesi = 

#c10*pesi0 + jdjdjdjdj ... < capacità-c-esima

#_________________________________________

def forceAnd(prob,name,v0,v1):
    d = LpVariable(name,lowBound=0,upBound=1,cat=LpInteger) # risultato
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


"""
___________________TEST STAMPA GETMAX()
prob = LpProblem("Problema", LpMinimize)
ddds = [23,45,78,90,3,45,6]
getMax(prob,"dd",0,2000,ddds)

prob.solve()

for var in prob.variables():
        if not re.match("(^[0-9]_[0-9]_[0-9]_[0-9]_[0-9]$)", var.name) and not re.match("(^tours_[0-9]_[0-9]_[0-9]$)", var.name): #elimino variabili superflue
            print(f"{var.name} = {var.varValue}",type(var.varValue))


exit(0)
"""

"""
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
"""

try:
    sys.path.insert(0, 'instances')
    from parser import *
except:
    print("Please move into the main folder of the project :)")
    exit(0)

def main(filename):
    
    m, n, l, s, D = parseInstance(filename)


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

    #start of the problem

    second_dimension = n-m+3

    third_dimension=[i for i in range(n+1)]

    numberOfCouriers=[i for i in range(m)]

    numberOfPosition=[i for i in range(second_dimension)]

    #commentata perchè non veniva usata
    #distances = makeDict([third_dimension , third_dimension], D, 0)

    prob = LpProblem("Problema", LpMinimize)




    # Crea le variabili del problema -> parallelepipedo 3 dimensioni (n+1 per via di starting point)
    # tours = [[[LpVariable(f"tours_{i}_{j}_{k}",lowBound=0.0, upBound=1.0, cat=LpInteger) for k in range(n+1)] for j in range(second_dimension)] for i in range(m)]


    tours = LpVariable.dicts("tours", (numberOfCouriers, numberOfPosition, third_dimension), lowBound=0.0, upBound=1.0, cat=const.LpInteger)


    #vincolo di exactly one per ogni piano di una cella. un indice di consegna deve comparire exactly once
    #saltiamo il primo piano perchè è starting point (=0)
    for z in range(1,n+1):
        #vado a sommare tutto il piano
        prob += lpSum([tours[i][j][z] for j in range(second_dimension) for i in range(m)]) == 1.0
        #prob += lpSum([tours[i][j][z] for j in range(second_dimension) for i in range(m)]) <= 1

    #stesso vincolo ma sulla profondità
    for i in range(m):
        for j in range(second_dimension):
            prob += lpSum([tours[i][j][z] for z in range(n+1)]) == 1.0
            #prob += lpSum([tours[i][j][z] for z in range(n+1)]) <= 1

    #ulteriore vincolo: prima colonna solo origin point
    for i in range(m):
        prob+=tours[i][0][0] == 1.0
        #prob+=tours[i][0][0] <= 1

    #ulteriore vincolo: seconda colonna almeno un pacco
    for i in range(m):
        prob+=lpSum([tours[i][1][k] for k in range(1,n+1)]) == 1.0
        #prob+=lpSum([tours[i][1][k] for k in range(1,n+1)]) <= 1


    #check su ordine assegnamenti - no buchi
    # for i in range(m): #per ogni corriere
    #     for j in range(2,second_dimension): #mi muovo orizzontalmente sul cubo
    #         #salto la prima e la seconda (che è sempre un pacco) --- vedi foto su discord del 26/06/23 ore 12:11
    #         prob+=(lpSum([tours[i][jj][k] for jj in range(j,second_dimension)]for k in range(1,n+1))>= \
    #             (lpSum([tours[i][jjj][k] for jjj in range(second_dimension)]for k in range(1,n+1))-j+1))

    # for each courier, keep two consecutive columns and sum all the elements on each column
    # then check that the first is >= the second, if it is not the case then there is a 0 and then a 1
    # so the courier returns to the home and then deliver another item, it is not possible
    for i in range(m): #per ogni corriere
        for j in range(2,second_dimension-1): #mi muovo orizzontalmente sul cubo
            #salto la prima e la seconda (che è sempre un pacco) --- vedi foto su discord del 26/06/23 ore 12:11
            prob+=lpSum([tours[i][j][k] for k in range(1,n+1)])>= lpSum([tours[i][j+1][k] for k in range(1,n+1)])



    #checking weights, sum of the sum of the depth of our matrix (first dimension excluded), multiplied by the weight of each package, 
    # trivially if the sum is 1 then we'll get the weight as result and we have to check that the sum of all of this packages is <= capacity of the courier
    for i in range(m):
        prob+=lpSum([lpSum([tours[i][j][k] for j in range(second_dimension)])*s[k-1] for k in range(1,n+1)])<=l[i]
        

    
    distance_of_tours = [LpVariable(f"distance_of_tours_{i}",lowBound=0,upBound=upper_bound_distances,cat=LpInteger) for i in range(m)]


    # for i in range(m):
    #     prob+=distance_of_tours[i]==lpSum([tours[i][j][k]*tours[i][j+1][kk]*D[k][kk] for kk in third_dimension for k in third_dimension for j in range(second_dimension-1)])

    #this is the proof that addition can be done
    #prob+=(tours[0][1][0] + tours[0][0][1]) >=2


    #itero per ogni corriere
    for c in range(m): 
        acc_distances = [] #accumula per ogni corriere la distanza
        #itero per tutte le variabili i,j -> vista dall'alto del 3D, scorro prima la colonna e poi la riga
        for i in range(second_dimension-1): #seconda dimensione, x
            for j in range(n+1): #3a dimensione -> z
                #recupero il valore della Lp variable corrispondente a i,j
                current_i = tours[c][i][j] #recupero flag 0-1 assegnato
                #now itero sulla colonna successiva
                for jj in range(n+1): #iteriamo di nuovo su terza dimensione
                    #next_c.append

                    acc_distances.append(forceAnd(prob,f"{c}_{i}_{j}_{i+1}_{jj}",current_i,tours[c][i+1][jj])* D[j][jj])
                
        prob+= distance_of_tours[c] == lpSum(acc_distances) 

    prob.setObjective(getMax(prob,"dd",0,upper_bound_distances,distance_of_tours))

    print("-----------------")
    print(prob.objective)
    print("-----------------")

    # Risolvi il problema
    
    solver=getSolver('PULP_CBC_CMD', timeLimit=300)
    
    
    prob.solve(solver=solver)
    #0 no solution found, 1 optimal, 2 sub-optimal
    print("PROB:",prob.sol_status)
    sol_time=prob.solutionTime
    sol_status=prob.sol_status
        
    print("Status:", LpStatus[prob.status])
    # prob.roundSolution(epsInt=1e0,eps=1e0) #approfondire.... 

    print("-----------------")
    for row in D:
        print(row)
    print("-----------------")

    if ('Infeasible' in str(LpStatus[prob.status])):
        pass
    else:

        #Stampa i valori delle variabili
        for var in prob.variables():
            if not re.match("(^[0-9]_[0-9]_[0-9]_[0-9]_[0-9]$)", var.name) and not re.match("(^tours_[0-9]_[0-9]_[0-9]$)", var.name): #elimino variabili superflue
                print(f"{var.name} = {var.varValue}",type(var.varValue))

            #if "distance_of_tours" in var.name:
            #    print(f"{var.name} = {var.varValue}")
            


        depthSearch=np.zeros((m,second_dimension))

        for row in range(m): #0:3
            for column in range(second_dimension): #0:7
                temp=0
                for var in prob.variables():
                    if f"tours_{row}_{column}" in var.name:
                        if var.varValue==1.0:
                            temp=int(var.name.split("_")[-1])                
                depthSearch[row][column]=temp
            
        print(depthSearch)

        obj=[]
        #stampo controcalcolo delle distanze
        for c in range(m): #per ogni corriere
            obj.append(sum([D[int(depthSearch[c,i])][int(depthSearch[c,i+1])] for i in range(second_dimension-1)]))
            #print(sum([D[int(depthSearch[c,i])][int(depthSearch[c,i+1])] for i in range(second_dimension-1)]))
            
        return sol_time,sol_status,max(obj),depthSearch


if __name__ == "__main__":
    
    try:
        fileName = sys.argv[1]
    except:
        print("Give me the name of the file like first parameter")
        exit(0)

    sol_time,sol_status,objective,tours=main(filename=fileName)
    
    bool_status= False
    
    if sol_status==1:
        bool_status=True
    
    if not bool_status:
        sol_time=300
        
    jsonData = {"MIP":{
            "time": str(int(sol_time)),
            "optimal": bool_status,
            "obj": str(objective),
            "sol": tours.tolist()
        }}
    jsonString = json.dumps(jsonData)
    print(jsonString)
