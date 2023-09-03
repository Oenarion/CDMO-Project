# Import the json module
import json
import os

# Define the path of the main folder
#main_folder = "results"
main_folder = "."

# Define the names of the subfolders
f1 = "DWD_R_GECODE_NOSB"
f2 = "DWD_R_GECODE_NOSB_RESTART"
f3 = "FF_CHUFFED_NOSB"
f4 = "FF_CHUFFED_SB"
f5 = "FF_R_GECODE_NOSB"
f6 = "FF_R_GECODE_SB"


# Get the list of files in the subfolders
files = os.listdir(os.path.join(main_folder, f1))

#print(files)
#exit(0)

# Loop through the files
for file in files:
    # Open the first file and load its content as a dictionary
    with open(os.path.join(main_folder, f1, file), "r") as f:
        data1 = json.load(f)

        #print(data1)
    
    # Open the second file and load its content as a dictionary
    with open(os.path.join(main_folder, f2, file), "r") as f:
        data2 = json.load(f)

    with open(os.path.join(main_folder, f3, file), "r") as f:
        data3 = json.load(f)

        #print(data1)
    
    # Open the second file and load its content as a dictionary
    with open(os.path.join(main_folder, f4, file), "r") as f:
        data4 = json.load(f)

    with open(os.path.join(main_folder, f5, file), "r") as f:
        data5 = json.load(f)

        #print(data1)
    
    # Open the second file and load its content as a dictionary
    with open(os.path.join(main_folder, f6, file), "r") as f:
        data6 = json.load(f)

#------------

    

    # Unisci le stringhe JSON dei due file in un nuovo dizionario
    combined_data = {
        "cp_domwdeg_random_gecode_no_sb": data1["cp"],
        "cp_domwdeg_random_gecode_no_sb_restart_luby": data2["cp"],
	  "cp_first_fail_chuffed_no_sb": data3["cp"],
        "cp_first_fail_chuffed_sb": data4["cp"],
        "cp_first_fail_random_gecode_no_sb": data5["cp"],
        "cp_first_fail_random_gecode_sb": data6["cp"]
    }

    #output_folder = main_folder + "/" + "MIP_COMBINED"
    output_folder = "CP_COMBINED"

    # Scrivi il nuovo dizionario in un file combined.json nella cartella di destinazione
    #output_path = os.path.join(output_folder, 'combined.json')
    output_path = os.path.join(output_folder, file)
    with open(output_path, 'w') as output_file:
        var = json.dump(combined_data, output_file, indent=4)



    # Merge the two dictionaries into one
    #data = {**data1, **data2}
    
    # Write the merged dictionary to a new file in the main folder
    #with open(os.path.join(main_folder, file), "w") as f:
    #    json.dump(data, f, indent=4)