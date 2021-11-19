import socket

# All constants
BUFFER_SIZE = 1024
SERVER_ADDRESS = (socket.gethostbyname(socket.gethostname()), 3001)  # IPV4 Address of computer running this code, and port that server is listening on.
