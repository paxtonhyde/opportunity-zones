import pandas as pd 
import numpy as np 
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_samples
from clusterer import Clusterer
from nmf import drop_cols

from directory import data, images

def drop_columns(dataframe, columns):
    dropped = dataframe[columns]
    for c in columns:
        try:
            dataframe.drop(columns=[c], inplace=True)
        except KeyError:
            print("Couldn't drop column '{}' from features matrix.".format(c))
    return dropped

if __name__ == "__main__":

    ## load file
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
        model = 'agglomerative'
        linkage = "ward"
        pax = Clusterer(model, linkage=linkage, n_clusters=k)
        centers = pax.fit(X)
        cluster_labels["k={}".format(k)] = pax.attributes['labels_']
        cluster_labels["k{}silhouette_score".format(k)] = silhouette_samples(X, pax.attributes['labels_'])
        print("{} grouped {} clusters.".format(model, np.shape(centers)[0]))

        ## map centroids back to descriptive features
        ## and plot
        from paxplot import cluster_plots, silhouette_plot
        import matplotlib.pyplot as plt 
        import seaborn as sns
        ## ---- styling
        plt.style.use('seaborn-ticks')
        plt.rcParams['font.size'] = 16
        sns.set_context(rc = {'patch.linewidth': 0.0, 'font.size':16.0})
        palette = sns.color_palette(palette='deep')

        ## make cluster plots
        cluster_plots(centers, features)
        imagepath = "{}/agglo"
        plt.savefig("{}/k={}.png".format(imagepath, k), dpi=120, transparent=True)
        print("Made cluster plots.")

        ## make silhouette plot
        f, ax = plt.subplots(figsize=(7,7))
        silhouette_plot(ax, pax, X)
        f.tight_layout()
        ax.legend()
        plt.savefig("{}/silok={}".format(imagepath, k), dpi=120, transparent=True)
        print("Made silhouette plot.-->{}\n".format(imagepath))

    cluster_labels.to_pickle("{}/{}labels.pkl".format(data, model))

    

    