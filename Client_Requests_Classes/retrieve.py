from Client_Requests_Classes import request


class Retrieve(request.clientRequest):
    def __init__(self,name , host, udp_socket) -> object:
        super().__init__('retrieve')
        self.host = host
        self.host = host
        self.udp_socket = udp_socket



    def getHeader(self):
        header_string = '\n['+self.request_type + ' | ' + str(self.rid) +  ']\n'
        return header_string
