from z3 import *

s = Solver() # create a solver s

from arithmetic_op import *

a0 = Bool("a0")
a1 = Bool("a1")
a2 = Bool("a2")
a3 = Bool("a3")
s.add(Not(a0))
s.add(Not(a1))
s.add(a2)
s.add(a3)

a = [a0,a1,a2]

b0 = Bool("b0")
b1 = Bool("b1")
b2 = Bool("b2")
b3 = Bool("b3")
s.add(Not(b0))
s.add(b1)
s.add(Not(b2))
s.add(b3)

b = [b0,b1,b2]

#res = binary_adder_(a,b,"testAdder", s)
res = binary_subtraction(a, b, "testAdder", s)

s.check()
model = s.model()

for decl in model:
        
        # ottieni il nome della variabile
        name = decl.name()
        if "testAdder" in name :

            # ottieni il valore assegnato alla variabile nel modello
            val = model[decl]
            print(name, val)