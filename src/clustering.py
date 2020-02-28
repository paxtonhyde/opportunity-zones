import pandas as pd 
import numpy as np 
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_samples
from clusterer import Clusterer
import argparse

from directory import data, images

drop_cols = ['percent_tenure_owner2017', 'age_median2017', 'population_total2017',\
     'household_income_median2017','home_value_median2017', 'housing_units_total2017', 'geoid',\
     'oz', 'LICadj', 'eligible']

def drop_columns(dataframe, columns):
    dropped = dataframe[columns]
    for c in columns:
        try:
            dataframe.drop(columns=[c], inplace=True)
        except KeyError:
            print("Couldn't drop column '{}' from features matrix.".format(c))
    return dropped

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--plot', action='store_true',\
                        help='Update cluster and silhouette plots in images/<clusterer>')
    args = vars(parser.parse_args())
    do_plots = args['plot']

    ## load file
    filename = 'clean.pkl'
    print("Loading {}...".format(filename))
    clean = pd.read_pickle(f"{data}/{filename}")

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
    for k in range(3, 10):
        model = 'kmeans'
        pax = Clusterer(model, n_clusters=k, random_state=24)
        centers = pax.fit(X)
        cluster_labels["k={}".format(k)] = pax.attributes['labels_']
        cluster_labels["k{}silhouette_score".format(k)] = silhouette_samples(X, pax.attributes['labels_'])
        print("{} grouped {} clusters.".format(model, np.shape(centers)[0]))

        ## map centroids back to descriptive features
        ## and plot
        from paxplot import cluster_plots, silhouette_plot, generate_feature_labels
        import matplotlib.pyplot as plt 
        import seaborn as sns
        ## ---- styling
        plt.style.use('seaborn-ticks')
        plt.rcParams['font.size'] = 16
        sns.set_context(rc = {'patch.linewidth': 0.0, 'font.size':16.0})
        palette = sns.color_palette(palette='deep')
        feature_labels = generate_feature_labels(features)

        if do_plots:
            ## make cluster plots
            cluster_plots(centers, feature_labels)
            plt.savefig("{}/kmeans/k={}.png".format(images, k), dpi=120, transparent=True)
            print("Made cluster plots.")

            ## make silhouette plot
            f, ax = plt.subplots(figsize=(7,7))
            silhouette_plot(ax, pax, X)
            ax.legend(), f.tight_layout()
            plt.savefig("{}/kmeans/silok={}".format(images, k), dpi=120, transparent=True)
            print("Made silhouette plot.\n")

            cluster_labels.to_pickle("{}/{}labels.pkl".format(data, model))