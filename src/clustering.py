import argparse
import pickle
import pandas as pd 
import numpy as np 
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_samples
from paxplot import generate_feature_labels
from clusterer import Clusterer
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
    model = 'kmeans'
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
    for k in range(6, 7):
        pax = Clusterer(model, n_clusters=k, random_state=24)
        centers = pax.fit(X)
        pax.store_features(features)
        print("{} grouped {} clusters.".format(model, np.shape(centers)[0]))


        ## update labels and scores for column k
        filepath = "{}/{}/labels.pkl".format(data, model)
        with open(filepath, "rb") as f:
            k = pax.attributes['n_clusters']
            model_labels_df = pickle.load(f)
            model_labels_df["k={}".format(k)] = pax.attributes['labels_']
            model_labels_df["k{}silho_score".format(k)] = pax.get_silhouette_samples()
        model_labels_df.to_pickle(filepath)
        print("Updated labels @ {}".format(filepath))

        ### !
        filepath = "{}/{}/estimator.pkl".format(data, model)
        with open(filepath, "wb") as c:
            pickle.dump(pax, c)
            print("Clusterer object @ {}".format(filepath))

        if do_plots:
            with open("{}/{}/estimator.pkl".format(data, model), "rb") as c:
                clusterer = pickle.load(c)

            ## map centroids back to features and plot
            import matplotlib.pyplot as plt 
            import seaborn as sns
            ## ---- styling
            plt.style.use('seaborn-ticks')
            plt.rcParams['font.size'] = 16
            sns.set_context(rc = {'patch.linewidth': 0.0, 'font.size':16.0})
            palette = sns.color_palette(palette='deep')


            plots_dir = "{}/{}".format(images, clusterer.name)
            clusterer.plot_clusters_from_object(plots_dir)