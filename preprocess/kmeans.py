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
        for id in ids:
            token = self.dict[id]
            table.addDocument(id,token)
        return table

    def assign_clusters(self, clusters):
        clusters_dict = {}
        cluster_dict_inv = {}
        cluster_dict_inv[0] = []
        cluster_dict_inv[1] = []
        cluster_dict_inv[2] = []
        cluster_dict_inv[3] = []
        cluster_dict_inv[4] = []
        cluster_dict_inv[5] = []
        cluster_dict_inv[6] = []
        cluster_dict_inv[7] = []
        cluster_dict_inv[8] = []
        cluster_dict_inv[9] = []
        i = 0
        for cluster in clusters:
            id = self.ids[i]
            clusters_dict[id] = cluster
            cluster_dict_inv[cluster].append(id)
            i = i+1
        return clusters_dict, cluster_dict_inv

    def assign_clusters2(self, clusters, starting_value, ids):
        clusters_dict = {}
        cluster_dict_inv = {}
        cluster_dict_inv[starting_value] = []
        cluster_dict_inv[starting_value+ 1] = []
        cluster_dict_inv[starting_value+2] = []
        cluster_dict_inv[starting_value+3] = []
        cluster_dict_inv[starting_value+4] = []
        cluster_dict_inv[starting_value+5] = []
        cluster_dict_inv[starting_value+6] = []
        cluster_dict_inv[starting_value+7] = []
        cluster_dict_inv[starting_value+8] = []
        cluster_dict_inv[starting_value+9] = []
        i = starting_value
        k = 0
        for cluster in clusters:
            id = ids[k]
            clusters_dict[id] = i
            cluster_dict_inv[i].append(id)
            i = i+1
            k = k+1
        return clusters_dict, cluster_dict_inv

    #def assign_clusters_inv(self, clusters):
        
    #for cluster in clusters:
            
            

def main():
    mongo = pymongo.Connection('localhost', 27017)
    pics = mongo['my_database']['merged_info'].find()
    cluster = Clustering()
    array1 = cluster.index(pics)
    table = cluster.set_up_table(array1)
    matrix = cluster.find_matrix(table)
    centroids,_ = kmeans(matrix,10)
    clusters,_ = vq(matrix, centroids)
    #print clusters
    #print 'hi'
    #print centroids
    starting_value = 0
    clusters_dict, cluster_inv = cluster.assign_clusters(clusters)
    CLUSTERS = {}
    CLUSTERS_INV = {}
    CLUSTERS['tier9'] = clusters_dict
    CLUSTERS_INV['tier9'] = cluster_inv
    #print clusters_dict
   # print cluster_inv

    ##SECOND ROUND
    i = 0
    k = 8
    while i < 10:
        #print cluster_inv
        ids = cluster_inv[i]
        #print ids
        if len(ids) > 1:
            table = cluster.set_up_table2(ids)
            matrix = cluster.find_matrix2(table, ids)
            #print matrix
            centroids,_ = kmeans(matrix,10)
            #print centroids
            clusters,_ = vq(matrix, centroids)
            #print clusters
            
            if 'tier'+str(k) in CLUSTERS.keys():
                starting_value = max(CLUSTERS.values()) + 1
                clusters_dict, cluster_inv = cluster.assign_clusters2(clusters,starting_value, ids)
                CLUSTERS['tier' + str(k) ].update(clusters_dict)
                CLUSTERS_INV['tier' + str(k) ].update(cluster_inv)
                
            else:
                starting_value = 0
                clusters_dict, cluster_inv = cluster.assign_clusters2(clusters,starting_value, ids)
                CLUSTERS['tier' + str(k) ] = clusters_dict
                CLUSTERS_INV['tier' + str(k) ] = cluster_inv

        i = i+1
    print CLUSTERS_INV
        
    
    



if __name__=="__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print 'done with cluster after %.3f seconds'%(end_time-start_time)

