# Import the json module
import json
import os

# Define the path of the main folder
#main_folder = "results"
main_folder = "."

# Define the names of the subfolders
f1 = "SMT_NO_SYM_BRK"
f2 = "SMT_SYM_BRK"

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
    

    # Unisci le stringhe JSON dei due file in un nuovo dizionario
    combined_data = {
        "smt_no_sb": data1["smt"],
        "smt_sb": data2["smt"]
    }

    #output_folder = main_folder + "/" + "MIP_COMBINED"
    output_folder = "SMT_COMBINED"

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