import socket
from Client_Requests_Classes import register, unregister, update_contact, retrieve,publish, publish_denied,published_reply,remove_denied,remove,removed
import pickle
from datetime import datetime


class Publishing:

    def __init__(self, name, list_of_files=[], list_of_files_to_remove=[]):
        super().__init__('Publishing')
        self.name = name
        self.list_of_files = list_of_files
        self.list_of_files_to_remove = list_of_files_to_remove

# client send publish request
    def publish_request(self):
        # Send the server formatted data that it can expect for registration.
        self.printwt('Attempting to publish a file ...')

        # Create a registration object that can be sent to the server using the pickle library.
        client_publish_req_object = publish.publish_req(self.name, self.list_of_files)
        print(client_publish_req_object.getHeader())

        # create a local variable that holds the serialized registration object to keep code neat and tidy.
        p_object = pickle.dumps(client_publish_req_object)

        # send the pickled object to the server using a function we define below. #5 sendToServer().
        self.printwt('Sending registration data to server...')
        self.sendToServer(publish_object, 'register')
