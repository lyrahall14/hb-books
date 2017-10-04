"""Pretty-prints JSON file given on command-line."""

from sys import argv
from pprint import pprint
import json

# Read JSON string from filename given on command-line
json_string = open(argv[1]).read()

# Turn into Python dictionary
json_dict = json.loads(json_string)

titles_list = json_dict['titles']
authors_list = json_dict['authors']
ratings_list = json_dict['ratings']
pic_url_list = json_dict['pics']

books_list = zip(titles_list, authors_list, ratings_list, pic_url_list)

# "Pretty print" it
print books_list