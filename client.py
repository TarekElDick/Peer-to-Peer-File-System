# 0. Import the socket and datetime module
import glob
import socket
import threading

from Client_Requests_Classes import register, unregister, update_contact, retrieve, publish, remove
import os
import pickle
from datetime import datetime
from config import BUFFER_SIZE, SERVER_ADDRESS


# 1. init() - sets the host and port address for the UDP Server upon object creation
class Client:
    def __init__(self, name, host, UDP_port, TCP_port):
        self.name = name  # Host name
        self.host = host  # Host Address
        self.UDP_port = UDP_port  # Host UDP port client always listening to
        self.TCP_port = TCP_port  # Host TCP Port client always listening to
        self.UDP_sock = None  # Host UDP Socket
        self.TCP_sock = None  # Host TCP Socket
        self.timeout = 5
        self.BUFFER_SIZE = BUFFER_SIZE
        self.SERVER_ADDRESS = SERVER_ADDRESS
        self.list_of_available_files = self.get_all_file()
        #self.file_name = file_name

    # 2. printwt() - messages are printed with a timestamp before them. Timestamp is in this format 'YY-mm-dd
    # HH:MM:SS:' <message>.
    @staticmethod
    def printwt(msg):
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print(f'[{current_date_time}] {msg}')

    # 3. configure_client() - Creates a UDP socket that uses IPv4 and binds the client to a specific address for listening.
    def configure_client(self):

        # 3.1. Create the UDP socket with IPv4 Addressing
        self.printwt('Creating UDP client socket...')
        self.UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.printwt(f'Binding UDP client...')
        self.UDP_sock.bind((self.host, self.UDP_port))
        self.UDP_port = self.UDP_sock.getsockname()[1]
        self.printwt(f'Bound UDP client to {self.host}: {self.UDP_port}')
        self.UDP_sock.settimeout(5)

        # 3.2. Create the TCP socket with IPv4 Addressing
        self.printwt('Creating TCP client socket...')
        self.TCP_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.printwt('Binding TCP client socket...')
        self.TCP_sock.bind((self.host, self.TCP_port))
        self.TCP_port = self.TCP_sock.getsockname()[1]
        self.printwt(f'Bound TCP client socket {self.host}: {self.TCP_port}')
        # TODO set time out for TCP socket and implement it.

    # 4. Interactions with the server
    # 4.1. register() - registers the client with the server.
    def register(self):

        # Send the server formatted data that it can expect for registration.
        self.printwt('Attempting to register with the server...')

        # Create a registration object that can be sent to the server using the pickle library.
        client_registration_object = register.Register(self.name, self.host, self.UDP_port, self.TCP_port)
        print(client_registration_object.getHeader())

        # create a local variable that holds the serialized registration object to keep code neat and tidy.
        register_object = pickle.dumps(client_registration_object)

        # send the pickled object to the server using a function we define below. #5 sendToServer().
        self.printwt('Sending registration data to server...')
        self.sendToServer(register_object, 'register')

    # 4.2 unregister() - unregister the client with the server.
    def unregister(self):
        self.printwt('Attempting to unregister with the server...')

        client_unregister_object = unregister.Unregister(self.name)
        print(client_unregister_object.getHeader())

        unregister_object = pickle.dumps(client_unregister_object)

        self.printwt('Sending de-registration data to the server...')
        self.sendToServer(unregister_object, 'unregister')

    # TODO 4.3 publish() - publish the file names that a client has ready to be shared
    def publish(self):
        self.printwt("attempt to add a file to client's list at the server")
        client_publishing_object = publish.publish_req(self.name, self.host, self.UDP_port, self.list_of_available_files)
        print(client_publishing_object.getHeader())
        publishing_object = pickle.dumps(client_publishing_object)
        self.printwt("send publishing request to server")
        self.sendToServer(publishing_object, 'publish')

    # TODO 4.4 remove() - remove the files that a client has already published
    def remove(self):
        self.printwt("attempt to remove a file to client's list at the server")
        client_remove_object = remove.remove_req(self.name, self.host, self.UDP_port, self.list_of_files_to_remove)
        print(client_remove_object.getHeader())
        remove_object = pickle.dumps(client_remove_object)
        self.printwt("send remove request to server")
        self.sendToServer(remove_object, 'remove')

    # 4.5 retrieveAll() - retrieve all the information from the server
    def retrieveAll(self):
        self.printwt('Attempting retrieving all information from the server...')

        client_retrieve_all_object = retrieve.Retrieve(self.name)
        print(client_retrieve_all_object.getHeader())

        retrieve_object = pickle.dumps(client_retrieve_all_object)

        self.printwt('Sending retrieving all request to server...')
        self.sendToServer(retrieve_object, 'retrieve-all')

    # TODO 4.6 retrieveInfoT() - retrieve info about a specific peer

    # TODO 4.7 searchFile() - check with Aida if that's what is required
    def get_file(file_name, search_path):
        result = []
        # Walking top-down from the root
        for root, dir, files in os.walk(search_path):
            if file_name in files:
                result.append(os.path.join(root, file_name))
            else:
                print("File Not Found")
        return result

    def get_all_file(self, DATA_FOLDER="./Data"):
        """Get all files and make a list to process each files."""
        files = []
        os.chdir(DATA_FOLDER)
        for file in glob.glob("*"):
            files.append(file)
        os.chdir("..")
        return files
    # TODO 4.8 download() -

    # 4.9 updateContact()  - client can update their client information
    def updateContact(self, ip_address, udp_socket, tcp_socket):
        # must update this clients sockets also
        self.host = ip_address
        self.UDP_port = udp_socket
        self.TCP_port = tcp_socket

        # close the old sockets and create and bind the new ones and update the binding
        self.printwt('Closing old sockets and rebinding the new ones...')
        self.UDP_sock.close()
        self.TCP_sock.close()

        self.UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDP_sock.bind((self.host, self.UDP_port))
        self.UDP_port = self.UDP_sock.getsockname()[1]
        self.printwt(f'Bound UDP client to {self.host}: {self.UDP_port}')

        self.TCP_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCP_sock.bind((self.host, self.TCP_port))
        self.TCP_port = self.TCP_sock.getsockname()[1]
        self.printwt(f'Bound TCP client socket {self.host}: {self.TCP_port}')

        self.printwt('Attempting to update contact with the server...')

        # Create the updateContact object
        client_update_contact_object = update_contact.UpdateContact(self.name, self.host, self.UDP_port, self.TCP_port)
        print(client_update_contact_object.getHeader())

        update_object = pickle.dumps(client_update_contact_object)

        # send the object to the server
        self.printwt('Sending update contact data to server...')
        self.sendToServer(update_object, 'update-contact')

    # 5. sendtoServer() - sends command to server and handles the reply as well, also helps with retransmission
    def sendToServer(self, command_object, requestType):
        flag = True
        trials = 5

        while flag:
            # try to send the command and receive a reply from the server
            try:

                if trials == 0:
                    # if we exceeded the amount of trials we exit
                    flag = False
                    break

                self.UDP_sock.sendto(command_object, self.SERVER_ADDRESS)
                self.printwt('Sent ' + requestType + ' request to server')
                # try to receive a reply from the server.
                msg_from_server, server_address = self.UDP_sock.recvfrom(self.BUFFER_SIZE)
                self.printwt(f'Received {requestType} reply from server : {server_address}')
                self.printwt(msg_from_server.decode())
                # if we received a reply, set the flag to false, so we don't try again
                flag = False

                # once we sent the request, remove from the amount of trials if reply not received.
                trials -= 1
                if trials == 0:
                    # if we exceeded the amount of trials we exit
                    flag = False
                    self.printwt('Attempted to send ' + requestType + ' request to server and failed 5 times')
                    break
            except socket.error:
                # if sending failed
                self.printwt('Failed to send ' + requestType + ' request to server')
                trials -= 1
            except socket.timeout:
                self.printwt(
                    'Failed to receive ' + requestType + ' reply from server attempting ' + str(trials) + ' more times')
                trials -= 1
            except socket.error:
                self.printwt(
                    "ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host : Server might be offline")
                trials -= 1

    def close_sockets(self):
        self.printwt('Closing sockets...')
        self.UDP_sock.close()
        self.TCP_sock.close()
        self.printwt('Sockets closed')

def handle_client_cmd(client,cmd):
    if cmd == "register":
        client.register()
    elif cmd == "unregister":
        client.unregister()
    elif cmd == "publish":
        client.publish()
    elif cmd == "remove":
        client.list_of_files_to_remove = ["file4.txt"]
        client.remove()
    else:
        print("Invalid Command! :(")


def main():
    """ Create a UDP Client, send message to a UDP server and receive reply"""
    client_name = input("Enter Client name:")
    tom = Client(client_name, socket.gethostbyname(socket.gethostname()), 4000, 5000)
    tom.configure_client()
    query = None
    while query != "exit":
        if query is not None:
            t = threading.Thread(target=handle_client_cmd, args=(tom, query))
            t.start()
            t.join()
        query = input(">")
    tom.close_sockets()


if __name__ == '__main__':
    main()
