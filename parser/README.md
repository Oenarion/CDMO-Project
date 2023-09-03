The parser.py file is used within the code to import .dat instances

As for the other files present, it is necessary to point out some instructions for proper use. 
When launching the single .py executor of CP/SAT/SMT/MIP, the program looks for the corresponding folder e.g. res/CP to save the output .json files. 
The individual .json files refer to the single launch (with a certain model and with a certain solver: e.g., no symmetry breaking). 
Running the code again will inevitably overwrite the previous results. 
It is therefore necessary, manually, to save the results from time to time within a hierarchical structure in which 
each folder represents a certain solver/model combination. In case you run all possible combinations, you might get a structure as follows:
```
.
+-- CP
|   +-- CP_COMBINED
|   +-- DWD_R_GECODE_NOSB
    |   +-- 1.json
    |   +-- 2.json
    |   +-- ...
|   +-- DWD_R_GECODE_NOSB_RESTART
|   +-- FF_CHUFFED_NOSB
|   +-- FF_CHUFFED_SB
|   +-- FF_R_GECODE_NOSB
|   +-- FF_R_GECODE_SB
+-- MIP
|   +-- MIP_COMBINED
|   +-- MIP_GLPK_CMD
|   +-- MIP_PULP_CBC_CMD
+-- SAT
|   +-- SAT_COMBINED
|   +-- SAT_NO_SYM_BRK
|   +-- SAT_SYM_BRK
+-- SMT
|   +-- SMT_COMBINED
|   +-- SMT_NO_SYM_BRK
|   +-- SAT_SYM_BRK
```

Within the single subdirectory, taking the combined (output) folder as a reference, it is necessary to launch the corresponding merge file 
to merge all the results of all combinations of a single modeling technology into a single .json file (as already present in the res folder, 
in which, for each instance, the different results of different combinations are given).

Once the hierarchical structure is properly constructed, in order to be in accordance with the requirements of the provided checker, 
the formatting files (digits /obj) must be executed, directly in the main folder containing CP/MIP/SAT/SMT. 
You will indeed be asked for the directory to explore, and it is simply necessary to indicate "." to explore all the folder files present in the current directory.
