import json
import argparse
import pandas as pd

class JSONParser():
    def __init__(self, filename, type=None, fields=None):
    # """
    # type: 'file': file contaning json objects in each line, 'jsonfile' : single json object
    # """
        self.filename = filename
        self.get_file_dict()

    
    def get_file_dict(self):
        with open(self.filename) as f:
            for line in f:
                file_dict = dict(line)
                print (file_dict)
                yield file_dict


    def extract_drug(self, file_dict):
        pass

    

def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_file', dest='input_file', help='json_file')
    parser.add_argument('-o','--output_file', dest='output_file', help='tsv_file')
    return parser

def main():
    print ('########## Reading JSON file ########')
    parser = add_arguments()
    args = parser.parse_args()
    input_file = args.input_file
    print (input_file)
    json_parser = JSONParser(input_file)


if __name__ == "__main__":
    print('#######')
    main()
