from census import Census

census_key = "be526a50bd1d95edbf21709b4e5c72a3c0436af0"

class census_fetcher():

    def __init__(self, key, year, dataset):
        self.key = key
        self.year = year
        self.c = Census(self.key, year=self.year)
        self.c.dataset = self._pick_dataset(dataset)

    def _pick_dataset(self, dataset):
        '''
        Params: dataset (str), options : acs5, acs1dp, sf1, sf3
        '''
        if dataset == 'acs5':
            #print(type(self.c.acs5))
            return self.c.acs5
        elif dataset == 'sf1':
            return self.c.sf1
        else:
            print(f"Failed. Try another dataset.")
            return None
        
    def search_tables(self, search_term):
        pass

    def get_tract_data(self, fields, geoid):
        '''
        Parameters: fields (str or list/tuple of strs), geoid (str) includes state fips, county fips, and tract.
            For example 01001020700 = 01 (state) + 001 (county) + 020700 (tract)

        Returns: tuple of results
        '''
        if len(geoid) != 11:
            ## if the geoid is ten chars and does not start with zero
            ## it probably lost the starting zero
            if not geoid.startswith('0') and len(geoid) == 10:
                geoid = '0' + geoid
            else:
                print("Invalid geoid. Must be 11 characters : 2 + 3 + 6 (state + county + tract).")
                return

        ## This way of indexing the geoid isn't ideal because of type conversions
        ## and loss of the first zero when converting from a string to an int
        state, county, tract = geoid[:2], geoid[2:5], geoid[5:]

        ## !!! Need to catch errors thrown by census.get()
        response = self.c.dataset.get(fields, {'for' : f'tract:{tract}', 'in' : f'state:{state} county:{county}'})
        if len(response) == 0:
            print(f"Empty response for geoid {geoid}.")
            return (-1 for f in fields)

        return (response[0][f] for f in fields)