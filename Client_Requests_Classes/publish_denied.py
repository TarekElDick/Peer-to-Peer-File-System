from Client_Requests_Classes import request


class publish_denied(request.clientRequest):
    def __init__(self, name, list_of_files=[]) -> object:
        super().__init__('publish_denied')
        self.name = name
        self.list_of_files = list_of_files

    def getHeader(self):
        header_string = '\n[ ' + self.request_type + ' | ' + str(self.rid) +' | ' + " Name doesn't exist " + ']\n'
        return header_string
