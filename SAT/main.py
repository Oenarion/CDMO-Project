from z3 import *
from itertools import *
import math

def at_least_one_np(bool_vars):
    return Or(bool_vars)
def at_most_one_np(bool_vars, name = ""):
    return And([Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)])
def exactly_one_np(bool_vars, name = ""):
    return And(at_least_one_np(bool_vars), at_most_one_np(bool_vars, name))


def at_least_one_seq(bool_vars):
    return at_least_one_np(bool_vars)
def at_most_one_seq(bool_vars, name):
    constraints = []
    n = len(bool_vars)
    s = [Bool(f"s_{name}_{i}") for i in range(n - 1)]
    constraints.append(Or(Not(bool_vars[0]), s[0]))
    constraints.append(Or(Not(bool_vars[n-1]), Not(s[n-2])))
    for i in range(1, n - 1):
        constraints.append(Or(Not(bool_vars[i]), s[i]))
        constraints.append(Or(Not(bool_vars[i]), Not(s[i-1])))
        constraints.append(Or(Not(s[i-1]), s[i]))
    return And(constraints)
def exactly_one_seq(bool_vars, name):
    return And(at_least_one_seq(bool_vars), at_most_one_seq(bool_vars, name))

def at_least_one_he(bool_vars):
    return at_least_one_np(bool_vars)
def at_most_one_he(bool_vars, name):
    if len(bool_vars) <= 4:
        return And(at_most_one_np(bool_vars))
    y = Bool(f"y_{name}")
    return And(And(at_most_one_np(bool_vars[:3] + [y])), And(at_most_one_he(bool_vars[3:] + [Not(y)], name+"_")))
def exactly_one_he(bool_vars, name):
    return And(at_most_one_he(bool_vars, name), at_least_one_he(bool_vars))

def at_least_k_seq(bool_vars, k, name):
    return at_most_k_seq([Not(var) for var in bool_vars], len(bool_vars)-k, name)
def at_most_k_seq(bool_vars, k, name):
    constraints = []
    n = len(bool_vars)
    s = [[Bool(f"s_{name}_{i}_{j}") for j in range(k)] for i in range(n - 1)]
    constraints.append(Or(Not(bool_vars[0]), s[0][0]))
    constraints += [Not(s[0][j]) for j in range(1, k)]
    for i in range(1, n-1):
        constraints.append(Or(Not(bool_vars[i]), s[i][0]))
        constraints.append(Or(Not(s[i-1][0]), s[i][0]))
        constraints.append(Or(Not(bool_vars[i]), Not(s[i-1][k-1])))
        for j in range(1, k):
            constraints.append(Or(Not(bool_vars[i]), Not(s[i-1][j-1]), s[i][j]))
            constraints.append(Or(Not(s[i-1][j]), s[i][j]))
    constraints.append(Or(Not(bool_vars[n-1]), Not(s[n-2][k-1])))   
    return And(constraints)
def exactly_k_seq(bool_vars, k, name):
    return And(at_most_k_seq(bool_vars, k, name), at_least_k_seq(bool_vars, k, name))

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

