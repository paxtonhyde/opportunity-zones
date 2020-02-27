import argparse
import pandas as pd 
import numpy as np 
from sklearn.cluster import KMeans, MeanShift, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, MaxAbsScaler

import os
this_directory = os.path.realpath(".")
home_directory = os.path.split(this_directory)[0]
data_directory = os.path.join(home_directory, "data")

class Clusterer():
    '''
    '''

    def __init__(self, estimator, **kwargs):
        self.name = estimator.lower()

        if kwargs:
            self.estimator = self._pick_estimator(estimator, kwargs)
        else:
            self.estimator = self._pick_estimator(estimator)
        self.attributes = self.estimator.__dict__
        print("Using: {}".format(self.estimator))

    def _pick_estimator(self, algo_name, kwargs={}):
        '''
        Picks KMeans by default.
        '''
        a = algo_name.strip().lower()
        if a == 'agglomerative':
            return AgglomerativeClustering(**kwargs)
            ## defaults : 
        elif a == 'dbscan':
            return DBSCAN(**kwargs)
            ## defaults : 
        else:
            return KMeans(**kwargs)
            ## defaults :

    def _map_labels_to_centers(self, X):
        labels = self.attributes['labels_']
        clusters = np.unique(labels)

        centers = []
        for c in clusters:
            mask = (labels == c)
            this_cluster = X[mask]
            centers.append(np.mean(this_cluster, axis=0))

        return centers

    def fit(self, X, kwargs={}):
        ''' .fit() will not standardize X
        '''
        self.estimator.fit(X, **kwargs)
        self.attributes = self.estimator.__dict__
        if self.name == 'dbscan':
            return self.attributes['core_sample_indices_']
        elif self.name == 'agglomerative':
            return self._map_labels_to_centers(X)
        else:
            return self.attributes['cluster_centers_']
    
    ## for the future
    def score(self):
        ## if not KMeans:
        ## reject
        pass

    def predict(self, X):
        ## if KMeans:
        ## self.estimator.predict()
        ## else:
        ## self.fit_predict()
        pass

    def fit_predict(self, X):
        pass
