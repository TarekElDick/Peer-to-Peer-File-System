class Publishing:

    def __init__(self, name):
        super().__init__('Publishing')
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
                print("file will be fragmented")
                # call split
                #split(a_file, 200)
                # call send