# m = 5
# n = 20
# l = [15, 43, 42, 16, 42]
# s_dato = [5, 4, 3, 5, 6, 3, 9, 5, 6, 1, 6, 4, 8, 3, 1, 4, 8, 6, 8, 8]
# D = [  [0, 10,  5,  2, 11,  7, 20, 16,  6,  1, 18, 20, 15, 19, 17, 10, 18, 19,  6, 13, 10],
#   [20,  0, 16, 10,  7, 16, 17,  9, 16, 11,  9, 15, 13,  9, 12, 13,  8, 14,  9,  6,  6],
#   [19, 20,  0, 15, 11,  7, 18, 12, 16, 10, 19, 15, 11, 20, 18, 10, 15, 16,  7, 19, 12],
#   [17, 16, 11,  0, 19,  8, 19, 20, 14, 18, 17, 18, 16, 20, 19, 14, 20, 20, 11, 20, 17],
#   [13, 11, 12, 11,  0, 16, 20, 12, 17, 14,  9, 17, 18, 15, 11,  9, 15, 19, 19, 16, 14],
#   [17, 13,  7,  9, 16,  0, 20, 13, 14, 12, 19, 19, 11, 13, 16, 11, 14, 20,  7, 12, 16],
#   [10,  9, 13, 10, 11, 15,  0, 10,  9,  8, 10,  7,  7,  8,  5, 11,  6, 11,  6, 13,  9],
#   [15,  8, 14, 15,  4, 20, 14,  0, 19, 15,  8, 14, 17, 16, 11, 12,  8, 20, 10, 12, 14],
#   [11, 14, 14,  4, 19, 12, 15, 19,  0, 10, 18, 16, 16, 17, 15, 12, 13, 18, 13, 19, 11],
#   [10, 19, 12,  8, 15,  9, 20, 18, 16,  0, 19, 20, 17, 19, 18, 12, 18, 18,  7, 14, 11],
#   [17, 10, 12, 17, 15, 19, 14, 14, 19, 17,  0,  8, 13, 10,  9, 15, 14, 15, 12, 12, 14],
#   [16,  9, 15, 12,  7, 18, 20, 10, 20, 14, 16,  0,  9, 13, 11, 10, 13,  9, 12,  8, 10],
#   [19, 17, 15, 17, 12, 10, 17, 11, 16, 16, 17, 10,  0, 12, 18, 18, 17, 11,  7,  8, 15],
#   [20, 12, 19, 11, 11, 15, 12, 18, 15, 19, 14, 12, 18,  0, 13, 19, 17, 14, 15, 13, 16],
#   [14, 12, 11,  9, 18, 16, 18, 16, 20,  8, 16, 20, 15, 17,  0,  7,  9, 18, 12, 11, 18],
#   [12, 13, 17,  8, 19, 12, 13, 19, 18,  9, 14, 19, 10, 13, 16,  0, 15, 16, 13, 15, 19],
#   [13,  7, 13, 13,  9, 14, 12,  9, 14,  7, 12, 11, 14, 15, 10, 13,  0, 19,  9,  7,  9],
#   [13, 12,  9, 15, 13, 14, 18, 13, 11, 10, 15, 14, 12, 20, 20, 10, 15,  0,  5,  6, 13],
#   [16, 17, 19, 12, 18, 14, 16, 14, 18, 17, 12, 20, 13, 16, 19, 17, 15, 16,  0, 15, 10],
#   [20, 13, 11, 10, 11, 14, 18,  9, 18, 15, 10, 16, 12, 20, 19, 11, 12, 19, 17,  0, 10],
#   [17,  9, 16, 15, 14, 11, 14, 10, 12, 15,  9, 10,  8, 18, 12, 15, 16, 19, 12,  9,  0],
#  ]

def maxNumberItem(s, l):
    max_l = max(l)
    s_copy = s.copy()
    s_copy.sort()
    tmp = 0
    i = 0
    while(tmp+s_copy[i] < max_l):
        tmp = tmp + s_copy[i]
        i += 1
    return i

s = Solver() # create a solver s

# encoding of the sizes of items
max_weight = max(s_dato) #compute the maximum weight among all items
depth_weight = math.ceil(math.log2(max_weight+1))
# sizes = [[Bool(f"size{i}_{j}") for j in range(depth_weight)] for i in range(n)]
# for i in range(n):
#     binary_enc = bin(s_dato[i])[2:].rjust(depth_weight, '0')
#     for j in range(depth_weight):
#         if binary_enc[j] == '0':
#             s.add(Not(sizes[i][j]))
#         else:
#             s.add(sizes[i][j])

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

weights=[[[Bool(f"weight{i}_{j}_{k}") for k in range(depth_weight)] for j in range(n-m+3)] for i in range(m)]

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
    # for each [i][j] where bin(item_index) == [j][j][:] --> add constraint exactly_once
    s.add(exactly_one_np(find(i,tours)))

