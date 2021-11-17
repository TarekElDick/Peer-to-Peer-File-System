test_data = ""
counter = 0

def main():
    # global counter, test_data
    # with open("file_to_upload.txt") as f:
    #     test_data = f.read()
    #
    # while True:
    #     try:
    #         print(test_data[counter: counter + 200])
    #         counter += 1
    #     except:
    #         break
    #         print("Done!")
    data = []
    with open("file_to_upload.txt") as f:
        while True:
            d = f.read(200)
            if not d:
                break
            else:
                data.append(d)
    a= data[0]
    print(a)

main()