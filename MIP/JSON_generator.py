import numpy as np
import math
from pulp import *
import re #string mather
import sys
from jsonToFile import saveJson


if __name__ == "__main__":

    #i parametri devono essere nome JSON file, numero di corrieri
    
    try:
        fileName = str(sys.argv[1])
        number_of_fake_courires = sys.argv[2]
    except:
        print("Give me the name of the file like first parameter and number of couriers as second!!! Please, thanks.")
        exit(0)

    tours = [] #initial list
    for n in range(int(number_of_fake_courires)):
        tours.append([])
        
    jsonData = {"MIP":{
            "time": "300",
            "optimal": False,
            "obj": "-1",
            "sol": tours
        }}
    jsonString = json.dumps(jsonData)
    print(jsonString)

    saveJson(sys.argv[1],jsonData)
