from sphinx.util import requests


class Publishing:

    def __init__(self, name, host, udp_socket, tcp_socket) -> object:
        super().__init__('Publishing')
        self.name = name
        self.host = host
        self.udp_socket = udp_socket
        self.tcp_socket = tcp_socket


# open text file and count the number of characters
with open("file_to_upload.txt", "rt") as a_file:
    data = a_file.read()
    number_of_characters = len(data)
    print('Number of characters in text file :', number_of_characters)



# upload text file

with open("file_to_upload.txt", "rt") as a_file:  # open(file_name, mode) , rt--> read text   as  target
    file_dict = {"file_to_upload.txt": a_file}
    response = requests.post("http://httpbin.org/post", files=file_dict)  # upload the file to the url
