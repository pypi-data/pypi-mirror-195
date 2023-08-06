import os

def find_files(folder_path, file_extension):
    file_names = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.' + file_extension):
            file_names.append(file_name)
    return file_names
