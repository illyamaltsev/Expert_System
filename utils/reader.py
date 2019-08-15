
def read_all(filename: str):
    f = open(filename, 'r')
    file_content = f.read()
    f.close()
    return file_content
