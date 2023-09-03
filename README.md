# CDMO-Project
A repository for the Combinatorial Decision Making and Optimization project done during the master's degree in Artificial Intelligence
The authors of this project are: Caroli Giacomo, Galfano Lorenzo and Torzi Luca.

## How to create the docker
Please go to the home directory of the project, then run
``` 
sudo docker build . -t docker-cdmo-cgt
```

## Execute the docker
<!-- The name of the docker is the one defined above (__docker-cdmo__).
Execute the image of the docker
```
sudo docker run -t docker-cdmo
```
Retrieve the id of the image of the docker
```
sudo docker ps -a
```
Then enter inside the docker using the id of the docker 
```
sudo docker exec -it $ID /bin/bash
```
-->
To run the docker and enter inside it, type
```
sudo docker run -it docker-cdmo-cgt
```

## How to run the instances
From the main folder (named __src__) we could run every instance.
### **CP**
```
python3 "cp/cp.py" "../instances/$name_file_instance" "cp/$mzn_file" "$solver"
```
__name_file_instance__ is the name of the file of the instance that we want to run (ex. __inst01.dat__). 

__mzn_file__ is the file containing the minizinc model with the search strategy we want to use. It is possible to choose between:
- MCP_cp_firstFailRand_gecode_no_sym.mzn
- MCP_cp_firstFail_chuffed_no_sym.mzn
- MCP_cp_wdegRand_gecode.mzn
- MCP_cp_firstFailRand_gecode_sym.mzn
- MCP_cp_firstFail_chuffed_sym.mzn
- MCP_cp_wdegRand_gecode_restart.mzn.

__solver__ is the solver that we want to use (it depends on the mzn file selected): it is possible to use __gecode__ or __chuffed__.

example:
```
python3 "cp/cp.py" "../instances/inst01.dat" "cp/MCP_cp_wdegRand_gecode_restart.mzn" "gecode"
```


### **SAT**
```
python3 "SAT/$file_to_run" "../instances/$name_file_instance"
```
__file_to_run__ is the main file the we want to run: it is possible to choose between __main.py__ and __main_symBreak.py__. The second one is the version with symmetry breaking.

__name_file_instance__ is the name of the file of the instance that we want to run (ex. __inst01.dat__). 

example:
```
python3 "SAT/main.py" "../instances/inst01.dat"
```

### **SMT**
```
python3 "SMT/$file_to_run" "../instances/$name_file_instance"
```
__file_to_run__ is the main file the we want to run: it is possible to choose between __main.py__ and __main_symBreak.py__. The second one is the version with symmetry breaking.

__name_file_instance__ is the name of the file of the instance that we want to run (ex. __inst01.dat__). 

example:
```
python3 "SMT/main.py" "../instances/inst01.dat"
```

### **MIP**
```
python3 "MIP/main.py" "../instances/$name_file_instance" $solver
```
__name_file_instance__ is the name of the file of the instance that we want to run (ex. __inst01.dat__). 

__solver__ is a number representing the solver we want to use:
- 1 to solve using __PULP_CBC_CMD__
- 2 to solve using __GLPK_CMD__

example:
```
python3 "MIP/main.py" "../instances/inst01.dat" 1
```
