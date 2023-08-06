import random
import json


'''

This package is used to generate random names for testing purpose
Package is for educational purpose only.

'''

class IndiaDataSet:
    
    def __init__(self) -> None:
        self.file = open('name.json', 'r')
        self.content = json.load(self.file)
        self.name_list = [each["name"] for each in self.content]

    # To generate random name .... 
    def get_name(self):
        return random.choice(self.name_list)