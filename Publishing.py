import glob
import os
import pickle

from Client_Requests_Classes import publish,remove


class Publishing:

    def __init__(self, name,file_name, list_of_files=None, list_of_files_to_remove=None):
        super().__init__('Publishing')
        if list_of_files is None:
            list_of_files = []
        # if list_of_files_to_remove is None:
        #   list_of_files_to_remove = []
        self.name = name
        self.file_name = file_name
        self.list_of_files = list_of_files
        self.list_of_files_to_remove = list_of_files_to_remove

# search for a file in a list
    def get_file(file_name, search_path):
        result = []
        # Wlaking top-down from the root
        for root, dir, files in os.walk(search_path):
            if file_name in files:
                result.append(os.path.join(root, file_name))
        return result
    # test and to be used in main
    print(get_file("file_to_upload.txt", ".\Data"))

# publish request from the client side
    def publish(self):
        self.printwt("attempt to add a file to client's list at the server")
        client_publishing_object = publish.publish_req(self.name, self.file_name)
        print(client_publishing_object.getHeader())
        publishing_object = pickle.dumps(client_publishing_object)
        self.printwt("send publishing request to server")
        self.sendToServer(publishing_object, 'publish')

# remove request from the client side
    def remove(self):
        self.printwt("attempt to remove a file to client's list at the server")
        client_remove_object = remove.remove_req(self.name, self.file_name)
        print(client_remove_object.getHeader())
        remove_object = pickle.dumps(client_remove_object)
        self.printwt("send remove request to server")
        self.sendToServer(remove_object, 'publish')