def binary_adder_2(a,b,name,solver):
    # effettuo soma binaria di a + b (che sono una lista[][] di True-false)
    # somma la stessa cardinalità

    len_a = len(a)
    len_b = len(b)
    max_len = max(len_a,len_b)

    if len_a != max_len: #padding per a
        delta = max_len - len_a
        a1 = [Bool(f"paddingAdd1_{name}_{k}") for k in range(delta)]
        a1.extend(a)
        a=a1
        
        for i in range(delta):
            solver.add(Not(a[i]))

    if len_b != max_len: #padding per b
        delta = max_len - len_b
        b1 = [Bool(f"paddingAdd2_{name}_{k}") for k in range(delta)]
        b1.extend(b)
        b=b1
        
        for i in range(delta):
            solver.add(Not(b[i]))
    
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
    
    d.insert(0,c[-1])
    return (d)

def binary_adder_(a,b,name,solver):
    # effettuo soma binaria di a + b (che sono una lista[][] di True-false)
    # somma la stessa cardinalità

    len_a = len(a)
    len_b = len(b)
    max_len = max(len_a,len_b)

    if len_a != max_len: #padding per a
        delta = max_len - len_a
        a1 = [Bool(f"paddingAdd1_{name}_{k}") for k in range(delta)]
        a1.extend(a)
        a=a1
        
        for i in range(delta):
            solver.add(Not(a[i]))

    if len_b != max_len: #padding per b
        delta = max_len - len_b
        b1 = [Bool(f"paddingAdd2_{name}_{k}") for k in range(delta)]
        b1.extend(b)
        b=b1
        
        for i in range(delta):
            solver.add(Not(b[i]))
    
    #ora abbiamo i numeri con stesso padding (cardinalità)

    d = [Bool(f"d_{name}_{k}") for k in range(max_len)]
    c = [Bool(f"c_{name}_{k}") for k in range(max_len+1)] #carry max_len+1
    
    solver.add(Not(c[max_len]))
    
    #ora finamente dopo un enorme preambolo faccio la somma bit-bit
    for i in range(len(d)):
        #double implication
        solver.add((d[i] == \
                    Or(And(a[i],Not(b[i]),Not(c[i])),\
                        And(Not(a[i]),b[i],Not(c[i])),\
                        And(Not(a[i]),Not(b[i]),c[i]),\
                        And(a[i],b[i],c[i]))))

        if(i>0):
            solver.add(c[i-1] ==\
                Or(And(a[i],b[i]),And(a[i],c[i]),And(b[i],c[i])))
    
    d.insert(0,c[0])
    return (d)




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


# constraint to have the exact number of 0 in the matrix       
bool_vars = [[tours[i][j] for j in range(n-m+3)] for i in range(m)]
s.add(at_least_k_seq(bool_vars=find(0,tours), k=(n-m+3)*m-n, name="at_least_k_0"))

# constraint for max courier load
# sizes = [[Bool(f"size{i}_{j}") for j in range(depth_weight)] for i in range(m)]
# capacities = [[Bool(f"capacity{i}_{j}") for j in range(depth_capacity)] for i in range(m)]
# tours = [[[Bool(f"tour{i}_{j}_{k}") for k in range(depth_tours)] for j in range(n-m+3)] for i in range(m)]
        
"""
    if(len_a != len_b):
        raise Exception("cardinality difference in binary_adder") 
"""
    




