#!/usr/bin/env python
# script to test your k-means algorithm
import unittest
import utils
import cluster3
import math


TEST_CORPUS2 = [
    {
         "filename":"1000000000",
         "tags":"cat lion roar savannah africa",
    },
    {
        "filename":"2000000000",
        "tags":"antelope savannah africa tree",
    },
    {
        "filename":"3000000000",
        "tags":"cat house meow silly house",
    },
    {
        "filename":"4000000000",
        "tags":"sunset africa tree savannah",
    },
    {
        "filename":"5000000000",
        "tags":"house silly game dog",
    },
    {
        "filename":"6000000000",
        "tags":"dog sniff frisbee game",
    },
    {
        "filename":"0000000007",
        "tags":"cat meow window house",
    },
    {
        "filename":"8000000000",
        "tags":"car camaro red race",
    },
    {
        "filename":"9000000000",
        "tags":"race truck red crash",
    },
    {
        "filename":"0000000010",
        "tags":"orange sunset fish boat",
    },
        {
        "filename":"0000000011",
        "tags":"fish blue ocean boat",
    },
    {
        "filename":"0000000012",
        "tags":"decoration people door holiday",
    },
        {
        "filename":"0000000013",
        "tags":"decoration christmas people tree holiday",
    },
        {
        "filename":"0000000014",
        "tags":"people thanksgiving eat house holiday",
    },
    {
        "filename":"0000000015",
        "tags":"homework sad people book study",
    },
    {
        "filename":"0000000016",
        "tags":"book paper sad assignment homework study",
    }
    ]

TEST_CORPUS = [
    {
         "filename":"1",
         "tags":"cat lion roar savannah africa",
    },
    {
        "filename":"2",
        "tags":"antelope savannah africa tree ",
    },
    {
        "filename":"3",
        "tags":"cat house meow silly house",
    },
    
    {
        "filename":"5",
        "tags":"house silly dog",
    },
    {
        "filename":"6",
        "tags":"dog sniff frisbee game",
    },
    {
        "filename":"7",
        "tags":"cat meow window house",
    },
    {
        "filename":"8",
        "tags":"car camaro red race",
    },
    {
        "filename":"9",
        "tags":"race truck red crash",
    },
    {
        "filename":"4",
        "tags":"sunset africa tree savannah",
    },
    {
        "filename":"10",
        "tags":"orange sunset fish boat",
    },
        {
        "filename":"11",
        "tags":"fish blue ocean boat",
    },
    {
        "filename":"12",
        "tags":"decoration people door holiday",
    },
    {
        "filename":"13",
        "tags":"decoration christmas people tree holiday",
    },
    {
        "filename":"14",
        "tags":"people thanksgiving eat house holiday",
    },
    {
        "filename":"15",
        "tags":"homework sad people book study",
    },
    {
        "filename":"16",
        "tags":"book paper sad assignment homework study",
    }
    ]

class TestClustering(unittest.TestCase):
    def setUp(self):
        self.cluster = cluster3.Cluster()
        #self.info = self.cluster.concatenate(TEST_CORPUS)

        self.cluster.index(TEST_CORPUS)
        size = self.cluster.find_beginning_size()
        i = 1
        table = self.cluster.set_up_table(i-1)
        matrix = self.cluster.init_matrix(TEST_CORPUS, i, table)
        pairs = self.cluster.find_closest_pairs(matrix)
        new_matrix = self.cluster.combine_pairs(matrix, pairs, i)
        i = i +1
        while i<size:
            table = self.cluster.set_up_table(i-1)
            matrix=self.cluster.find_matrix(new_matrix,i,table)
            pairs = self.cluster.find_closest_pairs(matrix)
            new_matrix = self.cluster.combine_pairs(matrix, pairs, i)
            i = i+1

        self.cluster1 = self.cluster.clusters
        self.cluster1inv = self.cluster.clusters_inv

    def test_cluster1(self):
        # tests to make sure picture 15 and 16 are in the same cluster
        values =  self.cluster1['tier8'].values()
        ans = 'FALSE'
        for value in values:
            if '15' and '16' in value:
                ans = 'TRUE'
        self.assertEqual('TRUE', ans)

    def test_cluster2(self):
        # tests to make sure picture 1 and 2 are in the same cluster
        values =  self.cluster1['tier9'].values()
        ans = 'FALSE'
        for value in values:
            if '1' and '2' in value:
                ans = 'TRUE'
        self.assertEqual('TRUE', ans)

    def test_cluster_begin(self):
        # tests to make sure the initial iteration starts with having each doc as its own cluster
        num_clusters =  len(self.cluster1['tier0'].keys())
        self.assertEqual(num_clusters, 16)

    def test_cluster_end(self):
        # tests to make sure the last iteration reveals two main clusters
        num_clusters =  len(self.cluster1['tier15'].keys())
        self.assertEqual(num_clusters, 2)
        
    def test_all_clustered(self):
        #tests to make sure every picture is included in a cluster
        keys = self.cluster1['tier4'].values()
        picids = []
        for key in keys:
            for k in key:
                picids.append(k)
        self.assertTrue('1' in picids)
        self.assertTrue('2' in picids)
        self.assertTrue('3' in picids)
        self.assertTrue('4' in picids)
        self.assertTrue('5' in picids)
        self.assertTrue('6' in picids)
        self.assertTrue('7' in picids)
        self.assertTrue('8' in picids)
        self.assertTrue('9' in picids)
        self.assertTrue('10' in picids)
        self.assertTrue('11' in picids)
        self.assertTrue('12' in picids)
        self.assertTrue('13' in picids)
        self.assertTrue('14' in picids)
        self.assertTrue('15' in picids)
        self.assertTrue('16' in picids)
            

if __name__ == '__main__':
    unittest.main()

