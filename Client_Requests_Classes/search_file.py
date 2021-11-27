from Client_Requests_Classes import request


class SearchFile(request.clientRequest):
    def __init__(self, name, host, udp_socket,filename) -> object:
        super().__init__('search-file')
        self.name = name
        self.host = host
        self.udp_socket = udp_socket
        self.filename = filename



    def getHeader(self):
        header_string = '\n[' + self.request_type + ' | ' + str(self.rid) + ' | ' + self.filename + ']\n'
        return header_string
