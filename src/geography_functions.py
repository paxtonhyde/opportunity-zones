from us import states

def fips_to_state(fips_as_string):
    return states.lookup(fips_as_string).name
