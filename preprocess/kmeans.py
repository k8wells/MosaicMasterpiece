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
            print pic
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

    #def assign_clusters_inv(self, clusters):
        
    #for cluster in clusters:
            
            

def main():
    mongo = pymongo.Connection('localhost', 27017)
    pics = mongo['my_database']['merged_info'].find()
    cluster = Clustering()
    array1 = cluster.index(pics)
    #print array1
    table = cluster.set_up_table(array1)
    matrix = cluster.find_matrix(table)
    #print matrix
    centroids,_ = kmeans(matrix,6)
    clusters,_ = vq(matrix, centroids)
    #print clusters
    #print 'hi'
    #print centroids
    clusters_dict, cluster_inv = cluster.assign_clusters(clusters)
    print clusters_dict
    print cluster_inv

    ##SECOND ROUND

    
    



if __name__=="__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print 'done with cluster after %.3f seconds'%(end_time-start_time)

