from Client_Requests_Classes import request


class Retrieve(request.clientRequest):
    def __init__(self, name) -> object:
        super().__init__('retrieve-all')
        self.name = name

    def getHeader(self):
        header_string = '\n[' + self.request_type + ' | ' + str(self.rid) + ']\n'
        return header_string
