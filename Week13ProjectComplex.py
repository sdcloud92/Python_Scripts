import os 

def get_file_info(path=None):
    if path is None:
        path = os.getcwd()

    files = {} 

    for root, dirs, file_names in os.walk(path):
        folder_files = {}
        for file_name in file_names:
            file_info = {
                "name": os.path.join(root, file_name),
                "size": os.path.getsize(os.path.join(root, file_name))
            }
            folder_files[file_name] = file_info
        files[root] = folder_files

    return files

file_structure = get_file_info()
for folder, folder_files in file_structure.items():
    print("Folder:", folder)
    for file_name, file_info in folder_files.items():
        print(" Name:", file_info["name"])
        print(" Size:", file_info["size"], "bytes")
        print("")