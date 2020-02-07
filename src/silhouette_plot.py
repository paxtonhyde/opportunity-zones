import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import seaborn as sns

## ---- styling
plt.style.use('seaborn-ticks')
sns.set_context(rc = {'patch.linewidth': 0.0})
palette = sns.color_palette(palette='deep')

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans, DBSCAN, MeanShift
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_samples, silhouette_score

import os
this_directory = os.path.realpath(".")
home_directory = os.path.split(this_directory)[0]
data_directory = os.path.join(home_directory, "data")
images_directory = os.path.join(home_directory, "images")

if __name__ == "__main__":
    ## Adapted from https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html

    ## load file
    filename = 'qoz_model.pkl'
    dataframe = pd.read_pickle(f"{data_directory}/{filename}")

    ## reorder columns
    order = ['Non-LIC', 'household_income_median', 'outofcountyflux', 'p_white', 'p_multiple_unit_strucs',\
        'home_value_median', 'structure_year_median', 'p_never_married', 'p_renting', 'vacancy',\
            'population_total', 'p_black', 'age_median', 'poverty', 'p_mobilehomes']
    dataframe = dataframe[order]

    ## standardize data
    standardize = StandardScaler()
    X, features = dataframe.values,\
        dataframe.columns.values
    X = standardize.fit_transform(X)

    ## plotting
    range_n_clusters = np.arange(6, 14)
    for n_clusters in range_n_clusters:

        fig, ax1 = plt.subplots()
        fig.set_size_inches(7, 7)

        # The 1st subplot is the silhouette plot
        # The silhouette coefficient can range from -1, 1 but in this example all
        # lie within [-0.1, 1]
        x_low, x_high = -0.3, 0.8
        ax1.set_xlim([x_low, x_high])
        # The (n_clusters+1)*10 is for inserting blank space between silhouette
        # plots of individual clusters, to demarcate them clearly.
        ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

        # using KMeans
        clusterer = DBSCAN(eps=0.87, min_samples=5, n_jobs=-1)
        labels_ = clusterer.fit_predict(X)

        silhouette_avg = silhouette_score(X, labels_)
        sample_silhouette_values = silhouette_samples(X, labels_)

        y_lower = 10
        for i in range(n_clusters):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = \
                sample_silhouette_values[labels_ == i]

            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = palette.as_hex()[i%10]
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                            0, ith_cluster_silhouette_values,
                            facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax1.set_title(f"DBSCAN")
        ax1.set_xlabel("Silhouette coefficient")
        ax1.set_ylabel("Cluster")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="k", linestyle="--", label=f"{round(silhouette_avg, 3)}")

        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks(np.linspace(x_low, x_high, num=6))

        # # 2nd Plot showing the actual clusters formed
        # colors = palette.as_hex()[i%10]
        # ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
        #             c=colors, edgecolor='k')

        # # Labeling the clusters
        # centers = clusterer.cluster_centers_
        # # Draw white circles at cluster centers
        # ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
        #             c="white", alpha=1, s=200, edgecolor='k')

        # for i, c in enumerate(centers):
        #     ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
        #                 s=50, edgecolor='k')

        # ax2.set_title("The visualization of the clustered data.")
        # ax2.set_xlabel("Feature space for the 1st feature")
        # ax2.set_ylabel("Feature space for the 2nd feature")

        # plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
        #             "with n_clusters = %d" % n_clusters),
        #             fontsize=14, fontweight='bold')

        plt.legend()
        plt.savefig(f"{images_directory}/silo_DBeps87m5.png")
        break
