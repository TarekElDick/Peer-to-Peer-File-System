# 0. Import the socket,  threading, datetime, and our own server.py module
import socket
import threading
import server
from datetime import datetime


# 1. init() - call the base class (server) constructor to initialize host address and port. Use a lock to make sure
# only one thread uses the sendto() method at a time
class serverMultiClient(server.UDPServer):
    """ A simple UDP Server for handling multiple clients """

    def __init__(self, host, port):
        super().__init__(host, port)
        self.socket_lock = threading.Lock()

    # 2. handle_request() - Handle client's request and send back the response after acquiring lock
    def handle_request(self, client_data, client_address):
        """ Handle the client """

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

        # to be removed , this is an example ------------------------------------------------------------------------
        # 2.1 Handle the request
        name = client_data.decode('utf-8')
        resp = self.get_phone_no(name)
        self.printwt(f'[ REQUEST from {client_address} ]')
        print('\n', name, '\n')

        # send response to the client
        self.printwt(f'[ RESPONSE to {client_address} ]')
        with self.socket_lock:
            self.sock.sendto(resp.encode('utf-8'), client_address)
        print('\n', resp, '\n')

        # ------------------------------------------------------------------------------------------------------------

    # 3. wait_for_client() - Override the server's wait_for_client() method to handle multiple clients by using an
    # infinite loop
    def wait_for_client(self):
        """ Wait for clients and handle their requests """

        try:
            while True:  # Keep Alive

                try:
                    data, client_address = self.sock.recvfrom(1024)

                    c_thread = threading.Thread(target=self.handle_request, args=(data, client_address))

                    c_thread.daemon = True
                    c_thread.start()

                except OSError as err:
                    self.printwt(err)

        except KeyboardInterrupt:
            self.shutdown_server()


# 4. main() - Driver code to test the program
def main():
    """ Create a UDP server and handle multiple clients simultaneously """

    udp_server_multi_client = serverMultiClient(socket.gethostbyname(socket.gethostname()), 3001)
    udp_server_multi_client.configure_server()
    udp_server_multi_client.wait_for_client()


if __name__ == '__main__':
    main()
