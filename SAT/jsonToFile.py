import json

def saveJson(filename,jsonData):
    
    directory="res/SAT/"

    filename = str(filename)

    filename = filename.split('/')[-1]

    print("primonome:",filename)

    #rimozione stringa
    if "inst0" in filename:
        filename = filename[5:6]
    else:
        filename = filename[4:6]

    print(filename) 

    jsonString = json.dumps(jsonData)
    print(jsonString)

    try:
        f = open(f"{directory}{filename}.json", "w")
        f.write(jsonString)
        f.close()
    except Exception as e:
        print(e)
        print("errore scrittura file json")