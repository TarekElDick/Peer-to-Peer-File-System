from Client_Requests_Classes import request


class publish_req(request.clientRequest):
    def __init__(self,  name,list_of_files=[]  ) -> object:
        super().__init__('publish_req')
        self.name = name
        self.list_of_files = list_of_files

    def getHeader(self):
        header_string = '\n['+self.request_type + ' | ' + str(self.rid) + ' | ' + self.name + ' | ' + str(self.list_of_files) + ']\n'
        return header_string


