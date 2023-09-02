import numpy as np

def printer(model,string_name,i,j):

    matrix = np.zeros((i,j))

    #print(type(model))
    # itera attraverso le variabili del modello
    #print(model.decls())

    for decl in model:
        #print(type(decl))
        
        # ottieni il nome della variabile
        name = decl.name()
        #print(name)
        if name.startswith(string_name):

            #rimuovo tour dal nome
            sub_string = name[len(string_name):]
            parts = sub_string.split("_")
            #print(parts)
            # ottieni il valore assegnato alla variabile nel modello
            val = model[decl]

            #i,j,k
            #results.append((int(parts[0]),int(parts[1])), int(val))
            matrix[int(parts[1])][int(parts[3])] = int(val.as_long())

            # stampa il nome e il valore della variabile
            #print(f"{name}: {val}")

    return matrix