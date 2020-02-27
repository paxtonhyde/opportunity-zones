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
        self.dbscan = False
        self.name = estimator

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
            self.dbscan = True
            return DBSCAN(**kwargs)
            ## defaults : 
        else:
            return KMeans(**kwargs)
            ## defaults :

    def fit(self, X, kwargs={}):
        ''' .fit() will not standardize X
        '''
        self.estimator.fit(X, **kwargs)
        self.attributes = self.estimator.__dict__
        if self.dbscan:
            return self.attributes['core_sample_indices_']
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