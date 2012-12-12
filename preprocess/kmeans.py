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
#from sklearn.feature_extraction.text import TfidfTransformer

from stemming import porter2
import tfidf
import numpy as np
from numpy import unravel_index
from scipy.cluster.vq import kmeans2, kmeans, vq


class Clustering(object):
    
    def __init__(self):
        self.ids = []
        self.dict = {}
        self.pics = {}
        
    def index(self, pics):
        array1 = []
        for pic in pics:
            #print pic
            #print pic
            id = pic["filename"]
            self.ids.append(id)
            if pic['keywords']['keywords'] == []:
                tokens = pic['keywords']['title']
            else:
                tokens = pic['keywords']['keywords']
            color = pic['color']
            self.pics[id] = {}
            self.pics[id]['tokens'] = tokens
            self.pics[id]['color'] = color
            self.dict[id]=tokens
            array1.append(tokens)
        return array1

    def find_matrix(self, table):
        sims = []
        for pic in self.dict.keys():
            sims = sims + table.similarities(self.dict[pic])
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

    def find_matrix2(self, table, ids):
        sims = []
        for id in ids:
            sims = sims + table.similarities(self.dict[id])
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
    
    def set_up_table(self, tokens):
        table = tfidf.tfidf()
        i = 0
        for token in tokens:
            table.addDocument(self.ids[i],token)
            i = i+1
        return table

    def set_up_table2(self, ids):
        table = tfidf.tfidf()
       # print ids
        for id in ids:
            token = self.dict[id]
            table.addDocument(id,token)
        return table

    def assign_clusters(self, clusters):
        clusters_dict = {}
        cluster_dict_inv = {}
        cluster_dict_inv['0'] = []
        cluster_dict_inv['1'] = []
        cluster_dict_inv['2'] = []
        cluster_dict_inv['3'] = []
        cluster_dict_inv['4'] = []
        cluster_dict_inv['5'] = []
        cluster_dict_inv['6'] = []
        cluster_dict_inv['7'] = []
        cluster_dict_inv['8'] = []
        cluster_dict_inv['9'] = []
        i = 0
        for cluster in clusters:
            id = self.ids[i]
            clusters_dict[id] = str(cluster)
            cluster_dict_inv[str(cluster)].append(id)
            i = i+1
        return clusters_dict, cluster_dict_inv

    def assign_clusters2(self, clusters, starting_value, ids):
        starting_value = int(starting_value)
        clusters_dict = {}
        cluster_dict_inv = {}
        cluster_dict_inv[str(starting_value)] = []
        cluster_dict_inv[str(starting_value+ 1)] = []
        cluster_dict_inv[str(starting_value+2)] = []
        cluster_dict_inv[str(starting_value+3)] = []
        cluster_dict_inv[str(starting_value+4)] = []
        cluster_dict_inv[str(starting_value+5)] = []
        cluster_dict_inv[str(starting_value+6)] = []
        cluster_dict_inv[str(starting_value+7)] = []
        cluster_dict_inv[str(starting_value+8)] = []
        cluster_dict_inv[str(starting_value+9)] = []
        i = starting_value
        k = 0
        for cluster in clusters:
            id = ids[k]
            clusters_dict[id] = str(cluster + starting_value)
            cluster_dict_inv[str(cluster+starting_value)].append(id)
            #i = i+1
            k = k+1
        return clusters_dict, cluster_dict_inv

    #def assign_clusters_inv(self, clusters):
        
    #for cluster in clusters:
    def return_pics(self):
        return self.pics
            
            

