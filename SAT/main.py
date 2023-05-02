from z3 import *
from itertools import *
import math

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
s = [3, 2, 6, 8, 5, 4, 4] #weight of each item
D = [[0, 3, 3, 6, 5, 6, 6, 2], #distances
    [3, 0, 4, 3, 4, 7, 7, 3],
    [3, 4, 0, 7, 6, 3, 5, 3],
    [6, 3, 7, 0, 3, 6, 6, 4],
    [5, 4, 6, 3, 0, 3, 3, 3],
    [6, 7, 3, 6, 3, 0, 2, 4],
    [6, 7, 5, 6, 3, 2, 0, 4],
    [2, 3, 3, 4, 3, 4, 4, 0]]

#control parameters
#depth = math.log(n+1)
depth_tours = math.ceil(math.log2(n+1))

max_weight = max(s) #compute the maximum weight among all items
depth_weight = math.ceil(math.log2(max_weight))

"""
tours: 3 boolean arrays, each position in each row is the delivery index. starting from origin point, ending in origin point
ex: [5,1,2,5]
    [5,3,5,5]
    [5,4,5,5]
"""
tours = [[[Bool(f"tour{i}_{j}_{k}") for k in range(depth_tours)] for j in range(n-m+3)] for i in range(m)]
items = [[Bool(f"item{i}_{j}") for i in range(n)] for j in range(depth_weight)]

#items index = {i} index from items list
#we should add a constraint that says that from all i,j

#def graphic_representation():
    

s = Solver() # create a solver s

#constraint 1: each item exactly once
for i in range(1,n+1): #iterate on 1,2,3...5
    s.add(exactly_one(find(i,tours))) #for each [i][j] where bin(item_index) == [j][j][:] --> add constraint exactly_once

print(s.check())

print(s.model())