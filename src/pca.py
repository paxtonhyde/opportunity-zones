import pandas as pd
import numpy as np

## –––– plotting style
import matplotlib.pyplot as plt 
import seaborn as sns
plt.style.use('seaborn-ticks')
palette = sns.color_palette(palette='deep').as_hex()
sns.set_context(rc = {'patch.linewidth': 0.0, 'font.size':16.0})

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import statsmodels.stats.weightstats as wstats

from directory import data as data_dir, images
from paxplot import scree_plot, centroid_plot, cluster_plots, pca_2comp_plot,\
     generate_feature_labels, percentage_plot
from clustering import drop_cols, drop_columns
drop_cols.remove("percent_tenure_owner2017")

def percent_differences(data1, data2):
    array = []
    for feature in range(len(data1[0, :])):
        a, b = data1[:, feature], data2[:, feature]
        percent_diff = (np.mean(a) - np.mean(b)) / np.mean(b)
        _, prob = wstats.ztest(a, b)
        array.append([percent_diff, prob])
    return np.array(array)

if __name__ == "__main__":
    labels = pd.read_pickle("{}/kmeans/labels.pkl".format(data_dir))
    clean = pd.read_pickle("{}/clean.pkl".format(data_dir))
    suspect = pd.read_pickle("{}/suspect_tracts.pkl".format(data_dir))
    drop_columns(suspect, drop_cols)

    X_all = clean[clean['eligible'] == 1]
    X_notpicked = X_all[X_all['oz'] == 0]
    X_picked = X_all[X_all['oz'] == 1].reset_index(drop=True)
    data = [X_notpicked, X_picked, X_all]
    for d in data:
        drop_columns(d, drop_cols)
    features= X_notpicked.columns
    feature_labels = generate_feature_labels(features)

    std_scaler = StandardScaler()
    std_X = std_scaler.fit_transform(X_all)
    n = 9 # explains ~90% of variance
    paxPCA = PCA(n_components=n)
    pca_all = paxPCA.fit(std_X)

    ## scree plot
    f, axes = plt.subplots(2, 1, figsize=(12, 8))
    scree_plot(axes.flatten()[0], pca_all, n_components_to_plot=n, title="Explained variance, all eligible tracts")
    scree_plot(axes.flatten()[1], pca_all, n_components_to_plot=n,\
            title="Cumulative explained variance, all eligible tracts", cumsum=True)
    f.tight_layout()
    # plt.savefig("{}/pca_scree_{}.png".format(labels[i]), dpi=120, transparent=True)

    ## Plot first two components of picked and not picked to see no separation
    fig, ax = plt.subplots(figsize=(15, 12))
    data_labels = ["Other eligible tracts", "Designated OZs"]
    data = data[:2]
    for i, d in enumerate(data):
        ## plot picked and not-picked
        pca_2comp_plot(ax, pca_all, data[i], n_points=3000, \
            scatter_kwargs={'color':palette[i+3],'alpha':0.7, 'label':data_labels[i]})

        # suspicious tracts
    pca_2comp_plot(ax, pca_all, suspect, show_centroid=False, \
            scatter_kwargs={'color':'k', 'marker':"*", 's':200,\
                            'alpha':0.9, 'label':'Identified \"suspicious\" tracts'})
    
    ax.set_title("No separation between picked and unpicked tracts", fontsize=24)
    # plt.savefig("{}/pca_noseparation.png".format(images), dpi=120, transparent=True)

    ## Plot PCA clusters
    n_clusters = 6
    k_labels = labels['k={}'.format(n_clusters)]
    cluster_masks = []
    for c in np.unique(k_labels): # for every label
        cluster_masks.append(k_labels == c)

    fig, ax = plt.subplots(figsize=(15, 12))
    data_labels = ['cluster 0', 'cluster 1', 'cluster 2', 'cluster 3',\
         'cluster 4', 'cluster 5', 'other eligible tracts']
    for i, d in enumerate(data):

        if i == 1: ## if we're looking at X_picked
            for j, mask in enumerate(cluster_masks):
                pca_2comp_plot(ax, pca_all, data[i][mask], n_points=1000, \
                    scatter_kwargs={'color':palette[j],'alpha':0.7, 'label':data_labels[j]})
        else:
            pca_2comp_plot(ax, pca_all, data[i], n_points=1500,\
                scatter_kwargs={'color':'gray','alpha':0.5, 'label':data_labels[-1]},\
                centroid_kwargs={'marker':"X", 's':150})
            
        ## show suspect tracts
    pca_2comp_plot(ax, pca_all, suspect, show_centroid=False, \
            scatter_kwargs={'color':'k', 'marker':"*", 's':200,\
                            'alpha':0.9, 'label':'Identified \"corrupt\" tracts'})

    ax.set_title("KMeans clusters", fontsize=24)
    # plt.savefig("{}/pca_clusters.png".format(images), dpi=120, transparent=True)

    ## plot significant differences between picked and nonpicked
        ## calculate significant differences
    pdiff = percent_differences(X_picked.values, X_all.values)
    diffs = pdiff[:,0]
    sig_zproba = pdiff[:, 1] < 0.05
        ## pick colors for plot
    color_seq = np.array([palette[7] for c in range(len(diffs))]) ## palette[7] is gray
    gainloss = np.where(diffs >= 0, palette[2], palette[3]) ## palette[2] and [3] are red/green for loss/gain
    color_seq[sig_zproba] = gainloss[sig_zproba]

        ## plot
    f = plt.figure(figsize=(10,8))
    f.subplots_adjust(left=0.25, right=0.9)
    ax = f.add_subplot(111)
    percentage_plot(ax, feature_labels, pdiff[:,0], kwargs={'color':color_seq})
    ax.set_title("OZ feature means relative to all eligible tracts", fontsize=22)
    ax.annotate('*Colored bars show \n significant differences', (320, 280), xytext = (285, 20),\
                xycoords='axes points', fontsize=16)
    f.tight_layout()
    # plt.savefig("{}/feature_comparison.png".format(images), dpi=120, transparent=True)
    plt.show()