def main():
    mongo = pymongo.Connection('localhost', 27017)
    pics = mongo['my_database']['merged_info'].find()
    cluster = Clustering()
    array1 = cluster.index(pics)
    mongo_clusters = mongo['my_database']['clusters']
    mongo_clusters.remove({})
    mongo_clusters_inv = mongo['my_database']['clusters_inv']
    mongo_clusters_inv.remove({})
    mongo_pics = mongo['my_database']['pics']
    mongo_pics.remove({})
    mongo_pics.insert(cluster.return_pics())
    table = cluster.set_up_table(array1)
    matrix = cluster.find_matrix(table)
    centroids,_ = kmeans(matrix,10)
    clusters,_ = vq(matrix, centroids)
    #print clusters
    #print 'hi'
    #print centroids
    starting_value = '0'
    clusters_dict1, cluster_inv1 = cluster.assign_clusters(clusters)
    CLUSTERS = {}
    CLUSTERS_INV = {}
    CLUSTERS['tier9'] = clusters_dict1
    CLUSTERS_INV['tier9'] = cluster_inv1
    #print clusters_dict
   # print cluster_inv

    ##SECOND ROUND
    
    k = 8
    j = 1
    while k > -1:
        #print k
        i = 0
        print cluster_inv1
        #print math.pow(10,j)-j*10
        while i < int(max(cluster_inv1.keys()))+1:
            #print i
            
            ids = cluster_inv1[str(i)]
            #print len(ids)
            if len(ids) > 1:
                table = cluster.set_up_table2(ids)
                matrix = cluster.find_matrix2(table, ids)
                #print matrix
                centroids,_ = kmeans(matrix,10)
                #print centroids
                clusters,_ = vq(matrix, centroids)
                #print clusters
                
                if 'tier'+str(k) in CLUSTERS.keys():
                    #print 'starting value'
                    #print max(CLUSTERS_INV['tier'+str(k+1)].keys()) + 1
                    starting_value = str(int(max(CLUSTERS_INV['tier'+str(k)].keys())) + 1)
                    clusters_dict, cluster_inv = cluster.assign_clusters2(clusters,starting_value, ids)
                    CLUSTERS['tier' + str(k) ].update(clusters_dict)
                    CLUSTERS_INV['tier' + str(k) ].update(cluster_inv)
                    #print cluster_inv
                    
                else:
                    #print 'ONCE'
                    #print clusters
                    starting_value = '0'
                    clusters_dict, cluster_inv = cluster.assign_clusters2(clusters,starting_value, ids)
                    CLUSTERS['tier' + str(k) ] = clusters_dict
                    CLUSTERS_INV['tier' + str(k) ] = cluster_inv
            elif len(ids) == 1:
                if 'tier'+str(k) in CLUSTERS.keys():
                    starting_value = str(int(max(CLUSTERS_INV['tier'+str(k)].keys())) + 1)
                    clusters_dict = {ids[0]:starting_value}
                    cluster_inv = {starting_value:[ids[0]]}
                    CLUSTERS['tier' + str(k) ].update(clusters_dict)
                    CLUSTERS_INV['tier' + str(k) ].update(cluster_inv)
                else:
                    starting_value = '0'
                    clusters_dict = {ids[0]:starting_value}
                    cluster_inv = {starting_value:[ids[0]]}
                    CLUSTERS['tier' + str(k) ] = clusters_dict
                    CLUSTERS_INV['tier' + str(k) ] = cluster_inv
            else:
                if 'tier'+str(k) in CLUSTERS.keys():
                    starting_value = str(int(max(CLUSTERS_INV['tier'+str(k)].keys())) + 1)
                    #clusters_dict = {ids[0]:starting_value}
                    cluster_inv = {starting_value:[]}
                    #CLUSTERS['tier' + str(k) ].update(clusters_dict)
                    CLUSTERS_INV['tier' + str(k) ].update(cluster_inv)
                else:
                    starting_value = 0
                    #clusters_dict = {ids[0]:starting_value}
                    cluster_inv = {str(starting_value):[]}
                    #CLUSTERS['tier' + str(k) ] = clusters_dict
                    CLUSTERS_INV['tier' + str(k) ] = cluster_inv
                

            i = i+1
        mongo_clusters.insert({'tier' + str(k) : CLUSTERS})
        mongo_clusters_inv.insert({'tier' + str(k) : CLUSTERS_INV})
        cluster_inv1 = CLUSTERS_INV['tier' + str(k) ]
        k = k-1
        j = j+1
    #print CLUSTERS_INV
    """
    cluster = CLUSTERS['tier7']['521450759']
    ids = CLUSTERS_INV['tier7'][cluster]
    print ids
    cluster = CLUSTERS['tier4']['521450759']
    ids = CLUSTERS_INV['tier4'][cluster]
    print ids
    """
    
    
        
    
    



if __name__=="__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print 'done with cluster after %.3f seconds'%(end_time-start_time)

