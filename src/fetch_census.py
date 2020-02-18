import pandas as pd
import numpy as np
from census_fetcher import census_fetcher, census_key

import os
src_directory = os.path.realpath(".")
home_directory = os.path.split(src_directory)[0]
data_directory = os.path.join(home_directory, "data")

def build_fields(query_dict):

    fields = []
    for table in query_dict.keys(): 
        for var in query_dict[table]: 
            fields.append(table+"_"+var)

    return tuple(fields)

def fetch_states(fetcher, variables, geoids, limiter=0):
    '''geoids must be unique for each state
    '''
    data = []
    for state in geoids:
        state_tracts = fetcher.get_state_tracts(variables, state)
        data.extend(state_tracts)
        print(f'Got state {str(state)}')

        limiter -= 1
        if limiter == 0:
            break

    return np.array(data)

def join_columns_as_str(df, columns, new_column):
    df[new_column] = df[columns].apply(lambda row : ''.join(row.astype(str)), axis=1)
    df.drop(columns=columns, inplace=True)


if __name__ == "__main__":

    from census_variables import query_dict, query_labels
    fields = build_fields(query_dict)

    tracts = pd.read_csv(f"{data_directory}/oz_acs_data_brookings.csv")
    states = np.unique(tracts['state_id']).astype(str)

    l = 0

    # build
    year, dataset = 2017, 'acs5'
    pax_fetcher = census_fetcher(census_key, year, dataset)
    data_columns = [t+"_"+v+str(year) for t in query_labels.keys() for v in query_labels[t]]
    data_columns.extend(['state', 'county', 'tract']) # the api also returns state, county, and tract

    # get 2017
    print("Getting {} data for {}".format(dataset, year))
    array = fetch_states(pax_fetcher, fields, states, limiter=l)
    seventeen = pd.DataFrame(array, columns=data_columns)
    join_columns_as_str(seventeen, ['state', 'county', 'tract'], 'geoid')

    # and 2012
    year = 2012
    pax_fetcher.year = year
    data_columns = [t+"_"+v+str(year) for t in query_labels.keys() for v in query_labels[t]]
    data_columns.extend(['state', 'county', 'tract']) # the api also returns state, county, and tract

    print("Getting {} data for {}".format(dataset, year))
    array = fetch_states(pax_fetcher, fields, states, limiter=l)
    twelve = pd.DataFrame(array, columns=data_columns)
    join_columns_as_str(twelve, ['state', 'county', 'tract'], 'geoid')

    # join and write
    fname = "census_raw.pkl"
    master = seventeen.merge(twelve, on='geoid')
    master.to_pickle(f"{data_directory}/{fname}")
    print(f"Wrote -->> {fname}")