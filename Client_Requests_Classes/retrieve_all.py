from Client_Requests_Classes import request


class RetrieveAll(request.clientRequest):
    def __init__(self) -> object:
        super().__init__('retrieve-all')



    def getHeader(self):
        header_string = '\n['+self.request_type + ' | ' + str(self.rid) +  ']\n'
        return header_string