def check_weight2(solver):
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
                            check_list.append(Not(tours[i][t+1][z])) #to the check list to check afterwards if the courier can deliver the packages
                        else:
                            check_list.append(tours[i][t+1][z])
                            
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
                    
            
def check_weight(solver):
    
    for i in range(n):
        bin_enc=binary_encoding(i+1,depth_tours)        #takes the encoding the number of the package
        weight_enc=binary_encoding(s_dato[i],depth_weight)   #takes the encoding of the weight of the package
        for j in range(m):
            for k in range(n-m+3):
                check_list=[]
                for t in range(len(bin_enc)): #iteration on every bit of the binary encoding
                    if(bin_enc[t]=="0"):   #checking if the bit is 0, if that's the case we add the negation of tours matrix
                        check_list.append(Not(tours[j][k][t])) #to the check list to check afterwards if the courier can deliver the packages
                    else:
                        check_list.append(tours[j][k][t])
                check_weight_list=[]
                for t in range(len(weight_enc)): #doing the same thing on weights
                    if(weight_enc[t]=="0"):   
                        check_weight_list.append(Not(weights[j][k][t])) 
                    else:
                        check_weight_list.append(weights[j][k][t])
                solver.add(Implies(And(check_list),And(check_weight_list)))
    
    zero_enc=binary_encoding(0,depth_tours)
    zero_weight_enc=binary_encoding(0,depth_weight)
    
    for j in range(m):
        for k in range(n-m+3):
            zero_check=[]
            for t in range(len(zero_enc)): #iteration on every bit of the binary encoding
                zero_check.append(Not(tours[j][k][t])) #to the check list to check afterwards if the courier can deliver the packages
            check_weight_zero_list=[]
            for t in range(len(zero_weight_enc)): #doing the same thing on weights  
                check_weight_zero_list.append(Not(weights[j][k][t])) 
            solver.add(Implies(And(zero_check),And(check_weight_zero_list)))

    for i in range(m):
        temp=[]
        # courier_weight=binary_encoding(l[i],depth_capacity)
        temp=binary_adder_(weights[i][0],weights[i][1],f"courier{i}",solver)
        for j in range(2,n-m+3):
            temp=binary_adder_(weights[i][j],temp,f"courier{i}_{j}",solver)
        result=binary_subtraction(capacities[i],temp,f"courierSub{i}",solver)
        solver.add(result)
        

max_distance = max(max(D, key=lambda x: max(x))) #compute the maximum distance among all the distances
depth_distance = math.ceil(math.log2(max_distance+1))
distances = [[[Bool(f"distance{i}_{j}_{k}") for k in range(depth_distance)] for j in range(n-m+2)] for i in range(m)]
def checkDistances(solver):
    for i in range(n+1):
        bin_enc1 = binary_encoding(i, depth_tours) #takes the encoding the number of the package
        for j in range(n+1):
            bin_enc2 = binary_encoding(j, depth_tours)
            if i>0 and j>0:
                distance = D[i-1][j-1]
            elif i>0:
                distance = D[i-1] [-1]
            else:
                distance = D[-1][j-1]
            #print(distance)
            bin_enc_distance = binary_encoding(distance, depth_distance)
            
            for x in range(m):
                for y in range(n-m+2):
                    bool_distance_enc = []
                    for t in range(len(bin_enc_distance)): #doing the same thing on weights  
                        if(bin_enc_distance[t] == "0"):   
                            bool_distance_enc.append(Not(distances[x][y][t])) 
                        else:
                            bool_distance_enc.append(distances[x][y][t])

                    bool_enc1 = []
                    bool_enc2 = []
                    for z in range(depth_tours):
                        if bin_enc1[z] == '0':
                            bool_enc1.append(Not(tours[x][y][z]))
                        else:
                            bool_enc1.append(tours[x][y][z])
                    for z in range(depth_tours):
                        if bin_enc2[z] == '0':
                            bool_enc2.append(Not(tours[x][y+1][z]))
                        else:
                            bool_enc2.append(tours[x][y+1][z])
                    
                    solver.add(Implies(And(And(bool_enc1),And(bool_enc2)), And(bool_distance_enc)))

def binary_subtractio2n(enc1,enc2,name,solver):
    len_a = len(enc1)
    len_b = len(enc2)
    max_len = max(len_a,len_b)+1

    reversed_enc=[]

    delta = max_len - len_a
    a = [Bool(f"paddingSub1_{name}_{k}") for k in range(delta)]
    a.extend(enc1)
    
        
    for i in range(delta):
        solver.add(Not(a[i]))
    
    delta=max_len - len_b
    b = [Bool(f"paddingSub2_{name}_{k}") for k in range(delta)]
    b.extend(enc2)

    for i in b:
        reversed_enc.append(Not(i))    
    
    
    bool = [Bool(f"{name}_bit_to_add") for j in range(1)]
    solver.add(bool)
    reversed_enc=binary_adder_(reversed_enc,bool,f"{name}_temp",solver)
    
    # for i in range(delta):
    #     solver.add(reversed_enc[i])

    return binary_adder_(a,reversed_enc,f"final{name}",solver)[0]   #returns the carry out, 1 if positive, 0 if not
    
