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
                'poverty':[''],
                'household_income':['median'],
                'home_value':['median'],
                'tenure':['total', 'owner'],
                'occupancy':['total', 'vacant'],
                'structure_year':['median'],
                'housing_units':['total', 'one_a', 'one_d', 'mobile'],
                'education':['universe', 'bachelor', 'master', 'prof', 'doc'],
                'enrollment':['universe', 'undergrad', 'grad']}

universe_to_column_mapping = {"population_total":["race_white", "race_black", "poverty_"],\
           "tenure_total":["tenure_owner"],\
            "occupancy_total":["occupancy_vacant"],\
            "housing_units_total":["housing_units_mobile", {"single_unit_housing": ["housing_units_one_a", "housing_units_one_d"]}],\
              "education_universe":[{"bachelorsplus": ["education_bachelor", "education_master", "education_prof", "education_doc"]}],\
              "enrollment_universe":[{"enrolled":["enrollment_undergrad", "enrollment_grad"]}]}

delta_features = ['population_total', 'household_income_median', 'home_value_median', 'housing_units_total']

us_averages = {'household_income_median': 63179, 
        'age_median': 38.2,
        'p_poverty': 0.118,
        'p_black': 0.127,
        'p_white' : 0.730,
        'home_value_median': 217600,
        'p_vacancy': 0.0315}

