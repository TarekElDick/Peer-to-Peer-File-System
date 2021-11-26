from Client_Requests_Classes import request


class Download(request.clientRequest):
    def __init__(self,  file_name) -> object:
        super().__init__('download')
        self.file_name = file_name

    def getHeader(self):
        header_string = '\n['+self.request_type + ' | ' + str(self.rid) + ' | ' + self.file_name + ']\n'
        return header_string


