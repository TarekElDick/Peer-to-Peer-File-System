import glob
import os
import pickle

from Client_Requests_Classes import publish


class Publishing:

    def __init__(self, name, list_of_files=None, list_of_files_to_remove=None):
        super().__init__('Publishing')
        if list_of_files is None:
            list_of_files = []
        # if list_of_files_to_remove is None:
        #   list_of_files_to_remove = []
        self.name = name
        self.list_of_files = list_of_files
        self.list_of_files_to_remove = list_of_files_to_remove

# search for a file in a list
    def get_files(filename, search_path):
        result = []
        # Wlaking top-down from the root
        for root, dir, files in os.walk(search_path):
            if filename in files:
                result.append(os.path.join(root, filename))
        return result
    # test and to be used in main
    print(get_files("file_to_upload.txt", ".\Data"))
