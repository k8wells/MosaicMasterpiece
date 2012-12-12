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

    def find_clusters(self, id, clusters):
        k = 0
        clust = {}
        for item in clusters:
            clust.update(item)
        #print clust
        clusterid = clust[str(id)]
        return clusterid

    def findID(self, cluster_id, clusters_inv, pics, color1):
        matching_id = '0'
        clust_inv = {}
        pic_data = {}
        for item in pics:
            pic_data.update(item)
        for item in clusters_inv:
            clust_inv.update(item)
        pic_ids = clust_inv[str(cluster_id)]
        sim_value = 103
        for id in pic_ids:
            color2 = pic_data[id]['color']
            sim = get_sim(color1, color2)
            print sim
            if sim<sim_value:
                matching_id = id
                sim_value = sim
                
        return matching_id

    def findID2(self, pics, color):
        pic_data = {}
        matching_id = '0'
        for item in pics:
            pic_data.update(item)
        sim_value = 100
        for pic in pic_data:
            if pic == '_id':
                break
            #print pic
            color2 = pic_data[pic]['color']
            sim = get_sim(color, color2)
            print sim
            if sim<sim_value:
                matching_id = pic
                sim_value = sim
        return matching_id


def main():
    mongo = pymongo.Connection('localhost', 27017)
    merge = mongo['my_database']['merged_info'].find()
    pics = mongo['my_database']['pics'].find()
    find_id = FindID()
    ####INPUT RAW INPUT HERE FOR COLOR AND STRING????#####
    color = [102, 9, 39]
    tag = 'cat'
    #id = get_id(tag, merge)
    #cluster_id = find_id.find_clusters(id, clusters)
    #new_id = find_id.findID(cluster_id, clusters_inv, pics, color)
    new_id = find_id.findID2(pics, color)
    print new_id
    


if __name__=="__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print 'done with cluster after %.3f seconds'%(end_time-start_time)
        
