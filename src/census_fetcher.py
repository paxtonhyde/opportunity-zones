from census import Census

census_key = "be526a50bd1d95edbf21709b4e5c72a3c0436af0"

class census_fetcher():

    def __init__(self, key, year, dataset):
        self.key = key
        self.year = year
        self.c = Census(self.key, year=self.year)
        self.datasetname = dataset
        self.c.dataset = self._pick_dataset(dataset)

    def _pick_dataset(self, dataset):
        '''
        Params: dataset (str), options : acs5, sf1
        '''
        if dataset == 'acs5':
            #print(type(self.c.acs5))
            return self.c.acs5
        elif dataset == 'sf1':
            return self.c.sf1
        else:
            print(f"Failed. Try another dataset.")
            return None

    def _clean_geoid(self, geoid):
        if len(geoid) != 11:
            # if the geoid is ten chars and does not start with zero,
            # it probably lost the starting zero
            if not geoid.startswith('0') and len(geoid) == 10:
                return '0' + geoid

            # if the geoid is two or one chars, it is probably a stateid
            elif len(geoid) in [1, 2]:
                if len(geoid) == 1:
                    return '0' + geoid
                return geoid

            else:
                print("Invalid geoid. Must be 11 characters : 2 + 3 + 6 (state + county + tract).")
                return False
        else:
            return geoid

    def get_state_tracts(self, fields, stateid):
        '''
        Parameters: fields (str or list/tuple of strs), stateid (str) including state fips.
            For example: 01

        Returns: ndarray, dimensions (number of tracts in state, fields)
        '''
        g = self._clean_geoid(stateid)

        if g:
            state = g[:2]

            # !!! Catch errors thrown by census.get()
            response = self.c.dataset.get(fields, {'for' : 'tract:*', 'in' : f'state:{state}'})
        else:
            return g

        ## Note: there may be some tracts with input errors that need to be cleaned later
        if len(response) == 0:
            print(f"Empty response for state {state}.")
            return [-1 for f in range(fields + 3)] # +3 for state, county, tract

        return [[row[j] for j in row] for row in response]
            

    def get_tract_data(self, fields, geoid):
        '''
        Parameters: fields (str or list/tuple of strs), geoid (str) includes state fips, county fips, and tract.
            For example 01001020700 = 01 (state) + 001 (county) + 020700 (tract)

        Returns: tuple of results, same length as fields
        '''
        g = self._clean_geoid(geoid)

        if g:
            state, county, tract = g[:2], g[2:5], g[5:]

            ## !!! Catch errors thrown by census.get()
            response = self.c.dataset.get(fields, {'for' : f'tract:{tract}', 'in' : f'state:{state} county:{county}'})
        else:
            return g

        ## Note: there may be some tracts with input errors that need to be cleaned later
        if len(response) == 0:
            print(f"Empty response for geoid {geoid}.")
            return (-1 for f in fields)

        return (response[0][f] for f in fields)