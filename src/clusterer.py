import argparse
import pandas as pd 
import numpy as np 
from sklearn.cluster import KMeans, MeanShift, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, MaxAbsScaler
from sklearn.metrics import silhouette_samples

import matplotlib.pyplot as plt 
import seaborn as sns
from paxplot import cluster_plots, silhouette_plot, generate_feature_labels

## ---- default plotting style
plt.style.use('seaborn-ticks')
plt.rcParams['font.size'] = 16
sns.set_context(rc = {'patch.linewidth': 0.0, 'font.size':16.0})
palette = sns.color_palette(palette='deep')

class Clusterer():
    '''
    Wrapper for sklearn clustering algorithms also stores fitted data, feature names,
    calculates cluster centers and silhouette scores, and plots cluster centroids.
    '''

    def __init__(self, estimator, **kwargs):
        self.is_fit = False
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

    def _map_labels_to_centers(self):
        '''
        Helper for making centroids from aglorithms that do not return cluster centers.
        '''
        labels = self.attributes['labels_']
        clusters = np.unique(labels)

        centers = []
        for c in clusters:
            mask = (labels == c)
            this_cluster = self.X[mask]
            centers.append(np.mean(this_cluster, axis=0))

        return centers

    def fit(self, X, kwargs={}):
        '''
        Like sk-learn's .fit()

        Parameters ––––
        X: numpy.ndarray of shape (observations, features)
        kwargs: dictionary for sk-learn .fit() kwargs
        '''
        self.estimator.fit(X, **kwargs)
        self.is_fit = True
        
        self.X = X
        self.attributes = self.estimator.__dict__
        if self.name == 'dbscan':
            ## ? This isn't useful
            return self.attributes['core_sample_indices_']

        if self.name == 'agglomerative':
            self.attributes['cluster_centers_'] = self._map_labels_to_centers()

        return self.attributes['cluster_centers_']

    def fit_predict(self, X, kwargs={}):
        '''
        Like sk-learn's .fit_predict()

        Parameters ––––
        X: numpy.ndarray of shape (observations, features)
        kwargs: dictionary for sk-learn .fit() kwargs
        '''
        pass

    ## ––– Can't call these if unfitted
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

    def store_features(self, feature_names):
        '''
        Register feature labels for plotting.

        Parameters ––––
        feature_names: list of shape (features, )
        '''
        if np.shape(self.X)[1] != len(feature_names):
            print("Dimensions of fitted X and feature_names do not match.")
            return
        self.feature_names = feature_names

    def get_silhouette_samples(self):
        '''
        Returns silhouette scores for each observation in self.X, shape (observations, )
        '''
        return silhouette_samples(self.X, self.attributes['labels_'])

    def get_data(self):
        '''
        Return fitted data, shape (features, observations)
        '''
        return self.X, self.feature_names

    def get_centroids(self):
        '''
        Returns the centroid (mean feature values) of each fitted cluster, shape (n_clusters, features)
        '''
        return self.attributes['cluster_centers_']

    def plot_clusters_from_object(self, directory_for_plots):
        '''
        Saves cluster plots and silhouette plot to filepath directory_for_plots

        Parameters –––
        directory_for_plots: filepath where to put plots (string)
        '''
        
        ## get params
        feature_labels = generate_feature_labels(self.feature_names)
        centroids = self.get_centroids()
        k = self.attributes['n_clusters']

        ## make cluster plots
        cluster_plots(centroids, feature_labels)
        plt.savefig("{}/k={}.png".format(directory_for_plots, k), dpi=120, transparent=True)
        print("Made cluster plots.")

        ## make silhouette plot
        f, ax = plt.subplots(figsize=(7,7))
        silhouette_plot(ax, self)
        ax.legend(), f.tight_layout()
        plt.savefig("{}/silok={}".format(directory_for_plots, k), dpi=120, transparent=True)
        print("Made silhouette plot.")
        print("Plots @ {}".format(directory_for_plots))
