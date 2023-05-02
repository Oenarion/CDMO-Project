from z3 import *
from itertools import *
import math

def at_least_one(bool_vars):
    return Or(bool_vars)

def at_most_one(bool_vars):
    return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]

def exactly_one(bool_vars):
    return at_most_one(bool_vars) + [at_least_one(bool_vars)]

#input model
m = 3 #couriers
n = 7 #items
l = [15, 10, 7] #max load per courier
s_dato = [3, 2, 6, 8, 5, 4, 4] #weight of each item
D = [[0, 3, 3, 6, 5, 6, 6, 2], #distances
    [3, 0, 4, 3, 4, 7, 7, 3],
    [3, 4, 0, 7, 6, 3, 5, 3],
    [6, 3, 7, 0, 3, 6, 6, 4],
    [5, 4, 6, 3, 0, 3, 3, 3],
    [6, 7, 3, 6, 3, 0, 2, 4],
    [6, 7, 5, 6, 3, 2, 0, 4],
    [2, 3, 3, 4, 3, 4, 4, 0]]

s = Solver() # create a solver s

# encoding of the sizes
max_weight = max(s_dato) #compute the maximum weight among all items
depth_weight = math.ceil(math.log2(max_weight+1))
sizes = [[Bool(f"size{i}_{j}") for i in range(n)] for j in range(depth_weight)]
for i in range(len(s_dato)):
    binary_enc = bin(s_dato[i])[2:].rjust(depth_weight, '0')
    for j in range(len(binary_enc)):
        if binary_enc[j] == '0':
            s.add(Not(sizes[i][j]))
        else:
            s.add(sizes[i][j])



#control parameters
#depth = math.log(n+1)
depth_tours = math.ceil(math.log2(n+1))


"""
tours: 3 boolean arrays, each position in each row is the delivery index. starting from origin point, ending in origin point
ex: [5,1,2,5]
    [5,3,5,5]
    [5,4,5,5]
"""
tours = [[[Bool(f"tour{i}_{j}_{k}") for k in range(depth_tours)] for j in range(n-m+3)] for i in range(m)]
#items index = {i} index from items list
#we should add a constraint that says that from all i,j

def find(index,tours):
    """
    per ogni [i][j] di tours, abbiamo una lista k1,k2,k3,...kn
    questa lista viene messa in AND logico dentro una parentesi (k1 & k2 & k3 ...)
    ogni k1 .. ha davanti l'operatore logico corrispondente per computare l'elemento index
    es: index = 2 bin: 0010 (meno significativo a dx)
    --> cerchiamo un numero (!k1 & !k2 & k3 & !k4)
    tutte vengono aggiunte alla list[]
    si controlla che in list sia presente exactly_once(list[])
    quindi in tutte le i,j combinazioni di tours, solo una deve "accendersi" logicamente con l'index corrispondente
    """

    list = []
    enc = bin(index) #codifica in binario di index (1..n) -> 0b10 (esempio per index = 2)
    index_encoding = enc[2:].rjust(depth_tours, '0') #portiamo con padding depth_tours (ex: 8) -> '00001000'

    #recuperiamo tutti i k elementi di un [i][j]
    #j in range(n-m+3)] for i in range(m)]
    for i in range(m):
        for j in range(n-m+3):
            #abbiamo tutti i k di depth associati a [i][j]-esimo
            sub_list = []
            for k in range(depth_tours):
                #k0,k1,k2... <--> index_encoding (stessa dimensione)
                if(index_encoding[k] == '0'):
                    sub_list.append(Not(tours[i][j][k]))
                else:
                    sub_list.append(tours[i][j][k])

            #questa sub_lista deve avere tutti gli elementi in AND logico
            #successivamente vanno aggiunti alla list[] in OR
            list.append(And(sub_list))

    return list

#constraint 1: each item exactly once
for i in range(1,n+1): #iterate on 1,2,3...5
    s.add(exactly_one(find(i,tours))) #for each [i][j] where bin(item_index) == [j][j][:] --> add constraint exactly_once

# constraint if there is the home, then all the number after it must be n+1, because he have terminated the journey
for i in range(m):
    for j in range(2, n-m+3-1):
        tmp = []
        for k in range(depth_tours): 
             tmp.append(Not(tours[i][j][k]))
        tmp2 = []
        for k in range(depth_tours): 
             tmp2.append(Not(tours[i][j+1][k]))
        s.add(Implies(And(tmp), And(tmp2)))

# constraint on the starting point
for i in range(m):
    tmp = []
    for k in range(depth_tours):
        tmp.append(Not(tours[i][0][k]))
    s.add(And(tmp))


print(s.check())

model = s.model()







#faccio una lista di tuple
results = []

# itera attraverso le variabili del modello
for decl in model:
    # ottieni il nome della variabile
    name = decl.name()

    #rimuovo tour dal nome
    sub_string = name[4:]
    parts = sub_string.split("_")

    # ottieni il valore assegnato alla variabile nel modello
    val = model[decl]

    #i,j,k
    results.append((int(parts[0]),int(parts[1]),int(parts[2]), bool(val)))
    # stampa il nome e il valore della variabile
    #print(f"{name}: {val}")


matrix = [[['0' for x in range(depth_tours)] for y in range(n-m+3)] for z in range(m)]
for r in results:
    if r[3]:
        matrix[r[0]][r[1]][r[2]] = '1'
    else:
        matrix[r[0]][r[1]][r[2]] = '0'

matrix2 = [['0' for y in range(n-m+3)] for z in range(m)]
for i in range(m):
    for j in range(n-m+3):

        string_bin = ""

        for k in range(depth_tours):
            string_bin += matrix[i][j][k]

        #conversione in dec
        matrix2[i][j] = int (string_bin,2)

for row in matrix2:
    print(row)

print(model)


"""
#tours = [[[Bool(f"tour{i}_{j}_{k}") for k in range(depth_tours)] for j in range(n-m+3)] for i in range(m)]
matrix = [[[False for _ in range(depth_tours)] for _ in range(n-m+3)] for _ in range(m)]

for var_name, value in model:
    if var_name.startswith("tour"):
        parts = var_name.split("_")
        row = int(parts[1])
        col = int(parts[2])
        layer = int(parts[3])
        matrix[row][col][layer] = value
"""