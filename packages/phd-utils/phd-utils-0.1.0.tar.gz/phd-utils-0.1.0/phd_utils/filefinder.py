import os

class FileFinder:
    def __init__(self, folder_path, file_extension):
        self.folder_path = folder_path
        self.file_extension = file_extension

    def find_files(self):
        file_names = []
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.' + self.file_extension):
                file_names.append(file_name)
        return file_names
