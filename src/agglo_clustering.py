import argparse
import pickle
import pandas as pd 
import numpy as np 
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import silhouette_samples
from paxplot import generate_feature_labels
from clusterer import Clusterer
from directory import data, images
from clustering import drop_cols, drop_columns

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--plot', action='store_true',\
                        help='Update cluster and silhouette plots in images/<clusterer>')
    args = vars(parser.parse_args())
    do_plots = args['plot']

    ## load file
    model = 'agglomerative'
    linkage = "ward"
    filename = 'clean.pkl'
    print("Loading {}...".format(filename))
    clean = pd.read_pickle("{}/{}".format(data, filename))

    not_picked = clean[(clean['eligible'] == 1) & (clean['oz'] == 0)]
    picked = clean[clean['oz'] == 1]

    nonfeatures = drop_columns(picked, drop_cols)
    features = picked.columns

    ## standardize
    standardize = StandardScaler()
    X, features = picked.values, picked.columns.values
    X = standardize.fit_transform(X)

    ## build model
    cluster_labels = pd.DataFrame()
    for k in range(4, 10):
        pax = Clusterer(model, linkage=linkage, n_clusters=k)
        centers = pax.fit(X)
        feature_labels = generate_feature_labels(features)
        pax.store_features(feature_labels)

        ## What I need to do here is update the labels .pkl for column k 
        # cluster_labels["k={}".format(k)] = pax.attributes['labels_']
        # cluster_labels["k{}silhouette_score".format(k)] = silhouette_samples(X, pax.attributes['labels_'])
        # cluster_labels.to_pickle("{}/{}/labels.pkl".format(data, model))

        print("{} grouped {} clusters.".format(model, np.shape(centers)[0]))

        ### !
        with open("{}/{}/estimator.pkl".format(data, model), "wb") as c:
            pickle.dump(pax, c)

        if do_plots:
            ## map centroids back to features and plot
            from paxplot import cluster_plots, silhouette_plot
            import matplotlib.pyplot as plt 
            import seaborn as sns
            ## ---- styling
            plt.style.use('seaborn-ticks')
            plt.rcParams['font.size'] = 16
            sns.set_context(rc = {'patch.linewidth': 0.0, 'font.size':16.0})
            palette = sns.color_palette(palette='deep')

            ## make cluster plots
            cluster_plots(centers, feature_labels)
            plt.savefig("{}/kmeans/k={}.png".format(images, k), dpi=120, transparent=True)
            print("Made cluster plots.")

            ## make silhouette plot
            f, ax = plt.subplots(figsize=(7,7))
            silhouette_plot(ax, pax)
            ax.legend(), f.tight_layout()
            plt.savefig("{}/kmeans/silok={}".format(images, k), dpi=120, transparent=True)
            print("Made silhouette plot.\n")

    

    