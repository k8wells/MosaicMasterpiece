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
        count = 0
        for pic in pics:
            count = count + 1
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
        print count
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

    def assign_clusters(self, clusters):
        clusters_dict = {}
        cluster_dict_inv = {}
        i = 0
        for cluster in clusters:
            cluster_dict_inv[str(cluster)] = []
        for cluster in clusters:
            id = self.ids[i]
            clusters_dict[id] = str(cluster)
            cluster_dict_inv[str(cluster)].append(id)
            i = i+1
        return clusters_dict, cluster_dict_inv
        
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
    centroids,_ = kmeans(matrix,1000)
    clusters,_ = vq(matrix, centroids)
    print clusters
    clusters_dict, cluster_inv = cluster.assign_clusters(clusters)

    print clusters_dict
    print cluster_inv
    
    mongo_clusters.insert(clusters_dict)
    mongo_clusters_inv.insert(cluster_inv)
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

