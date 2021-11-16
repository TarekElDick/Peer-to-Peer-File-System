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
            exit
        elif int(number_of_characters) > 1:
            if int(number_of_characters) <= 200:
                print("file will be sent in 1 segment")
                # sendfile
            else:
                print("file will be fragmented")
                # call split
                #split(a_file, 200)
                # call send





    def split(infilepath, param):
        data, ext = infilepath.rsplit('.', 1)
        i = 0
        written = False
        with open(infilepath) as infile:
            while True:
                outfilepath = "{}{}.{}".format(data, i, ext)
                with open(outfilepath, 'w') as outfile:
                    for line in (infile.readline() for _ in range(param)):
                        outfile.write(line)
                    written = bool(line)
                if not written:
                    break
                i += 1


# upload text file
# with open("file_to_upload.txt", "rt") as a_file:  # open(file_name, mode) , rt--> read text   as  target
# file_dict = {"file_to_upload.txt": a_file}
# response = requests.post("http://httpbin.org/post", files=file_dict)  # upload the file to the url
