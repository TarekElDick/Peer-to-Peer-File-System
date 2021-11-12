# 0. Import the socket and datetime module
import socket
import register
import unregister
import pickle
from datetime import datetime

class MyException(Exception):
    pass
# 1. init() - sets the host and port address for the UDP Server upon object creation
class Client:
    """ A simple UDP Client """

    def __init__(self, host, UDP_port, TCP_port):
        self.name = None  # Host name
        self.host = host  # Host Address
        self.UDP_port = UDP_port  # Host UDP port
        self.TCP_port = TCP_port  # Host TCP Port
        self.UDP_sock = None  # Host UDP Socket
        self.TCP_sock = None  # Host TCP Socket
        self.server_address = ('192.168.0.198', 3001)
        self.timeout = 5  # TODO still not implemented

    # 2. printwt() - messages are printed with a timestamp before them. Timestamp is in this format 'YY-mm-dd
    # HH:MM:SS:' <message>.
    @staticmethod
    def printwt(msg):
        """ Print message with current time stamp"""

        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print(f'[{current_date_time}] {msg}')

    # 3. configure_client() - Creates a UDP socket that uses IPv4 and binds the server to a specific address.
    # socket.SOCK.DGRAM specifies that the connection type will be UDP
    # socket.AF_INET specifies that IPv4 will be used for addressing.
    def configure_client(self):
        """Configure the client to use UDP protocol with IPv4 addressing"""

        # 3.1. Create the UDP socket with IPv4 Addressing
        self.printwt('Creating UDP client socket...')
        self.UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.printwt(f'Binding UDP client...')
        self.UDP_sock.bind((self.host, self.UDP_port))
        self.UDP_port = self.UDP_sock.getsockname()[1]
        self.printwt(f'Bound UDP client to {self.host}: {self.UDP_port}')

        self.printwt('Creating TCP client socket...')
        self.TCP_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.printwt('Binding TCP client socket...')
        self.TCP_sock.bind((self.host, self.TCP_port))
        self.TCP_port = self.TCP_sock.getsockname()[1]
        self.printwt(f'Bound TCP client socket {self.host}: {self.TCP_port}')
        self.choice()
    # TODO Send request to the server,
    # publish
    # remove
    # retrieve_all
    # retrieve_info
    # search_file
    # download - sends request to server to download from another client
    # update_context
    def choice(self):
        actions = { '1':self.register,
                    '2':self.unregister,
                    '3':self.publish,
                    '4':self.retrieve_all,
                    '5':self.search,
                    '6':self.download,
                    '7':self.update_contact,
                    '8':self.close_sockets

        }
        while True:
            try:
                commands = input('\n1)Register, 2)Unregister, 3)Publish, 4)Retrieve_all, '
                                 '5) Search, 6) Download, 7) Update_Contact, '
                                 '8) Close_Socket \n Enter your request: ')
                actions.setdefault(commands, 'wrong input')()
            except MyException as e:
                print(e)

            except BaseException:
                self.close_sockets()
    # 4. Interactions with the server

    # 4.1. register(name) - registers the client with the server
    #def register(self, name):
    def register(self):
        """ Send the server a register request and receive a reply """
        name ='Tommy'
        # Send the server formatted data that it can expect for registration
        self.printwt('Attempting to register with the server...')
        client_registration_object = register.Register(name, self.host, self.UDP_port,
                                                       self.TCP_port)
        self.printwt('Sending registration data to server...')
        print(client_registration_object.getHeader())

        # TODO ( save the request in a log ) and send it to the server
        self.UDP_sock.sendto(pickle.dumps(client_registration_object), self.server_address)
        self.printwt('Sent Registration Data')
        # TODO Wait for server to respond, if no response send it again

        try:
            msg_from_server, server_address = self.UDP_sock.recvfrom(1024)
            # TODO look for the reply that matches our Request ID
            self.printwt('Received Registration Response')
            self.printwt(msg_from_server.decode())
        except socket.timeout as err:
            self.printwt('Server did not respond, attempting to register again')
            self.register(self.name)

    # 4.2 unregister(name) - unregister the client with the server
    def unregister(self, name):
        """ Send the server a unregister request and receive a reply"""

        self.printwt('Attempting to unregister with the server...')
        client_unregister_object = unregister.Unregister(name)

        self.printwt('Sending de-registration data to server...')
        print(client_unregister_object.getHeader())

        # TODO ( save the request in a log ) and send it to the server
        self.UDP_sock.sendto(pickle.dumps(client_unregister_object), self.server_address)
        self.printwt('Sent De-registration Data')
        # TODO Wait for server to respond, if no response send it again

        # TODO maybe make this into one function.
        try:
            msg_from_server, server_address = self.UDP_sock.recvfrom(1024)
            # TODO look for the reply that matches our Request ID
            self.printwt('Received De-Registration Response')
            self.printwt(msg_from_server.decode())
        except socket.timeout as err:
            self.printwt('Server did not respond, attempting to register again')
            self.unregister(self.name)

    def publish(self):
        self.printwt('Publishing file...')
        # To add logic later

    def retrieve_all(self):
            self.printwt('Retrieving all files...')
            # To add logic later

    def search(self):
        self.printwt('Searching files...')
        # To add logic later

    def download(self):
            self.printwt('Downloading file...')
            # To add logic later

    def update_contact(self):
        self.printwt('Updating Contact...')
        # To add logic later


    def close_sockets(self):
        self.printwt('Closing sockets...')
        self.UDP_sock.close()
        self.TCP_sock.close()
        self.printwt('Sockets closed')


def main():
    """ Create a UDP Client, send message to a UDP server and receive reply"""
    client = Client(socket.gethostbyname(socket.gethostname()), 0, 0)
    client.configure_client()
    #client.register('Tom')
    #client.unregister('Tom')
    #client.unregister('Tom')
    #client.close_sockets()


if __name__ == '__main__':
    main()
