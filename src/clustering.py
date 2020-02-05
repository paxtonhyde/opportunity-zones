import argparse
import pandas as pd 
import numpy as np 
from sklearn.cluster import KMeans, MeanShift
from sklearn.preprocessing import StandardScaler
from geography import fips_to_state

import os
this_directory = os.path.realpath(".")
home_directory = os.path.split(this_directory)[0]
data_directory = os.path.join(home_directory, "data")

if __name__ == "__main__":
    ## argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, default='qoz_model.pkl',\
                        help='''.pkl file with features. (Default: 'qoz_model.pkl')\n
                        note: Script will drop "state" and "tract" columns.''')
    parser.add_argument('-d', '--drop', type=str, default='tract state',\
                        help='''Columns to drop from file, separated by spaces. (Default: 'tract state') ''')
    parser.add_argument('-a', '--algorithm', type=str, default='meanshift',\
                        choices = ['meanshift', 'kmeans', 'dbscan'],
                        help='''Which scikit-learn clustering algorithm to use.
                        Options: 'meanshift' (default), 'kmeans', 'dbscan'.
                        note: If KMeans, specify k using '-k' or '--clusters'. ''')
    parser.add_argument('-k', '--clusters', type=int, default=8,\
                    help='''If clustering by KMeans, how many clusters to make. (Default: 8)''')                
    args = vars(parser.parse_args())

    filename, drop, clusterer, k = args['file'], args['drop'], args['algorithm'], args['clusters']

    ## Heavy arg lifting
    print("Loading {}...".format(filename))
    dataframe = pd.read_pickle(f"{data_directory}/{filename}")
    tract_ = dataframe['tract'].copy()
    for c in drop.split():
        try:
            dataframe.drop(columns=[c], inplace=True)
        except KeyError:
            print("Couldn't drop column '{}' from features matrix.".format(c))

    if clusterer == 'meanshift':
        pax_clusterer = MeanShift(bandwidth=None, n_jobs=-1, max_iter=300)
    elif clusterer == 'kmeans':
        pax_clusterer = KMeans(n_clusters=k, n_jobs=-1, verbose=1, \
            init='k-means++', n_init=10, max_iter=300, tol=0.0001)
    elif clusterer == 'dbscan':
        pass
    print("Clustering using: {}".format(pax_clusterer))

    ## MODEL
    standardize = StandardScaler()
    X, features = dataframe.values,\
        dataframe.columns.values
    X = standardize.fit_transform(X)
    pax_clusterer.fit(X)

    ## map centroids back to descriptive features
    centers_std = pax_clusterer.cluster_centers_
    centers = standardize.inverse_transform(centers_std)
    print("Grouped {} clusters.\n".format(centers.shape[0]))
    for c_i, c in enumerate(centers):
        print("--- Cluster {} ---".format(c_i))
        for i in range(len(features)):
            print("{} : {:.2f}".format(features[i], c[i]))

    ## next step: calculate majority state by cluster
    from collections import defaultdict

    dataframe['cluster'] = pax_clusterer.labels_
    dataframe['tract'] = tract_
    dataframe['state'] = dataframe['tract'].apply(lambda row : row[:2])
    sort_value, aggr, n = 'state', 'count', 3
    for cluster in np.unique(pax_clusterer.labels_):
        clus = dataframe[dataframe['cluster'] == cluster]
        clus = clus.groupby(sort_value).agg({ sort_value:aggr })
        column_name = sort_value + "_" + aggr
        clus.columns = [column_name]

        n_most = clus.sort_values(by=column_name, ascending=False)[:n]
        clus_size = np.sum(clus[column_name].values)
        info = defaultdict(list)
        for i, j in zip(n_most.index.values, n_most.values.flatten()):
            p = j/clus_size
            info[cluster] = [fips_to_state(i), round(p, 2)]
            #print("{} is {} of cluster {} ".format(fips_to_state(i), round(p, 2), cluster))

    print(info)