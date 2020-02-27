import pandas as pd
import numpy as np
from directory import data, images

from paxplot import centroid_plot, cluster_plots, scree_plot
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

drop_cols = ['population_total2017', 'household_income_median2017',
    'home_value_median2017', 'housing_units_total2017', 'geoid', 'oz', 'LICadj', 'eligible']

if __name__ == "__main__":
    clean = pd.read_pickle("{}/clean.pkl".format(data))
    not_picked = clean[(clean['eligible'] == 1) and (clean['oz'] == 0)]
    picked = clean[clean['oz'] == 1]

    X_n = not_picked.drop(columns=drop_cols)
    features= X_n.columns
    X = picked.drop(columns=drop_cols)
    data = [X, X_n]