# 0. Import the socket,  threading, datetime, and our own server.py module
import pickle
import threading

import server
from config import SERVER_ADDRESS

from Client_Requests_Classes.register import Register
from Client_Requests_Classes.unregister import Unregister
from Client_Requests_Classes.update_contact import UpdateContact
from Client_Requests_Classes.publish import publish_req
from Client_Requests_Classes.remove import remove_req


# 1. init() - call the base class (server) constructor to initialize host address and port. Use a lock to make sure
# only one thread uses the sendto() method at a time
class serverMultiClient(server.UDPServer):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.socket_lock = threading.Lock()
        self.list_of_registered_clients = list()
        self.list_of_client_files = list()
        self.list_of_acknowledgements = list()

    # 2. handle_request() - Handle client's request and send back the response after acquiring lock
    def handle_request(self, client_data, client_address):

        self.printwt(f'Received request from client {client_address}')
        client_request = pickle.loads(client_data)

        # Find out what kind of object it is and send it to the designated function
        if isinstance(client_request, Register):
            if not self.check_if_already_ack(client_request):
                self.try_registering(client_request)
            return
        elif isinstance(client_request, Unregister):
            if not self.check_if_already_ack(client_request):
                self.try_unregistering(client_request)
        elif isinstance(client_request, UpdateContact):
            if not self.check_if_already_ack(client_request):
                self.try_updatingContact(client_request)
        elif isinstance(client_request, publish_req):
            if not self.check_if_already_ack(client_request):
                self.try_publishing(client_request)
        elif isinstance(client_request, remove_req):
            if not self.check_if_already_ack(client_request):
                self.try_removeFile(client_request)

    def try_registering(self, re_request):
        print(re_request.getHeader())
        client_address = (re_request.host, re_request.udp_socket)

        # Check if the client is already registered, if not add the client name to the list of clients, if already
        # registered then deny the request
        if self.check_if_client(re_request):
            msg_to_client = '[REGISTER-DENIED' + ' | ' + str(re_request.rid) + ' | ' + 'Client already registered]'
            self.printwt(msg_to_client)

            array_to_append = [re_request.name, re_request.rid, msg_to_client, client_address]
            self.list_of_acknowledgements.append(array_to_append)

            self.sock.sendto(msg_to_client.encode('utf-8'), client_address)
            return
        else:
            # register the client and inform the client
            msg_to_client = '[REGISTERED' + ' | ' + str(re_request.rid) + ']'
            self.printwt(msg_to_client)

            array_to_append = [re_request.name, re_request.rid, msg_to_client, client_address]
            self.list_of_acknowledgements.append(array_to_append)

            self.list_of_registered_clients.append(re_request)
            self.sock.sendto(msg_to_client.encode('utf-8'), client_address)
            return

    def try_unregistering(self, de_request):
        print(de_request.getHeader())
        if self.check_if_client(de_request):
            client_address = self.get_client_udp_address(de_request)
            # if the client is registered then unregister them
            for obj in self.list_of_registered_clients:
                if isinstance(obj, Register):
                    if obj.name == de_request.name:
                        # delete the client from the database/list
                        self.list_of_registered_clients.remove(obj)
                        msg_to_client = '[DE-REGISTERED' + ' | ' + str(de_request.rid) + ']'
                        self.printwt(msg_to_client)

                        array_to_append = [de_request.name, de_request.rid, msg_to_client, client_address]
                        self.list_of_acknowledgements.append(array_to_append)

                        self.sock.sendto(msg_to_client.encode('utf-8'), client_address)
                        return
        self.printwt('Ignoring request, client not registered')
        return

    def try_updatingContact(self, up_request):
        client_address = self.get_client_udp_address(up_request)
        if self.check_if_client(up_request):
            # if the client is registered then we can update the register object
            for obj in self.list_of_registered_clients:
                if isinstance(obj, Register):  # for checking if client they are all register objects but
                    # isinstance is important to allow us to call obj.name
                    if obj.name == up_request.name:
                        obj.host = up_request.host
                        obj.udp_socket = up_request.udp_socket
                        obj.tcp_socket = up_request.tcp_socket
                        msg_to_client = '[UPDATE-CONFIRMED' + ' | ' + str(up_request.rid) + ' | ' + str(
                            up_request.name) + ' | ' + str(up_request.host) + ' | ' + str(
                            up_request.udp_socket) + ' | ' + str(up_request.tcp_socket) + ']'
                        self.printwt(msg_to_client)

                        array_to_append = [up_request.name, up_request.rid, msg_to_client, client_address]
                        self.list_of_acknowledgements.append(array_to_append)

                        self.sock.sendto(msg_to_client.encode('utf-8'), client_address)

        else:
            msg_to_client = '[UPDATE-DENIED' + ' | ' + str(up_request.rid) + ' | ' + str(
                up_request.name) + ' | ' + 'Name does not Exist]'
            self.printwt(msg_to_client)

            array_to_append = [up_request.name, up_request.rid, msg_to_client, client_address]
            self.list_of_acknowledgements.append(array_to_append)

            self.sock.sendto(msg_to_client.encode('utf-8'), client_address)

    def try_publishing(self, up_request):
        print(up_request.getHeader())
        client_address = (up_request.host, up_request.udp_socket)

        # Check if the client is already registered,add the file to list of files
        # if not add deny the request
        if self.check_if_client(up_request):
            #  check if the file already published
            if up_request not in self.list_of_client_files:
                self.list_of_client_files.append(up_request)
                msg_to_client = '[Publish-Accepted' + ' | ' + str(up_request.rid) + ' | ' + "Published Files ->"+str(up_request.list_of_available_files)+ ']'
            else:
                # if the client is already published
                msg_to_client = '[Publish-Denied' + ' | ' + str(up_request.rid) + ' | ' + 'Files already published]'
        else:
            msg_to_client = '[Publish-Denied' + ' | ' + str(up_request.rid) + '| ' + str(
                up_request.name) + ' name doesn`t exist]'

        self.printwt(msg_to_client)
        array_to_append = [up_request.name, up_request.rid, msg_to_client, client_address]
        self.list_of_acknowledgements.append(array_to_append)
        self.sock.sendto(msg_to_client.encode('utf-8'), client_address)

    def try_removeFile(self, rf_request):
        print(rf_request.getHeader())
        client_address = (rf_request.host, rf_request.udp_socket)

        if self.check_if_client(rf_request):
            # if the file is at the list remove it
            found = False
            for obj in self.list_of_client_files:
                if obj.name == rf_request.name:
                    found = True
                    # delete the file from the database/list
                    failed_file = []
                    for file in rf_request.list_of_files_to_remove:
                        try:
                            obj.list_of_available_files.remove(file)
                        except:
                            failed_file.append(file)

                    if len(failed_file) == 1:
                        msg_to_client = "[REMOVED-DENIED |" + str(rf_request.rid) + " | File Doesn't exist with " + str(
                            failed_file[0]) + "]"
                    elif len(failed_file) > 1:
                        msg_to_client = "[REMOVED-DENIED |" + str(
                            rf_request.rid) + "| File Doesn't exist with following names " + str(failed_file) + "]"
                    else:
                        msg_to_client = '[REMOVED' + ' | ' + str(rf_request.rid) + ']'
                    # Break the loop since we found the Obj
                    break

            if not found:
                msg_to_client = "[REMOVED-DENIED |" + str(rf_request.rid) + "| You didn't publish any files ]"
        else:
            msg_to_client = '[REMOVED-DENIED' + ' | ' + str(rf_request.rid) + '| ' + str(
                rf_request.name) + ' name doesn`t exist]'
        self.printwt(msg_to_client)
        array_to_append = [rf_request.name, rf_request.rid, msg_to_client]
        self.list_of_acknowledgements.append(array_to_append)
        self.sock.sendto(msg_to_client.encode('utf-8'), client_address)

    def check_if_client(self, client_request):
        for obj in self.list_of_registered_clients:
            if isinstance(obj,Register):  # for checking if client they are all register objects but isinstance
                # is important to allow us to call obj.name
                if obj.name == client_request.name:
                    return True
        return False

    def check_if_already_ack(self, client_request):
        for s_list in self.list_of_acknowledgements:
            if s_list[0] == client_request.name and s_list[1] == client_request.rid:
                print(client_request.getHeader())
                self.printwt(f'Already received this request. Resending the reply : {client_request.name}')
                self.sock.sendto(s_list[2].encode('utf-8'), s_list[3])
                return True
        return False

    def get_client_udp_address(self, client_request):
        for obj in self.list_of_registered_clients:
            if isinstance(obj, Register):  # for checking if client they are all register objects but isinstance
                # is important to allow us to call obj.name
                if obj.name == client_request.name:
                    return obj.host, obj.udp_socket

    # 3. wait_for_client() - Override the server's wait_for_client() method to handle multiple clients by using an
    # infinite loop
    def wait_for_client(self):

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
    udp_server_multi_client = serverMultiClient(SERVER_ADDRESS[0], SERVER_ADDRESS[1])

    udp_server_multi_client.configure_server()
    udp_server_multi_client.wait_for_client()


if __name__ == '__main__':
    main()
