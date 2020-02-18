## format table : variables
query_dict = {'B01003':['001E'],
                'B01002':['001E'],
                'B02001':['002E', '003E'],
                'B17001':['002E'],
                'B19013':['001E'],
                'B25077':['001E'],
                'B25008':['001E', '002E'],
                'B25002':['001E', '003E'],
                'B25035':['001E'],
                'B25024':['001E', '002E', '003E', '010E'],
                'B15003': ['001E', '022E', '023E', '024E', '025E'],
                'B14001': ['001E', '008E', '009E']}
query_labels = {'population':['total'],
                'age':['median'],
                'race':['white', 'black'],
                'poverty':['poor'],
                'household_income':['median'],
                'home_value':['median'],
                'tenure':['total', 'owner'],
                'occupancy':['total', 'vacant'],
                'structure_year':['median'],
                'structure_units':['total', 'one_a', 'one_d', 'mobile'],
                'education':['universe', 'bachelor', 'master', 'prof', 'doc'],
                'enrollment':['universe', 'undergrad', 'grad']}

us_averages = {'household_income_median': 63179, 
        'age_median': 38.2,
        'p_poverty': 0.118,
        'p_black': 0.127,
        'p_white' : 0.730,
        'home_value_median': 217600,
        'p_vacancy': 0.0315}

