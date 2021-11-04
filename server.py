
# 0. Import socket and datetime module
import socket
from datetime import datetime


# 1. init() - sets the host and port address for the UDP Server object creation.
class UDPServer:
    """A simple UDP Server"""

    def __init__(self, host, port):
        self.host = host  # Host Address
        self.port = port  # Host port
        self.sock = None  # Host Socket

    # 2. printwt() - messages are printed with a timestamp before them. Timestamp is in this format 'YY-mm-dd
    # HH:MM:SS' <message>.
    @staticmethod
    def printwt(msg):
        """ Print message with current time stamp"""

        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{current_date_time}] {msg}')

    # 3. configure_server() - Creates a UDP socket that uses IPv4 and binds the server to a specific address.
    def configure_server(self):
        """Configure the server"""

        # 3.1. Create the UDP socket with IPv4 Addressing
        self.printwt('Creating server socket...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 3.2. Bind the server to the given address
        self.printwt(f'Binding server to {self.host}: {self.port}....')
        self.sock.bind((self.host, self.port))
        self.printwt(f'Server bound to {self.host}: {self.port}')

    # 4. wait_for_client() - Wait until you receive a message from a client. Here we'll handle only one client and
    # the we'll close the socket.
    def wait_for_client(self):
        """ Wait for a client"""

        # 4.1. Try to perform operations
        try:

            # 4.1.1. Receive data/message from client
            client_data, client_address = self.sock.recvfrom(1024)

            # 4.1.2. Handle the clients request
            self.handle_request(client_data, client_address)

        # 4.2. Handle any errors
        except OSError as err:
            print(err)

    # 5. handle_request() - Handles the clients request.
    def handle_request(self, client_data, client_address):
        """ Handle the client"""

        # 5.1. Handle the clients request
        name = client_data.decode('utf-8')

        # TODO 5.1.1 Handle request client requests. First bits are reserved for client requests types
        # 0000 = register
        # 0001 = de_register
        # 0010 = publish
        # 0011 = remove
        # 0100 = retrieve_all
        # 0101 = retrieve_info
        # 0110 = search_file
        # 0111 = download
        # 1000 = update_context

        # to remove, just an example ---------------------------------------------------------------------------------

        resp = self.get_phone_no(name)
        self.printwt(f'[ REQUEST from {client_address} ]')
        print('\n', name, '\n')

        # 6.3 Send response back to the client
        # send response to the client
        self.printwt(f'[ RESPONSE to {client_address} ]')
        self.sock.sendto(resp.encode('utf-8'), client_address)
        print('\n', resp, '\n')

    # 6. get_phone_no() - Get the phone number of the given name, is if doesn't exists return appropriate error message.

    @staticmethod
    def get_phone_no(name):
        """ Get phone no for a given name """

        phonebook = {'Alex': '1234567890', 'Bob': '1234512345'}

        if name in phonebook.keys():
            return f"{name}'s phone number is {phonebook[name]}"
        else:
            return f"No records found for {name}"

    # ---------------------------------------------------------------------------------------------------------------

    # 7. shutdown_server() - stop the server

    def shutdown_server(self):
        """ Shutdown the UDP server """

        self.printwt('Shutting down server...')
        self.sock.close()

    # 8. main() - Driver code to test the program


def main():
    """ Create a UDP Server and respond to a client's request """
    udp_server = UDPServer(socket.gethostbyname(socket.gethostname()), 3000)
    udp_server.configure_server()
    udp_server.wait_for_client()
    udp_server.shutdown_server()


if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()
