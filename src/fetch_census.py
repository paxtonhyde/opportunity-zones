import pandas as pd
from get_census import census_fetcher, census_key

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

if __name__ == "__main__":

    import OZ_variables
    q_dict, labels = OZ_variables.query_dict, OZ_variables.query_labels
    OZ_fields = build_fields(q_dict)

    QOZs = pd.read_pickle(f"{data_directory}/qozs_clean.pkl")['census_tract_number'].astype(str)

    dataset = 'acs5'
    year = 2015
    pax_fetcher = census_fetcher(census_key, year, dataset)

    census_data_columns = [t+"_"+v for t in labels.keys() for v in labels[t]]
    QOZ_census_data = pd.DataFrame(columns=census_data_columns)

    ## do it by 500 line block?, also could write line by line
    limiter = 9000
    for tract in QOZs.values:
        tract_data = pax_fetcher.get_tract_data(OZ_fields, tract)
        tract_data = [d for d in tract_data]
        print(f'Got {str(tract)}')

        row = pd.DataFrame([tract_data], columns=census_data_columns)

        ## !!! requires ~2X the size of the dataframe in memory
        QOZ_census_data = QOZ_census_data.append(row, ignore_index=True)
        print(QOZ_census_data)
        if limiter <= 0:
            break
        limiter -= 1

    #QOZ_census_data['tract_number'] = QOZs.values[:limiter]

    QOZ_census_data.to_pickle(f"{data_directory}/{dataset}-{str(year)[-2:]}.csv")