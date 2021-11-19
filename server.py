
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

        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
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

    # 7. shutdown_server() - stop the server
    def shutdown_server(self):
        """ Shutdown the UDP server """

        self.printwt('Shutting down server...')
        self.sock.close()