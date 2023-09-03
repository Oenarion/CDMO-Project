import os
import re

def process_folders_and_files(directory_path):
    for root, _, _ in os.walk(directory_path):
        for file_name in os.listdir(root):
            file_path = os.path.join(root, file_name)
            if file_path.endswith('.json') and os.path.isfile(file_path):
                replace_time_with_number(file_path)

def replace_time_with_number(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        
        # Utilizziamo espressioni regolari per cercare e sostituire il testo
        pattern = r'"time":\s+"(\d+)"'
        replacement = r'"time": \1'
        modified_content = re.sub(pattern, replacement, file_content)
        
        with open(file_path, 'w') as file:
            file.write(modified_content)
    
    except Exception as e:
        print(f"Errore durante la modifica di {file_path}: {str(e)}")

if __name__ == "__main__":
    folder_path = input("Inserisci il percorso della cartella da elaborare: ")
    process_folders_and_files(folder_path)
    print("Modifica completata.")
