import pandas as pd
import numpy as np

class census_featurizer():

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def     

if __name__ == "__main__":

    ## MAKE NEW COLUMNS
    pop = tracts['population_total']
    # note: race_total, poverty_total = population_total
    # mobility_total = total population > 1 year
    #     going to just use total population, looks closer than tenure_total
    # tenure_total = total population in occupied housing units
    # poverty = universe of people for whom poverty status is determined (!)
    tracts['p_black'] = tracts['race_black'] / pop
    tracts['p_white'] = tracts['race_white'] / pop
    tracts['poverty'] = tracts['poverty_poor'] / pop
    tracts['p_renting'] = tracts['tenure_renters'] / tracts['tenure_total']

    housing_units = tracts['structure_units_total']
    ## note : occupancy_total = structure_units_total
    tracts['vacancy'] = tracts['occupancy_vacant'] / housing_units
    tracts['p_mobilehomes'] = tracts['structure_units_mobile'] / housing_units
    tracts['p_multiple_unit_strucs'] = 1 - ((tracts['structure_units_one_a'] + tracts['structure_units_one_d']) / housing_units)

    ## ROUND
    tracts = tracts.round(decimals=3)

    ## PICK COLS
    cleaned = tracts[['population_total', 'age_median', 'p_never_married',\
            'p_white', 'p_black','poverty', 'household_income_median', \
            'home_value_median', 'structure_year_median', 'outofcountyflux',\
            'p_renting', 'vacancy', 'p_mobilehomes', 'p_multiple_unit_strucs']]

    pd.options.mode.chained_assignment = None  # default='warn'
    cleaned['state'] = states
    cleaned['tract'] = tract_numbers

    cleaned.reset_index(drop=True, inplace=True)
    file_out = "qozs_features.pkl"
    cleaned.to_pickle("{}/{}".format(data_directory, file_out))
    print("Cleaned -> {}".format(file_out))