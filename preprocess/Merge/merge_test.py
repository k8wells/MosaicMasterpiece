import operator
import utils
import re
from collections import defaultdict
import pymongo
import ujson
import json
import fileinput
from stemming import porter2


mongo = pymongo.Connection('localhost', 27017)
for item in mongo['my_database']['merged_info'].find():
    print item

