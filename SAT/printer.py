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
    
    return matrix2

def getMatrix(model,string_name,i,j,k):
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
    
    return matrix2

def printGivenName(model, nameGiven):
    for decl in model:
        # ottieni il nome della variabile
        name = decl.name()
        if (nameGiven in name):
            val = model[decl]
            print(f"{name} = {val}")
