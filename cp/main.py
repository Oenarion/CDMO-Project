import os
#Automated execution of cp files
print("benvenuto nello script MINIZINC!!!")
os.system("echo ciaoooo")

for i in range(20):
    num = i + 1
    stringa = ""
    if num<10:
        stringa = "inst0" + str(num) + ".dat"
    else:
        stringa = "inst" + str(num) + ".dat"

    print("eseguo: python3 cp/cp.py " + stringa)
    os.system("python3 cp/cp.py " + stringa)




