from Client_Requests_Classes import request


class publish_denied(request.clientRequest):
    def __init__(self, name) -> object:
        super().__init__('publish_denied')
        self.name = name

    def getHeader(self):
        header_string = '\n[ ' + self.request_type + ' | ' + str(self.rid) +' | ' + " Name doesn't exist " + ']\n'
        return header_string
