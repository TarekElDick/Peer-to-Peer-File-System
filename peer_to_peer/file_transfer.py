class file_transfer:

    def __init__(self, name):
        super().__init__('file_transfer')
        self.name = name

    # open text file and count the number of characters
    with open("file_to_upload.txt", "rt") as a_file:
        data = a_file.read()
        number_of_characters = len(data)
        print('Number of characters in text file :', number_of_characters)

        if int(number_of_characters) < 1:
            print("file is empty")
            exit()
        elif int(number_of_characters) > 1:
            if int(number_of_characters) <= 200:
                print("file will be sent in 1 segment")
                # sendfile
            else:
                # chuck the file into segments each 200 char
                print("file will be fragmented")
                data = []
                with open("file_to_upload.txt") as f:
                    while True:
                        d = f.read(200)
                        if not d:
                            break
                        else:
                            data.append(d)
                a = data[0]
                print(a)
                # call send
