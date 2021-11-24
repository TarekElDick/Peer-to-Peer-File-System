from Client_Requests_Classes import request


class RetrieveInfot(request.clientRequest):
    def __init__(self, name) -> object:
        super().__init__('retrieve-infot')
        self.name = name



    def getHeader(self):
        header_string = '\n[' + self.request_type + ' | ' + str(self.rid) + ' | ' + self.name + ']\n'
        return header_string
