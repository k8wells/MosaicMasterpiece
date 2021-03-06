from __future__ import division
import operator
import utils
import re
from collections import defaultdict
import pymongo
from pymongo import connection
import ujson
import json
import fileinput
from stemming import porter2

def tokenize(text):
    tokens = re.findall("[\w']+", text.lower())
    return [porter2.stem(token) for token in tokens]

def parseID(filename):
    tokens = filename.split("_")
    return tokens[0]


def read_data():
    for line in fileinput.input():
        yield json.loads(line)

def colordict(data):
    dictionary = {}
    for thing in data:
        if 'color' not in thing:
            continue
        dictionary[thing['id']] = thing['color']
    return dictionary

def datadict(data):
    dictionary = {}
    for thing in data:
        if 'filename' not in thing:
            continue
        id = parseID(thing['filename'])
        dictionary[id] = {}
        dictionary[id]['keywords'] = tokenize(thing['tags'])
        dictionary[id]['title'] = tokenize(thing['title'])
    return dictionary
        

def main():
    color = {}
    img = {}
    colordata = read_data()
    color_dict = {}
    color_dict = colordict(colordata)
    imgdata = read_data()
    img_dict = {}
    img_dict = datadict(imgdata)
   
    delete_ids = []
    for id in color_dict:
        if id not in img_dict.keys():
            delete_ids.append(id)
    for id in delete_ids:
        del color_dict[id]
    delete_ids = []
    for id in img_dict:
        if id not in color_dict.keys():
            delete_ids.append(id)
    for id in delete_ids:
        del img_dict[id]
    #the following code is a list of dict (like the json file)
    #{'color':[#,#,#], 'keywords': {keywords:[], title:[]}, _id:objid, id:#},
    data = []
    for id in img_dict:
        dict = {'filename': id, 'color':color_dict[id], 'keywords':img_dict[id]}
        data.append(dict)
    
    # the following code is a list of dics by id like
    # {id : {'color':[#,#,#], 'keywords': {keywords:[], title:[]}},
    """
    data = {}
    for id in img_dict:
        data[id] = {}
        data[id]['color'] = color_dict[id]
        data[id]['keywords'] = img_dict[id]
    """

    mongo = pymongo.Connection('localhost', 27017)
    mongo_db = mongo['my_database']
    mongo_collection = mongo_db['merged_info']
    mongo_collection.remove({})
    mongo_collection.insert(data)
    #for item in mongo_collection.find():
        #print item
        
    
if __name__=="__main__":
    main()

