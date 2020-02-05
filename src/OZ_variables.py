## format table : variables
query_dict = {'B01003':['001E'],
                'B12006':['001E', '002E'],
                'B07001':['001E', '017E', '033E'],
                'B01002':['001E'],
                'B02001':['002E', '003E'],
                'B17001':['002E'],
                'B19013':['001E'],
                'B25008':['001E', '003E'],
                'B25002':['001E', '003E'],
                'B25077':['001E'],
                'B25035':['001E'],
                'B25024':['001E', '002E', '003E', '010E']}
query_labels = {'population':['total'],
                'marriage':['total', 'never_married'],
                'mobility':['total', 'same_house_1yr', 'same_county_1yr'],
                'age':['median'],
                'race':['white', 'black'],
                'poverty':['poor'],
                'household_income':['median'],
                'tenure':['total', 'renters'],
                'occupancy':['total', 'vacant'],
                'home_value':['median'],
                'structure_year':['median'],
                'structure_units':['total', 'one_a', 'one_d', 'mobile']}

us_ = {'household_income_median':63179, 
        'age_median': 38.2,
        'p_poverty': 0.118,
        'p_black': 0.127,
        'p_white' : 0.730,
        'home_value_median':217600,
        'p_vacancy': 0.0315}

