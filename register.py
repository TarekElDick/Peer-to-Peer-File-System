import request


class Register(request.clientRequest):
    def __init__(self,  name, host, udp_socket, tcp_socket) -> object:
        super().__init__('register')
        self.name = name
        self.host = host
        self.udp_socket = udp_socket
        self.tcp_socket = tcp_socket

    def printRequest(self):
        from pprint import pprint
        pprint(vars(self))

    def getHeader(self):
        header_string = ' ' + self.request_type + ' ' + str(self.rid) + ' ' + self.name + ' ' + str(self.host) + ' ' + str(self.udp_socket) + ' ' + str(self.tcp_socket) + '\r\n'
        header_length = len(header_string)
        header_final = str(header_length) + header_string
        return header_final
