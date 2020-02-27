import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns
plt.style.use('seaborn-ticks')
sns.set_context(rc = {'patch.linewidth': 0.0, 'font.size':16.0})
palette = sns.color_palette(palette='deep')
from directory import data, images

from sklearn.cluster import KMeans, DBSCAN, MeanShift
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_samples, silhouette_score

def silhouette_plot(ax1, clusterer, X):
    ## Loosely adapted from https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html

    labels_ = clusterer.attributes['labels_']
    n_clusters = clusterer.attributes['n_clusters']

    # The silhouette coefficient can range from [-1, 1]
    x_low, x_high = -0.3, 0.8
    ax1.set_xlim([x_low, x_high])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

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

    ax1.set_title("{} (k={})".format(clusterer.name, n_clusters), fontsize=18)
    ax1.set_xlabel("Silhouette coefficient")
    ax1.set_ylabel("Cluster")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="k", linestyle="--", alpha = 0.7,
        label="mean silhouette score: {:.3f}".format(silhouette_avg))

    ax1.set_yticks([])  # Clear the y-axis
    ax1.set_xticks(np.linspace(x_low, x_high, num=7))


def centroid_plot(ax, features, centroid, kwargs={}):
    '''Plot weightings of each feature on the cluster. Set ax title outside.
    Params:
        ax: Matplotlib ax object to plot on
        features: array of strings (n,)
        centroid: array of weightings (n,)
    '''
    y = np.arange(len(centroid))
    ax.barh(y, centroid, tick_label=features, **kwargs)
    ax.set_yticklabels(features, )
    ax.set_xlim(np.min(centroid) - 0.3, np.max(centroid) + 0.7)


def cluster_plots(clusters, features, sns_palette='deep'):
    '''Not tested for n_components > 8
        *Look at figsize, 
    '''
    n_comp, h = np.shape(clusters)[0], clusters
    if n_comp > 4:
        figshape = (2, n_comp // 2+(n_comp%2))
    else:
        figshape = (1, n_comp)

    fig, axes = plt.subplots(figshape[0], figshape[1], figsize=(20, 10))
    palette = sns.color_palette(palette=sns_palette)

    i = 0
    for ax, c in zip(axes.flatten(), h):
        centroid_plot(ax, features, c, kwargs={'color':palette.as_hex()[i],'alpha':0.9})
        ax.set_title("Cluster {}".format(i), fontsize=18)
        if i%figshape[1] != 0:
            ax.set_yticklabels([])
            ax.set_yticks([])
        i+=1
        
    fig.tight_layout()
    

def scree_plot(ax, pca, n_components_to_plot=8, title=None, cumsum=False):
    """Scree plot showing the variance (default) or cumulative variance explained
    for the principal components in a fit sklearn PCA object.
    
    Parameters –––
    ax: matplotlib.axis object
    pca: sklearn.decomposition.PCA object, fitted.
    n_components_to_plot: int
    title: str (optional)
    cumsum: bool (optional)
    """
    if cumsum:
        vals = np.cumsum(pca.explained_variance_ratio_)
        y_label, y_pos = "Cumulative ", -1
    else:
        vals = pca.explained_variance_ratio_
        y_label, y_pos = "", 1
        
    num_components = pca.n_components_
    ind = np.arange(num_components)
    ax.plot(ind, vals, color='blue')
    ax.scatter(ind, vals, color='blue', s=50)

    for i in range(num_components):
        ax.annotate(r"{:2.0f}%".format(vals[i]*100), 
               (ind[i]+(y_pos*0.2), vals[i]+0.005), 
               va="bottom", 
               ha="center", 
               fontsize=12)

    ax.set_xticks(ind)
    ax.set_xticklabels(ind + 1, fontsize=12)
    ax.set_ylim(0, max(vals) + 0.05)
    ax.set_xlabel("Principal Component", fontsize=12)
    ax.set_ylabel("{}Variance Explained".format(y_label), fontsize=12)
    if title is not None:
        ax.set_title(title, fontsize=16)