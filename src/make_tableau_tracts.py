import pandas as pd
from directory import data as data_dir

if __name__ == "__main__":

    model = 'kmeans'
    n_clusters = '6'

    clean = pd.read_pickle("{}/clean.pkl".format(data_dir))
    clean = clean[clean.columns[-4:]]
    labels = pd.read_pickle("{}/{}/labels.pkl".format(data_dir, model))
    filtr = [col for col in labels.columns if n_clusters in col]
    labels = labels[filtr]

    ozs = clean[clean['oz'] == 1].reset_index(drop=True)
    ozs = pd.concat([ozs, labels], axis=1)
    for_tableau = clean.merge(ozs, how="left")
    for_tableau['not_picked'] = (for_tableau['eligible'] +  for_tableau['oz']) % 2

    for_tableau.to_csv("{}/tableau_tracts.csv".format(data_dir))