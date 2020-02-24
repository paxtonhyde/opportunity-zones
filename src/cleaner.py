## fancyimpute requires TensorFlow
import pandas as pd
import numpy as np
from fancyimpute import KNN
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from directory import data

def remove_bad_tracts(messy_df, useless_columns_if_zero):
    # 1 : tracts where the API returned nothing
    a = (messy_df != -1)
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

    # 3 : replace negative values (entry errors) with nan
    step_three = step_two.where(step_two >= 0, errors='ignore')
    n_nan_lines = np.count_nonzero(step_three.isna().any(axis=1))

    print("{} lines ({}%) had at least one NaN.".format(n_nan_lines, round((n_nan_lines / len(step_three)), 2)*100 ))

    return step_three

if __name__ == "__main__":
# loading
    file_suffix = "_imputetest"
    raw = pd.read_pickle("{}/census_raw.pkl".format(data))
    geoids = raw.geoid

# cleaning
    columns_that_render_useless = [c for c in raw.columns if c.startswith("population")]
    clean = remove_bad_tracts(raw.drop(columns=["geoid"]), columns_that_render_useless)

# missing value imputation
# todo: standardize
    standard = StandardScaler()
    X = standard.fit_transform(clean.values)
    filled = KNNImputer(n_neighbors=3).fit_transform(X)
    imputed = pd.DataFrame(standard.inverse_transform(filled), columns=clean.columns)

# featurize

# # adding premade features
# # eligible/picked, LIC/contiguous, distress index, gentrify

# writing
    file_out = "clean{}.pkl".format(file_suffix)
    imputed.to_pickle("{}/{}".format(data, file_out))
    print('Cleaned -> {}'.format(file_out))