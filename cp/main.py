import os
#Automated execution of cp files
print("benvenuto nello script MINIZINC!!!")
os.system("echo ciaoooo")

for i in range(10):
    num = i + 1
    stringa = ""
    if num<10:
        stringa = "inst0" + str(num) + ".dat"
    else:
        stringa = "inst" + str(num) + ".dat"

    execstr = f"python3 cp/cp.py {stringa} cp/MCP_cp_wdegRand.mzn gecode"
    #print("eseguo: python3 cp/cp.py " + stringa + " ../cp/MCP_cp_inpOrdMin.mzn" + " gecode")
    print("eseguo", execstr)
    #os.system("python3 cp/cp.py " + stringa)
    os.system(execstr)