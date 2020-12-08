import os

def read_file(filename):
    file_path = "{}/{}".format(os.path.abspath("."),filename)
    with open(file_path) as f:
        content = f.read()
        return content

read_file("Wiki_content.html")