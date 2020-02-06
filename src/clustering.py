import argparse
from collections import defaultdict
import pandas as pd 
import numpy as np 
from sklearn.cluster import KMeans, MeanShift, DBSCAN
from sklearn.preprocessing import StandardScaler, MaxAbsScaler
from geography import fips_to_state
from clusterer import Clusterer

import os
this_directory = os.path.realpath(".")
home_directory = os.path.split(this_directory)[0]
data_directory = os.path.join(home_directory, "data")
images_directory = os.path.join(home_directory, "images")

def majority_states(clusterlabels, dataframe, n_states=5):
    '''Calculates majority state by cluster.
    Pandas DataFrame with a state column
    '''
    info = defaultdict(list)
    sort_value, aggr, n_states = 'state', 'count', 5
    for c in np.unique(clusterlabels):
        clus = dataframe[dataframe['cluster'] == c]
        clus = clus.groupby(sort_value).agg({ sort_value:aggr })
        column_name = sort_value + "_" + aggr
        clus.columns = [sort_value + "_" + aggr]

        n_most = clus.sort_values(by=column_name, ascending=False)[:n_states]
        clus_size = np.sum(clus[column_name].values)

        for i, j in zip(n_most.index.values, n_most.values.flatten()):
            p = j/clus_size
            info[c].append((fips_to_state(i), round(p, 2)))

    return info

def map_cores_to_centers(dbscan, X):
    ''' Partially taken from the SKLearn website's DBSCAN demo.
    '''
    core_samples_mask = np.zeros_like(dbscan.labels_, dtype=bool)
    core_samples_mask[dbscan.core_sample_indices_] = True

    unique_labels_ = set(dbscan.labels_)
    cluster_centers = []
    for q in unique_labels_:
        if q == -1: ## -1 label in DBSCAN means unclustered
            continue
        class_mask = (dbscan.labels_ == q)
        cluster = X[core_samples_mask & class_mask] 
        cluster_centers.append(np.mean(cluster, axis=0))
    return cluster_centers

if __name__ == "__main__":

    ## load file
    filename = 'qoz_model.pkl'
    print("Loading {}...".format(filename))
    dataframe = pd.read_pickle(f"{data_directory}/{filename}")
    tract_ = dataframe['tract'].copy()
    states_ = dataframe['state'].copy()

    ## reorder columns
    order = ['Non-LIC', 'household_income_median', 'outofcountyflux', 'p_white', 'p_multiple_unit_strucs',\
        'home_value_median', 'structure_year_median', 'p_never_married', 'p_renting', 'vacancy',\
            'population_total', 'p_black', 'age_median', 'poverty', 'p_mobilehomes', 'state', 'tract']
    dataframe = dataframe[order]

    ## drop non-features (Eventually integrate this feature into Clusterer class)
    drop = 'state tract'
    for c in drop.split():
        try:
            dataframe.drop(columns=[c], inplace=True)
        except KeyError:
            print("Couldn't drop column '{}' from features matrix.".format(c))

    ## exclude LICs
    exclude_LIC = False
    if exclude_LIC:
        dataframe = dataframe[dataframe['Non-LIC'] == 1]

    ## standardize data
    standardize = StandardScaler()
    X, features = dataframe.values,\
        dataframe.columns.values
    X = standardize.fit_transform(X)

    algorithms = ['MeanShift', 'KMeans', 'DBSCAN']
    ## {eps:0.85, min_samples:5} = ~8
    ## w/o LIC {eps:2, min_samples:3} = 3
    n = 0
    k = 3
    ## build model
    pax = Clusterer(algorithms[n], drop, n_jobs=-1)
    centers = pax.fit(X)
    if algorithms[n] == 'DBSCAN':
        centers = map_cores_to_centers(pax.estimator, X)
    print("{} grouped {} clusters.\n".format(algorithms[n], np.shape(centers)[0]))

    ## map centroids back to descriptive features
    features = dataframe.columns
    ## , and plot
    from paxplot import style, cluster_plots
    import matplotlib.pyplot as plt 
    import seaborn as sns
    ## ---- styling
    plt.style.use('seaborn-ticks')
    sns.set_context(rc = {'patch.linewidth': 0.0})
    palette = sns.color_palette(palette='deep')

    cluster_plots(centers, features)
    plt.tight_layout()
    plt.savefig(f"{images_directory}/{algorithms[n]}_{'def'}.png", dpi=120)
    plt.show()

    ## calculate majority state by cluster

    pax_labels = pax.attributes['labels_']
    dataframe['cluster'] = pax_labels
    dataframe['tract'] = tract_
    dataframe['state'] = states_

    states = majority_states(pax_labels, dataframe)
    for k, v in states.items():
        print("Cluster {} states -> {}".format(k, v))

    cluster2 = dataframe[dataframe['cluster'] == 2]
    cluster2.to_pickle(f"{data_directory}/MScluster2.pkl")

    

    