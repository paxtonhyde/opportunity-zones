import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns
plt.style.use('seaborn')

def centroid_plot(ax, features, centroid):
    '''Plot weightings of each feature on the cluster. Set ax title outside.
    Params:
        ax: Matplotlib ax object to plot on
        features: array of strings (n,)
        centroid: array of weightings (n,)
    '''
    y = np.arange(len(centroid))
    ax.barh(y, centroid, tick_label=features)

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