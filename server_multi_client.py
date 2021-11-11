# 0. Import the socket,  threading, datetime, and our own server.py module
import pickle
import socket
import threading

import server
import register
from datetime import datetime

# 1. init() - call the base class (server) constructor to initialize host address and port. Use a lock to make sure
# only one thread uses the sendto() method at a time
import unregister


class serverMultiClient(server.UDPServer):
    """ A simple UDP Server for handling multiple clients """

    def __init__(self, host, port):
        super().__init__(host, port)
        self.socket_lock = threading.Lock()
        self.list_of_registered_clients = list()
        self.list_of_tuple_of_files = None

    # 2. handle_request() - Handle client's request and send back the response after acquiring lock
    def handle_request(self, client_data, client_address):
        """ Handle the client """

        self.printwt(f'Received request from client {client_address}')
        client_request = pickle.loads(client_data)

        # Find out what kind of object it is and send it to the designated function
        if isinstance(client_request, register.Register):
            self.try_registering(client_request, client_address)
        elif isinstance(client_request, unregister.Unregister):
            self.try_unregistering(client_request, client_address)
        #elif isinstance(client_request, publish.Publish):

    def try_registering(self, re_request, client_address):
        # Check if the client is already registered, if not add the client name to the list of clients, if already registered then deny the request
        if self.check_if_client(re_request):  # might be able to just send request.name.
            msg_to_client = '[REGISTER-DENIED' + ' | ' + str(re_request.rid) + ' | ' + 'Client already registered]'
            self.printwt(msg_to_client)
            self.sock.sendto(msg_to_client.encode('utf-8'), client_address)
            return

        # register the client and inform the client
        msg_to_client = '[REGISTERED' + ' | ' + str(re_request.rid) + ']'
        self.printwt(msg_to_client)
        self.list_of_registered_clients.append(re_request)
        self.sock.sendto(msg_to_client.encode('utf-8'), client_address)

    def try_unregistering(self, de_request, client_address):
        if self.check_if_client(de_request):
            # if the client is registered then unregister them
            for obj in self.list_of_registered_clients:
                if isinstance(obj, register.Register):
                    if obj.name == de_request.name:
                        # delete the client from the database/list
                        self.list_of_registered_clients.remove(obj)
                        msg_to_client = '[DE-REGISTERED' + ' | ' + str(de_request.rid) + ']'
                        self.printwt(msg_to_client)
                        self.sock.sendto(msg_to_client.encode('utf-8'), client_address)
                        return
        self.printwt('Ignoring request, client not registered')

    # TODO 5.1.1 Handle request client requests.
    # publish
    # remove
    # retrieve_all
    # retrieve_info
    # search_file
    # download
    # update_context

    def check_if_client(self, client_request):
        for obj in self.list_of_registered_clients:
            if isinstance(obj, register.Register):  # for checking if client they are all register objects but isinstance is important to allow us to call obj.name
                if obj.name == client_request.name:
                    return True
        return False

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
