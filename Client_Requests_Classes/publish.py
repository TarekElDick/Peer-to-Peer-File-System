from Client_Requests_Classes import request


class publish_req(request.clientRequest):
    def __init__(self,  name,file_name  ) -> object:
        super().__init__('publish_req')
        self.name = name
        self.file_name = file_name

    def getHeader(self):
        header_string = '\n['+self.request_type + ' | ' + str(self.rid) + ' | ' + self.name + ' | ' + str(self.file_name) + ']\n'
        return header_string


