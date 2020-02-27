import pandas as pd
import numpy as np
from directory import data, images

from paxplot import centroid_plot, cluster_plots, scree_plot
from nmf import drop_cols
import matplotlib.pyplot as plt 
import seaborn as sns
plt.style.use('seaborn-ticks')
palette = sns.color_palette(palette='deep')
sns.set_context(rc = {'patch.linewidth': 0.0, 'font.size':16.0})

import sklearn.preprocessing as prepro
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import scipy.stats as sstats
import statsmodels.stats.weightstats as wstats

if __name__ == "__main__":
    clean = pd.read_pickle("{}/clean.pkl".format(data))
    not_picked = clean[(clean['eligible'] == 1) and (clean['oz'] == 0)]
    picked = clean[clean['oz'] == 1]

    X_n = not_picked.drop(columns=drop_cols)
    features= X_n.columns
    X = picked.drop(columns=drop_cols)
    data = [X, X_n]

    ## crunch numbers
    pca_objs = []
    for d in data:
        std_scaler = prepro.StandardScaler()
        std_X = std_scaler.fit_transform(d.values)
        n = 10
        paxPCA = PCA(n_components=n)
        pca_objs.append(paxPCA.fit(std_X))

    ## scree plots
    labels = ["Designated OZs", "Other eligible tracts"]
    for i, p in enumerate(pca_objs):
        f, axes = plt.subplots(2, 1, figsize=(20, 16))
        scree_plot(axes.flatten()[0], p, n_components_to_plot=n, title="{}".format(labels[i]))
        scree_plot(axes.flatten()[1], p, n_components_to_plot=n,\
                title="{}, cumulative".format(labels[i]), cumsum=True)
        plt.savefig("{}/pca_scree_{}.png".format(labels[i]), dpi=120, transparent=True)

    ## Plot first two components of picked and not picked to see separation
    fig, ax = plt.subplots(figsize=(10,8))
    n_points = 2000
    for i, p in enumerate(pca_objs):
        component_a = p.components_[0]
        component_b = p.components_[1]
        x = np.dot(data[i], component_a)[:n_points]
        y = np.dot(data[i], component_b)[:n_points]
        ax.scatter(x, y, color=palette[i+3], alpha=0.7, label=labels[i])
    
    ax.legend(fontsize=16)
    ax.set_title("Separation between designated and other eligible tracts", fontsize=18)
    ax.set_xlabel("Principal Component 0", fontsize=16)
    ax.set_ylabel("PC1", fontsize=16)
    plt.savefig("{}/pca_separation.png".format(images), dpi=120, transparent=True)

    ## z-test on each component
    for c in range(len(pca_objs[0].components_)):
        comp_ai = pca_objs[0].components_[c]
        comp_bi = pca_objs[1].components_[c]
        a = np.dot(data[0], comp_ai)[:n_points]
        b = np.dot(data[1], comp_bi)[:n_points]
        z, p = wstats.ztest(a, b)
        print("Z-statistic ––> {}, probability ––> {}".format(z, p))
    #     t, p = sstats.ttest_ind(a, b)
    #     print("t-statistic ––> {}, probability ––> {}".format(t, p))

    cluster_plots(pca_objs[0].components_, features)