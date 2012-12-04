#!/usr/bin/env python
from __future__ import division
import heapq
import operator
import re
import math
import collections
import random
import time
import json
import itertools
from collections import defaultdict
import pymongo
from stemming import porter2



def get_id(tag, dblist):
    data = []
    for item in dblist:
        data.append(item)
    id = 'NULL'
    for entry in data:
        #print entry
        if tag in entry['keywords']['keywords']:
            id = entry['filename']
            #return entry['filename']
        #else:
            #print 'NNNNNNNNOOOOOOOOOOOOO'
            #return 0
    if id == 'NULL':
        k = random.randint(0, len(data)-1)
        id = data[k]['filename']
    return id

        
def get_sim(query, stored):
    diff = [pow((a-b),2) for a,b in zip(query,stored)]
    return math.sqrt(sum(diff))

class FindID(object):

    def find_clusters(self, id, clusters_inv):
        k = 0
        ids = []
        clust_inv = {}
        for item in clusters_inv:
            clust_inv.update(item)
        while k < len(clust_inv)-1:
            ids.append(clust_inv['tier'+str(k)][str(id)])
            k = k +1
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
        matching_id = '0'
        for cluster_id in cluster_ids:
            pic_ids = clust['tier'+str(k)][str(cluster_id)]
            for id in pic_ids:
                color2 = pic_data[id]['color']
                sim = get_sim(color1, color2)
                print sim
                if sim<103:
                    bool = 'FALSE'
                    matching_id = id
                    break
            if bool == 'FALSE':
                break
            k = k +1
        return matching_id


def main():
    mongo = pymongo.Connection('localhost', 27017)
    merge = mongo['my_database']['merged_info'].find()
    pics = mongo['my_database']['pics'].find()
    clusters = mongo['my_database']['clusters'].find()
    clusters_inv = mongo['my_database']['clusters_inv'].find()
    find_id = FindID()
    ####INPUT RAW INPUT HERE FOR COLOR AND STRING????#####
    color = [102, 9, 39]
    tag = 'dog'
    id = get_id(tag, merge)
    cluster_ids = find_id.find_clusters(id, clusters_inv)
    new_id = find_id.findID(cluster_ids, clusters, pics, color)
    print new_id
    


if __name__=="__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print 'done with cluster after %.3f seconds'%(end_time-start_time)
        
