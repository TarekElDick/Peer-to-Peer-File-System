import socket

# All constants
UDP_TIMEOUT = 5
TCP_TIMEOUT = 5
BUFFER_SIZE = 1024

# UPDATE THE IPV4 ADDRESS OF THE SERVER
# if running both server and client on same machine
SERVER_ADDRESS = (socket.gethostbyname(socket.gethostname()), 3001)

# if running on separate machines just put the server ip here
# SERVER_ADDRESS = ('', 3001)
