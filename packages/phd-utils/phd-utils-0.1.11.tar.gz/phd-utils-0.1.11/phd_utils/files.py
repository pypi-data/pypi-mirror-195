# deal with files names and paths

import os

def find_files(folder_path, file_extension):
    file_names = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.' + file_extension):
            file_names.append(file_name)
    return sorted(file_names)

def find_files_with_same_name(folder_paths, file_extensions):
    # return a list of the files that are in all the folders and have the same name, without the extension
    file_names = []
    for folder_path, file_extension in zip(folder_paths, file_extensions):
        file_names.append(find_files(folder_path, file_extension))
    # remove extension from file names
    file_names = [[file_name.split('.')[0] for file_name in file_names] for file_names in file_names]
    file_names = list(set(file_names[0]).intersection(*file_names))
    # put them in order
    file_names = sorted(file_names)
    return file_names
