#!/usr/bin/env python
from __future__ import division
import heapq
import operator
import re
import math
import collections
import random
import time
import utils
import json
import itertools
from collections import defaultdict
import pymongo
from numpy import array
import gc
#from sklearn.feature_extraction.text import TfidfTransformer

from stemming import porter2
import tfidf
import numpy as np
from numpy import unravel_index
from scipy.cluster.vq import kmeans2, kmeans, vq


mongo = pymongo.Connection('localhost', 27017)
pics = mongo['my_database']['merged_info'].find()
mongo_pics = mongo['my_database']['pics']
mongo_pics.remove({})
pics = mongo['my_database']['merged_info'].find()
pics2 = {}
for pic in pics:
    id = pic["filename"]
    if pic['keywords']['keywords'] == []:
        tokens = pic['keywords']['title']
    else:
        tokens = pic['keywords']['keywords']
    color = pic['color']
    pics2[id] = {}
    pics2[id]['tokens'] = tokens
    pics2[id]['color'] = color
    mongo_pics.insert({id: pics2[id]})


