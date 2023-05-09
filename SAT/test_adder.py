from z3 import *

s = Solver() # create a solver s

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

    reversed_enc=[Bool(f"reverse_enc{name}_{i}") for i in range(len(b))]
    for i in range(len(b)):
        solver.add(Implies(b[i], Not(reversed_enc[i])))
        solver.add(Implies(Not(b[i]), reversed_enc[i]))    
    
    
    bool = [Bool(f"{name}_bit_to_add") for j in range(1)]
    solver.add(bool)
    reversed_enc=binary_adder_(reversed_enc,bool,f"{name}_temp",solver)
    print(reversed_enc)
    # for i in range(delta):
    #     solver.add(reversed_enc[i])

    return binary_adder_(a,reversed_enc,f"final_{name}",solver)[0]   #returns the carry out, 1 if positive, 0 if not
    

def binary_encoding(num,depth):
    try:
        return bin(num)[2:].rjust(depth, '0') #most significant bit is the first one
    except:
        print("NaN")
        exit(1)

def codifica(solver, var, num, depth):
    num_enc = binary_encoding(num, depth)
    for i in range(len(num_enc)):
        if num_enc[i] == '0':
            solver.add(Not(var[i]))
        else: 
            solver.add(var[i])

a1 = [Bool(f"a1{k}") for k in range(4)]
a2 = [Bool(f"a2{k}") for k in range(6)]
a3 = [Bool(f"a3{k}") for k in range(6)]

b1 = codifica(s, a1, 2, len(a1))
b2 = codifica(s, a2, 10, len(a2))
b3 = codifica(s, a3, 2, len(a3))

# names = binary_adder_(a1,a2,"a12", s)
binary_subtraction(a1, a2, "a12", s)

s.check()
model = s.model()
print(model)

# for decl in model:
#     name = decl.name()
#     for n in names:
#         if str(n) == name:
#             val = model[decl]
#             print(f"{decl.name()} = {val}")
        
