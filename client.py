# 0. Import the socket and datetime module
import socket
from Client_Requests_Classes import register, unregister, update_contact, retrieve
import pickle
from datetime import datetime


# 1. init() - sets the host and port address for the UDP Server upon object creation
class Client:
    """ A simple UDP Client """

    def __init__(self, host, UDP_port, TCP_port):
        self.name = None  # Host name
        self.host = host  # Host Address
        self.UDP_port = UDP_port  # Host UDP port
        self.TCP_port = TCP_port  # Host TCP Port
        self.UDP_sock = None  # Host UDP Socket
        self.UDP_socket = None  # Host UDP Socket
        self.TCP_sock = None  # Host TCP Socket
        self.server_address = ('10.0.0.181', 3001)
      #  self.server_address = ('127.0.0.1', 3001)
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

    # TODO Send request to the server,
    # publish
    # remove
    # retrieve_all
    # retrieve_info
    # search_file
    # download - sends request to server to download from another client
    # update_context

    # 4. Interactions with the server

    # 4.1. register(name) - registers the client with the server
    def register(self, name):
        """ Send the server a register request and receive a reply """

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
    def retrieve(self):
        self.printwt('retrieving all files...')
     #   msg1 = 'Retrieve ALL Host %s\n'  % socket.gethostname()
     #   msg2 = 'Port: %s \n' % self.UDP_port
       # msg3 = 'server address %s \n' % self.server_address
       # msg = msg1 + msg2
      #  self.printwt("msg   " +msg)

        client_retrieve = retrieve.Retrieve(self.host, self.UDP_port,self.UDP_socket)
        self.printwt('Sending retrieving all request to server...')
        print(client_retrieve.getHeader())

        # save the request in a log file and send it to the server
        self.UDP_sock.sendto(pickle.dumps(client_retrieve), self.server_address)

        try:
         msg_from_server, server_address = self.UDP_sock.recvfrom(1024)
         self.printwt(msg_from_server.decode())
        except socket.timeout as err:
            self.printwt('Server did not respond, attempting to send retrieve request again')
            self.retrieve()

    # 4.3 updateContact()  - client can update their client information
    def updateContact(self, name, ip_address, udp_socket, tcp_socket):
        """ Send the server a updateContact request and receive a reply"""

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
        client_update_contact_object = update_contact.UpdateContact(name, self.host, self.UDP_port, self.TCP_port)

        # send the object to the server
        self.printwt('Sending update contact data to server...')
        print(client_update_contact_object.getHeader())
        self.UDP_sock.sendto(pickle.dumps(client_update_contact_object), self.server_address)

        # TODO maybe make this into one function.
        try:
            msg_from_server, server_address = self.UDP_sock.recvfrom(1024)
            # TODO look for the reply that matches our Request ID
            self.printwt('Received Update Contact Response')
            self.printwt(msg_from_server.decode())
        except socket.timeout as err:
            self.printwt('Server did not respond, attempting to register again')

    # 4.3 updateContact()  - client can update their client information
    def updateContact(self, name, ip_address, udp_socket, tcp_socket):
        """ Send the server a updateContact request and receive a reply"""

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
        client_update_contact_object = update_contact.UpdateContact(name, self.host, self.UDP_port, self.TCP_port)

        # send the object to the server
        self.printwt('Sending update contact data to server...')
        print(client_update_contact_object.getHeader())
        self.UDP_sock.sendto(pickle.dumps(client_update_contact_object), self.server_address)

        # TODO maybe make this into one function.
        try:
            msg_from_server, server_address = self.UDP_sock.recvfrom(1024)
            # TODO look for the reply that matches our Request ID
            self.printwt('Received Update Contact Response')
            self.printwt(msg_from_server.decode())
        except socket.timeout as err:
            self.printwt('Server did not respond, attempting to register again')

    def close_sockets(self):
        self.printwt('Closing sockets...')
        self.UDP_sock.close()
        self.TCP_sock.close()
        self.printwt('Sockets closed')


def main():
    """ Create a UDP Client, send message to a UDP server and receive reply"""
    client = Client(socket.gethostbyname(socket.gethostname()), 0, 0)
    client.configure_client()
   # client.register('Tom')
    client.retrieve()
    client.register('Tom')
    client.updateContact('Tom', socket.gethostbyname(socket.gethostname()), 4000, 5000)
    client.close_sockets()


if __name__ == '__main__':
    main()
