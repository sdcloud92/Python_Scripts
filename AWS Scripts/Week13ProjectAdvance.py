
# module gets information about each file in the working directory

import os 

def get_file_info(path=None):
    if path is None:
        path = os.getcwd()
        
#creates an empty list

    files = [] 
    
#Generates all file names within a directory tree, returns name and size, adds info to dictionary

    for root, dirs, file_names in os.walk(path):
        for file_name in file_names:
            file_info = {
                "name": os.path.join(root, file_name),
                "size": os.path.getsize(os.path.join(root, file_name))
            }
            files.append(file_info)
    return files
    
# loops a print to screen for each dictionary in the "files" list with the file name and size

files = get_file_info()
for file in files:
    print("Name:", file["name"])
    print("Size:", file["size"], "bytes")
    print("")