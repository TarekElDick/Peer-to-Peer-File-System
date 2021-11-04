# 0. Import the socket and datetime module
import socket
from datetime import datetime


# 1. init() - sets the host and port address for the UDP Server upon object creation
class UDPClient:
    """ A simple UDP Client """

    def __init__(self, host, port):
        self.host = host  # Host Address
        self.port = port  # Host port
        self.sock = None  # Host Socket

    # 2. printwt() - messages are printed with a timestamp before them. Timestamp is in this format 'YY-mm-dd
    # HH:MM:SS' <message>.
    @staticmethod
    def printwt(msg):
        """ Print message with current time stamp"""

        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:#S')
        print(f'[{current_date_time}] {msg}')

    # 3. configure_client() - Creates a UDP socket that uses IPv4 and binds the server to a specific address.
    # socket.SOCK.DGRAM specifies that the connection type will be UDP
    # socket.AF_INET specifies that IPv4 will be used for addressing.
    def configure_client(self):
        """Configure the client to use UDP protocol with IPv4 addressing"""

        # 3.1. Create the UDP socket with IPv4 Addressing
        self.printwt('Creating client socket...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.printwt('Client socket created')

    # 4. interact_with_server() - Send name to server and receive phone number from server
    def interact_with_server(self):
        """ Send request to a UDP Server and receive reply from it"""

        # 4.1. Try to perform operations
        try:

            # 4.1.1. TODO Send request to the server, First bits are reserved for client requests types
            # 0000 = register
            # 0001 = de_register
            # 0010 = publish
            # 0011 = remove
            # 0100 = retrieve_all
            # 0101 = retrieve_info
            # 0110 = search_file
            # 0111 = download
            # 1000 = update_context

            # to remove, just an example  ---------------------------------------------------------------------------

            # send data to server
            self.printwt('Sending name to the server to get phone number')
            name = 'Alex'
            self.sock.sendto(name.encode('utf-8'), (self.host, 3000))
            self.printwt('[ SENT ]')
            print('\n', name, '\n')

            # -------------------------------------------------------------------------------------------------------

            # 4.1.2 TODO Receive response from server.

            # to remove, just an example ----------------------------------------------------------------------------

            # receive data from server
            resp, server_address = self.sock.recvfrom(1024)
            self.printwt('[ Received ]')
            print('\n', resp.decode(), '\n')
            self.printwt('Interaction completed successfully...')

            # -------------------------------------------------------------------------------------------------------\

        # 4.2. Handle any errors
        except OSError as err:
            print(err)

        # 4.3 Close the socket
        finally:
            # close socket
            self.printwt('Closing socket...')
            self.sock.close()
            self.printwt('Socket closed')


def main():
    """ Create a UDP Client, send message to a UDP server and receive reply"""

    udp_client = UDPClient(socket.gethostbyname(socket.gethostname()), 4444)
    udp_client.configure_client()
    udp_client.interact_with_server()


if __name__ == '__main__':
    main()
