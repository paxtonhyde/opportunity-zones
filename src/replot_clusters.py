import pickle
import clusterer
from directory import data, images
import matplotlib.pyplot as plt 
import seaborn as sns
## ---- styling
plt.style.use('seaborn-ticks')
plt.rcParams['font.size'] = 16
sns.set_context(rc = {'patch.linewidth': 0.0, 'font.size':16.0})
palette = sns.color_palette(palette='deep')

if __name__ == "__main__":

    model = "kmeans"

    with open("{}/{}/estimator.pkl".format(data, model), "rb") as c:
        clusterer = pickle.load(c)

    plots_dir = "{}/{}".format(images, clusterer.name)
    clusterer.plot_clusters_from_object(plots_dir)

