#!/usr/bin/python
import ujson
import json
import fileinput
import re
from stemming import porter2

def tokenize(text):
    tokens = re.findall("[\w']+", text.lower())
    return [porter2.stem(token) for token in tokens]

def parseID(filename):
    tokens = filename.split("_")
    print tokens[0]
    return tokens[0]


def read_data():
    for line in fileinput.input():
        yield ujson.loads(line)

def colordict(data):
    dictionary = {}
    for thing in data:
        if 'color' not in thing:
            continue
        dictionary[thing['id']] = thing['color']
    print dictionary

def datadict(data):
    dictionary = {}
    for thing in data:
        if 'filename' not in thing:
            continue
        id = parseID(thing['filename'])
        dictionary[id] = {}
        dictionary[id]['keywords'] = tokenize(thing['tags'])
        dictionary[id]['title'] = tokenize(thing['title'])
    print dictionary
        

def main():
    color = {}
    img = {}
    colordata = read_data()
    colordict(colordata)
   # for data in colordata:
   #     print data
    imgdata = read_data()
    datadict(imgdata)
    #for data in imgdata:
    #    print data

if __name__=="__main__":
    main()
