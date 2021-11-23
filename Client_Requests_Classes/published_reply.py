from Client_Requests_Classes import request


class published_reply(request.clientRequest):
    def __init__(self, name) -> object:
        super().__init__('published_reply')
        self.name = name

    def getHeader(self):
        header_string = '\n[ ' + self.request_type + ' | ' + str(self.rid) + ']\n'
        return header_string