def binary_subtraction(enc1,enc2,name,solver):
    len_a = len(enc1)
    len_b = len(enc2)
    max_len = max(len_a,len_b)+1

    delta = max_len - len_a
    a = [Bool(f"paddingSub1_{name}_{k}") for k in range(delta)]
    a.extend(enc1)
    
        
    for i in range(delta):
        solver.add(Not(a[i]))
    
    delta=max_len - len_b
    b = [Bool(f"paddingSub2_{name}_{k}") for k in range(delta)]
    b.extend(enc2)

    for i in range(delta):
        solver.add(Not(b[i]))

    # reversed_enc=[Bool(f"reverse_enc{name}_{i}") for i in range(len(b))]
    # for i in range(len(b)):
    #     solver.add(Implies(b[i], Not(reversed_enc[i])))
    #     solver.add(Implies(Not(b[i]), reversed_enc[i]))    
    reversed_enc=[]
    for i in b:
        reversed_enc.append(Not(i))
    
    
    bool = [Bool(f"{name}_bit_to_add") for j in range(1)]
    solver.add(bool)
    complement2 = binary_adder_(reversed_enc,bool,f"{name}_temp",solver)
    # removing the bit added during the operation, because during the 2'complement operation we must mantein the same number of bits 
    complement2[len(complement2)-len(reversed_enc):]
    # for i in range(delta):
    #     solver.add(reversed_enc[i])

    return binary_adder_(a,reversed_enc,f"final_{name}",solver)[0]   #returns the carry out, 1 if positive, 0 if not
    



def binary_encoding(num,depth):
    try:
        return bin(num)[2:].rjust(depth, '0') #most significant bit is the first one
    except:
        print("NaN")
        exit(1)
# for i in range(m):
#     weight_list = []
#     for j in range(n-m+3):
#         #itero su riga i
#         weight_encoding = tours[i][j]
#         weight_list.append(weight_encoding)





def printer(model,string_name,i,j,k):
    #faccio una lista di tuple
    results = []

    # itera attraverso le variabili del modello
    for decl in model:
        
        # ottieni il nome della variabile
        name = decl.name()
        if name.startswith(string_name):

            #rimuovo tour dal nome
            sub_string = name[len(string_name):]
            parts = sub_string.split("_")

            # ottieni il valore assegnato alla variabile nel modello
            val = model[decl]

            #i,j,k
            results.append((int(parts[0]),int(parts[1]),int(parts[2]), bool(val)))
            # stampa il nome e il valore della variabile
            #print(f"{name}: {val}")


    matrix = [[['0' for x in range(k)] for y in range(j)] for z in range(i)]
    for r in results:
        if r[3]:
            matrix[r[0]][r[1]][r[2]] = '1'
        else:
            matrix[r[0]][r[1]][r[2]] = '0'

    matrix2 = [['0' for y in range(j)] for z in range(i)]
    for x in range(i):
        for y in range(j):

            string_bin = ""

            for z in range(k):
                string_bin += matrix[x][y][z]

            #conversione in dec
            matrix2[x][y] = int (string_bin,2)
    print(string_name)
    for row in matrix2:
        print(row)



def printGivenName(model, nameGiven):
    for decl in model:
        # ottieni il nome della variabile
        name = decl.name()
        if (nameGiven in name):
            val = model[decl]
            print(f"{name} = {val}")

check_weight(s)
checkDistances(s)

print(s.check())


model = s.model()
f = open("demofile2.txt", "w")
f.write(str(model))
f.close()
#printGivenName(model, "final")
printer(model,"weight",m,n-m+3,depth_weight)
printer(model,"tour",m,n-m+3,depth_tours)
printer(model, "distance", m, n-m+2, depth_distance)

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