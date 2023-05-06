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
s_dato = [3,2, 6, 8, 5, 4, 4] #weight of each item
D = [[0, 3, 3, 6, 5, 6, 6, 2], #distances
    [3, 0, 4, 3, 4, 7, 7, 3],
    [3, 4, 0, 7, 6, 3, 5, 3],
    [6, 3, 7, 0, 3, 6, 6, 4],
    [5, 4, 6, 3, 0, 3, 3, 3],
    [6, 7, 3, 6, 3, 0, 2, 4],
    [6, 7, 5, 6, 3, 2, 0, 4],
    [2, 3, 3, 4, 3, 4, 4, 0]]

s = Solver() # create a solver s

# encoding of the sizes of items
max_weight = max(s_dato) #compute the maximum weight among all items
depth_weight = math.ceil(math.log2(max_weight+1))
sizes = [[Bool(f"size{i}_{j}") for j in range(depth_weight)] for i in range(n)]
for i in range(n):
    binary_enc = bin(s_dato[i])[2:].rjust(depth_weight, '0')
    for j in range(depth_weight):
        if binary_enc[j] == '0':
            s.add(Not(sizes[i][j]))
        else:
            s.add(sizes[i][j])

# encoding of the capacity of each couriers
max_capacity = max(l) #compute the maximum capacity among all couriers
depth_capacity = math.ceil(math.log2(max_capacity+1))
capacities = [[Bool(f"capacity{i}_{j}") for j in range(depth_capacity)] for i in range(m)]
for i in range(m):
    binary_enc = bin(l[i])[2:].rjust(depth_capacity, '0')
    for j in range(depth_capacity):
        if binary_enc[j] == '0':
            s.add(Not(capacities[i][j]))
        else:
            s.add(capacities[i][j])



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

def binary_adder_(a,b,name,solver):
    # effettuo soma binaria di a + b (che sono una lista[][] di True-false)
    # somma la stessa cardinalità

    len_a = len(a)
    len_b = len(b)
    max_len = max(len_a,len_b)

    if len_a != max_len: #padding per a
        delta = max_len - len_a
        a = [Bool(f"padding_{name}_{k}") for k in range(delta)].append(a)
        
        for i in range(delta):
            solver.add(Not(a[i]))

    if len_b != max_len: #padding per b
        delta = max_len - len_b
        b = [Bool(f"padding_{name}_{k}") for k in range(delta)].append(b)

        for i in range(delta):
            solver.add(Not(a[i]))
    
    #ora abbiamo i numeri con stesso padding (cardinalità)

    d = [Bool(f"d_{name}_{k}") for k in range(max_len)]
    c = [Bool(f"c_{name}_{k}") for k in range(max_len+1)] #carry max_len+1
    
           
    solver.add(Not(c[max_len]))
    
    #ora finamente dopo un enorme preambolo faccio la somma bit-bit
    for i in reversed(range(len(d))):
        #double implication
    
        solver.add(Implies(d[i],Or(And(a[i],Not(b[i]),Not(c[i])),And(Not(a[i]),b[i],Not(c[i])),And(Not(a[i]),Not(b[i]),c[i]),And(a[i],b[i],c[i]))))
        solver.add(Implies(Or(And(a[i],Not(b[i]),Not(c[i])),And(Not(a[i]),b[i],Not(c[i])),And(Not(a[i]),Not(b[i]),c[i]),And(a[i],b[i],c[i])),d[i]))
        if(i>0):
            solver.add(Implies(c[i-1],Or(And(a[i],b[i]),And(a[i],c[i]),And(b[i],c[i]))))
            solver.add(Implies(Or(And(a[i],b[i]),And(a[i],c[i]),And(b[i],c[i])),c[i-1]))
    
    return (d.insert(0,c[-1]))


# binary_adder_(sizes[0],sizes[1],"sus",s)
# print(s.check())
# model = s.model()
# print(model)


#constraint 1: each item exactly once
for i in range(1,n+1): #iterate on 1,2,3...5
    # for each [i][j] where bin(item_index) == [j][j][:] --> add constraint exactly_once
    s.add(exactly_one(find(i,tours))) 
    

# constraint if there is the origin point, then all the number after it must be n+1
# because he have terminated the journey
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

# constraint To achieve a fair division among drivers, 
# each courier must have at least an item (because n>=m)
for i in range(m):
    tmp = []
    for k in range(depth_tours):
        tmp.append(tours[i][1][k])
    s.add(Or(tmp))

# constraint for max courier load
# sizes = [[Bool(f"size{i}_{j}") for j in range(depth_weight)] for i in range(m)]
# capacities = [[Bool(f"capacity{i}_{j}") for j in range(depth_capacity)] for i in range(m)]
# tours = [[[Bool(f"tour{i}_{j}_{k}") for k in range(depth_tours)] for j in range(n-m+3)] for i in range(m)]
        
    """
    if(len_a != len_b):
        raise Exception("cardinality difference in binary_adder") 
    """
    




def check_weight(solver):
    # 1) sommare tutti gli encoding di weight_list
    # 2) dalla somma calcolata effettuo la sottrazione con la capacity_encoding
    # 3) ritorno il bit di segno da aggiungere al solver (per capire se maggiore o minore)
    
    for i in range(m):      #number of couriers
        for j in range(1,n-m+2):       #number of packages that a courier COULD deliver
            for pair in permutations(range(1,n+1),j):     #every permutation of those packages
                x_enc=[]    
                check_list=[]
                for x in pair:  #takes every permutation and transform them in binary encoding
                    x_enc.append(bin(x)[2:].rjust(depth_tours, '0'))
                for t in range(len(x_enc)): #iteration on the binary encoding list
                    for z in range(len(x_enc[t])):  #iteration on every bit of each entry of the encoding list
                        if(x_enc[t][z]=="0"):   #checking if the bit is 0, if that's the case we add the negation of tours matrix
                            check_list.append(Not(tours[i][t][z])) #to the check list to check afterwards if the courier can deliver the packages
                        else:
                            check_list.append(tours[i][t][z])
                            
                # 1) recuperare la capacità in binario del corriere i
                # 2) effettuare la somma fra tutti gli encoding in x_enc
                # 3) sottrarre la capacità del corriere con la somma e aggiungere il not del bit di segno
                capacity=l[i]
                w_tot=0
                bit_sign=Bool(f"check_weight_{i}_{pair}")
                for p in pair:
                    w_tot+=s_dato[p-1]
                if w_tot>capacity:
                    solver.add(Not(bit_sign))
                else:
                    solver.add(bit_sign)
                    
                solver.add(Implies(And(check_list),bit_sign))
                    
            
        



# for i in range(m):
#     weight_list = []
#     for j in range(n-m+3):
#         #itero su riga i
#         weight_encoding = tours[i][j]
#         weight_list.append(weight_encoding)
check_weight(s)

        







print(s.check())

model = s.model()


print(model)




#faccio una lista di tuple
results = []

# itera attraverso le variabili del modello
for decl in model:
    
    # ottieni il nome della variabile
    name = decl.name()
    if name.startswith("tour"):

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