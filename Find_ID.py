#!/usr/bin/env python
from __future__ import division
import heapq
import operator
import re
import math
import collections
import random
import time
#import utils
import json
import itertools
from collections import defaultdict
import pymongo
from stemming import porter2
#import tfidf
#import numpy as np
#from numpy import unravel_index


def return_id():
    #REPLACE WITH REAL FUNCTION
    return '8143186204'

class FindID(object):
    def __init__(self):
        pass

    #REPLACE WITH REAL FUNCTION
    def mary_function(self, s1, s2):
        value1 = math.fabs(s1[0] - s2[0])
        value2 = math.fabs(s1[1] - s2[1])
        value3 = math.fabs(s1[2] - s2[2])
        output = (value1 + value2 + value3)/3
        return output

    def find_clusters(self, id, clusters_inv):
        k = 0
        ids = []
        clust_inv = {}
        for item in clusters_inv:
            clust_inv.update(item)
        print clust_inv
        while k < len(clust_inv)-1:
            ids.append(clust_inv['tier'+str(k)][str(id)])
            k = k +1
        print ids
        return ids

    def findID(self, cluster_ids, clusters, pics, color1):
        k = 0
        bool = 'TRUE'
        
        pic_data = {}
        for item in pics:
            pic_data.update(item)
        clust = {}
        for item in clusters:
            clust.update(item)
        print clust
        matching_id = '0'
        for cluster_id in cluster_ids:
            print 'tier'+str(k)
            pic_ids = clust['tier'+str(k)][str(cluster_id)]
            for id in pic_ids:
                color2 = pic_data[id]['color']
                sim = self.mary_function(color1, color2)
                print sim
                if sim<30:
                    bool = 'FALSE'
                    matching_id = id
                    break
            if bool == 'FALSE':
                break
            k = k +1
        return matching_id


def main():
    mongo = pymongo.Connection('localhost', 27017)
    pics = mongo['my_database']['pics'].find()
    clusters = mongo['my_database']['clusters'].find()
    clusters_inv = mongo['my_database']['clusters_inv'].find()
    find_id = FindID()
    id = return_id()
    cluster_ids = find_id.find_clusters(id, clusters_inv)
    color = [102, 9, 39]
    new_id = find_id.findID(cluster_ids, clusters, pics, color)
    print new_id
    


if __name__=="__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print 'done with cluster after %.3f seconds'%(end_time-start_time)
        
