from Client_Requests_Classes import request


class remove_denied(request.clientRequest):
    def __init__(self, name) -> object:
        super().__init__('remove_denied')
        self.name = name

    def getHeader(self):
        header_string = '\n[ ' + self.request_type + ' | ' + str(self.rid) +' | ' + " Name doesn't exist " + ']\n'
        return header_string
