# module gets information about each file in the working directory

import os 

#creates an empty list

files = [] 

# loops for each file in present working directory

for file_name in os.listdir(os.getcwd()): 

#assigns variable "file_info" as a dictionary with key values

    file_info = {
        "name": file_name,
        "size": os.path.getsize(file_name),
    }

#adds dictionary "file info" to the empty list "files"

    files.append(file_info)

# loops a print to screen for each dictionary in the "files" list with the file name and size

for file in files:
    print("Name:", file["name"])
    print("Size:", file["size"], "bytes")
    print("")