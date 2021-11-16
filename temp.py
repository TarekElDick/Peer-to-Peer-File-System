

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
