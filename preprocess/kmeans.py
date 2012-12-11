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
        #id = 0
        #self.matrix_ids={}
        #self.matrix_ids_inv = {}
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

def main():
    mongo = pymongo.Connection('localhost', 27017)
    pics = mongo['my_database']['merged_info'].find()
    cluster = Clustering()
    array1 = cluster.index(pics)
    print array1
        
    """
    tfidf = transformer.fit_transform(array1)
    array_final = tfidf.toarray()
    """
    i = 1
    table = cluster.set_up_table(array1)
    matrix = cluster.find_matrix(table)
    print matrix
    centroids,_ = kmeans(matrix,6)
    clusters,_ = vq(matrix, centroids)
    print clusters
    print 'hi'
    print centroids
    



if __name__=="__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print 'done with cluster after %.3f seconds'%(end_time-start_time)

