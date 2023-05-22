from z3 import *
from itertools import *

def binary_encoding(num,depth):
    try:
        return bin(num)[2:].rjust(depth, '0') #most significant bit is the first one
    except:
        print("NaN")
        exit(1)

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

def check_weight(solver,n,m,s,depth_tours,depth_weight,tours,weights,capacities):       #TO CHECK
    
    for i in range(n):
        bin_enc=binary_encoding(i+1,depth_tours)        #takes the encoding the number of the package
        weight_enc=binary_encoding(s[i],depth_weight)   #takes the encoding of the weight of the package
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
        binary_sum=binary_adder_(weights[i][0],weights[i][1],f"courier{i}",solver)
        for j in range(2,n-m+3):
            binary_sum=binary_adder_(weights[i][j],binary_sum,f"courier{i}_{j}",solver)
        result=binary_subtraction(capacities[i],binary_sum,f"courierSub{i}",solver)
        solver.add(result)
             
def create_distances(solver,n,m,D,depth_tours,depth_distance,distances,tours):
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
 
def check_distances(solver,n,m,distances,maximum,index):
    binary_sum=binary_adder_(distances[index][0],distances[index][1],f"distanceAdder{index}",solver)
    for j in range(2,n-m+3):
        binary_sum=binary_adder_(distances[index][j],binary_sum,f"distanceAdder{index}_{j}",solver)
    result=binary_subtraction(maximum,binary_sum,f"distanceSub{index}",solver)
    solver.add(result)        
           
def find(index,n,m,tours,depth_tours):
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