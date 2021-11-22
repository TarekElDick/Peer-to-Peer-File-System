from Client_Requests_Classes import request


class remove_req(request.clientRequest):
    def __init__(self,  name,list_of_files_to_remove=[]  ) -> object:
        super().__init__('remove_req')
        self.name = name
        self.list_of_files_to_remove = list_of_files_to_remove

    def getHeader(self):
        header_string = '\n['+self.request_type + ' | ' + str(self.rid) + ' | ' + self.name + ' | ' + str(self.list_of_files_to_remove) + ']\n'
        return header_string


