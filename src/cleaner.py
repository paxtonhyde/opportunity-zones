## fancyimpute requires TensorFlow
import pandas as pd
import numpy as np
# from fancyimpute import KNN
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from census_variables import delta_features, universe_to_column_mapping
from directory import data

def remove_bad_tracts(messy_df, useless_columns_if_zero):
    # 1 : tracts where the API returned nothing
    a = (messy_df.drop(columns=['geoid']) != -1)
    step_one = messy_df[a.all(axis=1)]

    # 2 : tracts with no information
    u = useless_columns_if_zero
    if type(u) == str or len(u) == 1:
        empty_line_mask = step_one[u] != 0
    elif type(u) == list:
        empty_line_mask = step_one[u[0]] != 0
        for i in range(1, len(u)):
            empty_line_mask = np.logical_or(empty_line_mask , step_one[u[i]] != 0)
    else:
        raise TypeError('''"useless_columns_if_zero" must be type str or list.''')
    step_two = step_one[empty_line_mask]

    print("Removed {} tracts with bad data.".format(len(messy_df) - len(step_two)))

    # 3 : replace negative values (entry errors) with nan (preparation for imputation)
    step_three = step_two.where(step_two[step_two.columns.difference(['geoid'])] >= 0, errors='ignore')
    step_three['geoid'] = step_two['geoid']
    n_nan_lines = np.count_nonzero(step_three.isna().any(axis=1))

    print("{} lines ({}%) had at least one NaN.".format(n_nan_lines, round((n_nan_lines / len(step_three)), 2)*100 ))

    return step_three


def make_percent_columns(dataframe, universe_to_column_mapping, years):
    '''
    Should be called before make_delta_columns()
    '''
    m = universe_to_column_mapping
    for y in years:
        y = str(y)
        for universe in m:
            
            columns = m[universe]
            for c in columns:
                if type(c) == str:
                    new_col_name = "percent_{}{}".format(c, y)
                    dataframe[new_col_name] = dataframe[c + y] / dataframe[universe + y]
                    if c not in delta_features:
                        dataframe.drop(columns=[c+y], inplace=True)
                    
                else:
                    for key in c:
                        cols_to_sum = [value + y for value in c[key]]
                        total = dataframe[cols_to_sum].sum(axis=1)
                        new_col_name = "percent_{}{}".format(key, y)
                        dataframe[new_col_name] = total / dataframe[universe + y]
                        dataframe.drop(columns=cols_to_sum, inplace=True)

            if universe not in delta_features:
                dataframe.drop(columns=[universe + y], inplace=True)
    return dataframe


def make_delta_columns(dataframe, columns_no_year, years):
    for c in columns_no_year:    
        delta = []

        for y in sorted(years):
            delta.append(c + str(y))
            
        dataframe["change_{}".format(c)] = ( dataframe[delta[1]] - dataframe[delta[0]] ) / dataframe[delta[0]]
        dataframe.drop(columns=delta, inplace=True)
    return dataframe


if __name__ == "__main__":
# loading
    file_suffix = ""
    raw = pd.read_pickle("{}/census_raw.pkl".format(data))

# cleaning
    columns_that_render_useless = [c for c in raw.columns if c.startswith("population")]
    clean = remove_bad_tracts(raw, columns_that_render_useless)
    geoids = clean.geoid # save
    clean.drop(columns=['geoid'], inplace=True)

# missing value imputation
    print("Imputing features using KNN.")
    standard = StandardScaler()
    X = standard.fit_transform(clean.values)
    filled = KNNImputer(n_neighbors=3).fit_transform(X)
    imputed = pd.DataFrame(standard.inverse_transform(filled), columns=clean.columns)

# featurize
    print("Making features.")
    featurized = make_percent_columns(imputed, universe_to_column_mapping, [2017])
    f = make_delta_columns(featurized, delta_features, [2017, 2012])
    f.drop(columns=[c for c in f.columns if c.endswith("2012")], inplace=True)

# adding brookings features
    brookings = pd.read_csv("{}/oz_acs_data_brookings.csv".format(data))
    brookings['geoid'] = brookings['geoid'].apply(lambda row: "0" + str(row) if len(str(row)) == 10 else str(row))
    brookings['LICadj'] = brookings['eligible'].apply(lambda row: 1 if row == "Contiguous" else 0)
    brookings['eligible'] = brookings['eligible'].apply(lambda row: 0 if row == "Not Eligible" else 1)
    brookings['oz'] = brookings['picked']
    brookings[['distress_index', 'z_score_distress_index']].to_pickle("{}/brookings_distress_idx.pkl".format(data))

    f['geoid'] = geoids
    final = f.merge(brookings[['geoid', 'oz', 'LICadj', 'eligible']], on='geoid')

# writing
    file_out = "clean{}.pkl".format(file_suffix)
    final.to_pickle("{}/{}".format(data, file_out))
    print('Cleaned -> {}'.format(file_out))