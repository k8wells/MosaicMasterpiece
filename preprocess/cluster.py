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

from stemming import porter2
import tfidf
import numpy as np
from numpy import unravel_index

def divide(id):
    return [id[i:i+10] for i in range(len(id)) if not i % 10]

class Cluster(object):
    
    def __init__(self):
        self.pics = {}
        self.clusters = {} # cluster id : [pic ids]
        self.matrix_ids = {} # cluster id : pic id
        #self.matrix_ids_inv = {} #pic id: cluster id
        self.clusters_inv = {} # pic id : cluster id
        self.new_pics = {}


    def index(self, pics):
        self.clusters["tier0"]={}
        self.clusters_inv['tier0']={}
        i = 0
        for pic in pics:
            id = pic["filename"]
            if pic['keywords']['keywords'] == []:
                tokens = pic['keywords']['title']
            else:
                tokens = pic['keywords']['keywords']
            color = pic['color']
            self.pics[id] = {}
            self.pics[id]['tokens'] = tokens
            self.pics[id]['color'] = color
            self.clusters["tier0"][str(i)]=[id]
            self.clusters_inv['tier0'][str(id)]=i
            i = i+1

    def set_up_table(self, k):
        table = tfidf.tfidf()
        size = len(self.clusters['tier'+str(k)])
        i = 0
        keys = self.clusters['tier'+str(k)].keys()
        self.new_pics = {}
        while i < size:
            pics =  self.clusters['tier'+str(k)][keys[i]]
            id = ''
            tokens = []
            j = 0
            while j < len(pics):
                id = id  + pics[j]
                tokens = tokens + self.pics[pics[j]]['tokens']
                j = j + 1
            self.new_pics[id] = tokens
            i = i +1
        for id in self.new_pics.keys(): 
            table.addDocument(id,self.new_pics[id])
        return table

    def find_matrix(self, matrix, k, table):
        sims = []
        id = 0
        self.matrix_ids={}
        #self.matrix_ids_inv = {}
        for pic in self.new_pics:
            sims = sims + table.similarities(self.new_pics[pic])
            self.matrix_ids[id] = pic
            #self.matrix_ids_inv[pic]= [id]
            id = id + 1
        values = []
        for sim in sims:
            values.append(sim[1])
        matrix = np.array(values)
        size = math.sqrt(len(sims))
        matrix.resize(size, size)
        #ignores the similarites to itself
        x = 0
        while x < size:
            y = matrix[x].argmax()
            matrix[x,y] = 0
            x = x + 1
        return matrix
                                
    def find_closest_pairs(self, matrix):
        closest_pair = unravel_index(matrix.argmax(), matrix.shape)
        return closest_pair
       
            
    def combine_pairs(self, matrix, pairs, k):
        self.clusters_inv['tier'+str(k)] = {}
        self.clusters['tier'+str(k)] = {}
       
        x = pairs[0]
        y = pairs[1]
        id1 = self.matrix_ids[x]
        id2 = self.matrix_ids[y]
        i = 0
        while i < len(matrix[0]):
            if i != x and i != y:
                id = str(self.matrix_ids[i]) # find pic id that corresponds with certain row
                divide_id = divide(id)
                value = str(self.clusters_inv['tier'+str(k-1)][divide_id[0]]) # find cluster that the pic was previously assigned to
                for id in divide_id:
                    self.clusters_inv['tier'+str(k)][id] = value # set pic id : same cluster id (row was not changed)
                
                self.clusters['tier'+str(k)][value] = self.clusters['tier'+str(k-1)][value]
            else:
                #new_id = str(id1 + id2)
                divide_id1 = divide(id1)
                divide_id2 = divide(id2)
                value = str(self.clusters_inv['tier'+str(k-1)][divide_id1[0]]) # find cluster value that the pic was previously assigned to
                ids = divide_id1 + divide_id2
                for id in ids:
                    self.clusters_inv['tier'+str(k)][id] = str(value) # use cluster id of first pic
                
                value2 = str(self.clusters_inv['tier'+str(k-1)][divide_id2[0]]) # find cluster that the pic was previously assigned to
                clusters1 = self.clusters['tier'+str(k-1)][value] # find all pic ids in previous cluster
                clusters2 = self.clusters['tier'+str(k-1)][value2] # find all pic ids in previous cluster
                combine_clusters = clusters1 + clusters2
                self.clusters['tier'+str(k)][value] = combine_clusters
            i = i + 1
        #print 'CLUSTERS'
        #print self.clusters
        #print 'INV_CLUSTER'
        #print self.clusters_inv

    def find_beginning_size(self):
        size =  len(self.pics)
        return size

    def return_clusters(self):
        return self.clusters
    def return_clusters_inv(self):
        return self.clusters_inv
    def return_pics(self):
        return self.pics

def main():
    #pics = utils.read_tweets()
    mongo = pymongo.Connection('localhost', 27017)
    pics = mongo['my_database']['merged_info'].find()
    #for item in pics:
        #print item
    cluster = Cluster()
    cluster.index(pics)
    size = cluster.find_beginning_size()
    i = 1
    table = cluster.set_up_table(i-1)
    #pics = utils.read_tweets()
    matrix = cluster.find_matrix(pics, i, table)
    pairs = cluster.find_closest_pairs(matrix)
    new_matrix = cluster.combine_pairs(matrix, pairs, i)
    i = i +1
    while i < size:
        table = cluster.set_up_table(i-1)
        matrix = cluster.find_matrix(new_matrix, i, table)
        pairs = cluster.find_closest_pairs(matrix)
        new_matrix = cluster.combine_pairs(matrix, pairs, i)
        i = i +1
    mongo_clusters = mongo['my_database']['clusters']
    #print cluster.return_clusters()
    mongo_clusters.remove({})
    mongo_clusters.insert(cluster.return_clusters())
    mongo_clusters_inv = mongo['my_database']['clusters_inv']
    mongo_clusters_inv.remove({})
    mongo_clusters_inv.insert(cluster.return_clusters_inv())
    mongo_pics = mongo['my_database']['pics']
    mongo_pics.remove({})
    mongo_pics.insert(cluster.return_pics())
    print cluster.return_pics()
    for item in mongo_clusters.find():
        print item
    for item in mongo_clusters_inv.find():
        print item
    


if __name__=="__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print 'done with cluster after %.3f seconds'%(end_time-start_time)
