from Client_Requests_Classes import request


class SearchFile(request.clientRequest):
    def __init__(self, filename) -> object:
        super().__init__('search-file')
        self.filename = filename



    def getHeader(self):
        header_string = '\n[' + self.request_type + ' | ' + str(self.rid) + ' | ' + self.filename + ']\n'
        return header_string
