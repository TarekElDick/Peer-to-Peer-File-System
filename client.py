# 0. Import the socket and datetime module
import socket
from Client_Requests_Classes import register, unregister, update_contact, retrieve, publish
import Publishing
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
    # TODO 4.4 remove() - remove the files that a client has already published

    # 4.5 retrieveAll() - retrieve all the information from the server
    def retrieveAll(self):
        self.printwt('Attempting retrieving all information from the server...')

        client_retrieve_all_object = retrieve.Retrieve(self.name)
        print(client_retrieve_all_object.getHeader())

        retrieve_object = pickle.dumps(client_retrieve_all_object)

        self.printwt('Sending retrieving all request to server...')
        self.sendToServer(retrieve_object, 'retrieve-all')

    # TODO 4.6 retrieveInfoT() - retrieve info about a specific peer
    # TODO 4.7 searchFile() -
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
        # Create a dedicated UDP port to send data to the server. 1 port that sends, and another that receives.
        UDP_sending_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDP_sending_sock.bind((self.host, 0))
        while flag:
            # try to send the command and receive a reply from the server
            try:
                UDP_sending_sock.sendto(command_object, self.SERVER_ADDRESS)
                self.printwt('Sent ' + requestType + ' request to server')
                # once we sent the request, remove from the amount of trials if reply not received.
                trials -= 1
                if trials == 0:
                    # if we exceeded the amount of trials we exit
                    flag = False
                    self.printwt('Attempted to send ' + requestType + ' request to server and failed 5 times')
                    UDP_sending_sock.close()  # close our sending socket once we exceed the amount of trials
                    break
            except socket.error:
                # if sending failed
                self.printwt('Failed to send ' + requestType + ' request to server')
                UDP_sending_sock.close()  # close our sending socket if we fail to send.

            # try to receive a reply from the server.
            try:
                msg_from_server, server_address = self.UDP_sock.recvfrom(self.BUFFER_SIZE)
                self.printwt(f'Received {requestType} reply from server : {server_address}')
                self.printwt(msg_from_server.decode())
                # if we received a reply, set the flag to false, so we don't try again
                flag = False
                UDP_sending_sock.close()  # close our sending socket once we receive a reply.
            except socket.timeout:
                self.printwt(
                    'Failed to receive ' + requestType + ' reply from server attempting ' + str(trials) + ' more times')
            except socket.error:
                self.printwt(
                    "ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host : Server might be offline")
                UDP_sending_sock.close()  # close our sending socket when we fail
                flag = False

    def close_sockets(self):
        self.printwt('Closing sockets...')
        self.UDP_sock.close()
        self.TCP_sock.close()
        self.printwt('Sockets closed')


def main():
    """ Create a UDP Client, send message to a UDP server and receive reply"""
    tom = Client('Tom', socket.gethostbyname(socket.gethostname()), 4000, 5000)
    tom.configure_client()
    tom.register()
    tom.unregister()
    tom.register()



if __name__ == '__main__':
    main()
