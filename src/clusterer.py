import argparse
import pandas as pd 
import numpy as np 
from sklearn.cluster import KMeans, MeanShift, DBSCAN
from sklearn.preprocessing import StandardScaler
from geography import fips_to_state

import os
this_directory = os.path.realpath(".")
home_directory = os.path.split(this_directory)[0]
data_directory = os.path.join(home_directory, "data")

class Clusterer():
    '''
    '''

    def __init__(self, algorithm, drop, **kwargs):
        self.drop = drop
        if kwargs:
            self.estimator = self._pick_estimator(algorithm, kwargs)
        else:
            self.estimator = self._pick_estimator(algorithm)
        self.attributes = self.estimator.__dict__
        print("Using: {}".format(self.estimator))

    def _pick_estimator(self, algo_name, kwargs={}):
        '''
        Picks MeanShift by default.
        '''
        a = algo_name.strip().lower()
        if a == 'kmeans':
            return KMeans(**kwargs)
            ## defaults : 
        elif a == 'dbscan':
            return DBSCAN(**kwargs)
            ## defaults : 
        else:
            return MeanShift(**kwargs)
            ## defaults :

    def standardize(self, X, fit=True):
        ''' Around zero, unit variance.
        '''
        pass

    def unstandardize(self, standard_X):
        ''' Inverse transform to original dimensions.
        '''
        pass
    
    def fit(self, X, kwargs={}):
        self.estimator.fit(X, **kwargs)
        self.attributes = self.estimator.__dict__
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

if __name__ == "__main__":
    ##
    a = Clusterer('kmeans', 'state tract', n_clusters=11)
    ##
    b = Clusterer('kmeans', 'state tract')

    ## Why use soft versus hard clustering
    ## expand EDA
    ## do NMF
    ## start README