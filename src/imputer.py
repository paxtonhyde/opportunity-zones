## to do: generalize for any file command line argument

## fancyimpute requires TensorFlow
import pandas as pd
import numpy as np
from fancyimpute import KNN
import argparse

import os
this_directory = os.path.realpath(".")
home_directory = os.path.split(this_directory)[0]
data_directory = os.path.join(home_directory, "data")

def add_LIC_col(dataframe):
    '''
    Add LIC/Non-LIC feature to dataframe of shape (tracts, features) with a census tract number column.
    '''
    LIC_column = pd.read_pickle("{}/qozs_1.pkl".format(data_directory))[['census_tract_number', 'Non-LIC']]
    LIC_column = LIC_column.rename(columns={'census_tract_number':'tract'})
    return dataframe.merge(LIC_column, how='left', on='tract')

if __name__ == "__main__":
    ## argument parsing
    parser = argparse.ArgumentParser()
    # parser.add_argument('-f', '--file', type=str,\
    #                     help='.pkl file with empty values.')
    parser.add_argument('-npr', '--NoPuertoRico', action='store_false',\
                        help='Exclude Puerto Rican tracts.')
    args = vars(parser.parse_args())
    exclude_PR = args['NoPuertoRico']

    ## start the work
    features = pd.read_pickle("{}/qozs_features.pkl".format(data_directory))
    states = [n[:2] for n in features['tract'].values]

    if exclude_PR:
        PR_print, PR_file_extension = 'Ex', '_plusPR'
        PR_idx = np.argwhere(np.array(states) == '72').reshape(-1)
        feature = features.drop(PR_idx)
        features.reset_index(inplace=True, drop=True)
    else:
        PR_print, PR_file_extension = 'In', ''
    print("{}cluding Puerto Rico tracts.".format(PR_print))

    incomplete = features.drop(columns=['state','tract'])
    filled_matrix = KNN(k=3).fit_transform(incomplete.values)
    filled = pd.DataFrame(filled_matrix, columns = incomplete.columns)

    # add non-LIC column, tract number, and state number
    filled['tract'] = features['tract']
    filled['state'] = states

    filled = add_LIC_col(filled)

    file_out = "qoz_model{}.pkl".format(PR_file_extension)
    filled.to_pickle("{}/{}".format(data_directory, file_out))
    print('Imputed file -> {}'.format(file_out))