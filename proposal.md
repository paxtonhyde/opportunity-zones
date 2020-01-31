Paxton Hyde

January 31, 2020

Galvanize DSI Capstone II proposal

## Question
I want to look at the designation process for Opportunity Zones established under the Tax Cuts and Jobs Act of 2017. The Act establishes tax benefits and deferrals for investments in qualifying Opportunity Zones. A census tract that meets the definition low-income community or that are adjacent to low-income communities may be designated as Opportunity Zones. There have been rumors however, that the designation process was corrupted and that the program has become a boon for luxury projects with wealthy investors. (See New York Times:  "Trump Tax Break That Benefited the Rich Is Being Investigated", and "How a Trump Tax Break to Help Poor Communities Became a Windfall for the Rich".)

Even if only low-income and certain low-income-adjacent tracts can be designated as Opportunity Zones, the fact that there is evidence that the tax breaks are benefitting luxury projects is an indication that the designation process is probably too casual. I would guess that a good portion of the apparently mis-designated tracts are either sparsely populated or gentrifying. Although I don't know exactly what demographic statistics identify this type of tract, my assumption is that an unsupervised learning algorithm could tell the difference between an actual low-income community and these outlier tracts.

## Data
I have a spreadsheet of all Opportunity Zones designated as of 12/14/2018, which includes the State, Country, Census Tract #, type of designation (low-income or low-income adjacent), and data source. The majority of Zones were designated based on the American Community Survey (ACS) 5-year estimate for 2011-2015. The ACS is generally less precise than the decennial Census, and so most of the estimates have a wider range of error.

For capstone 2 I will combine this with Census tract-level data for the designated Opportunity Zones. The challenge will be pulling the sorts of features that will make the machine learning work. The definition of low-income community is based on poverty level (>=20%) and median household income. Other relevant information would be population or population density, change in population, rents and rent changes, demographic characteristics particularly race and age, and development.

## MVP
Cull Census Data for all the Opportunity Zones, look at some EDA, and 

**MVP+ :** Look at some maps of Opportunity Zones and adjacent Census tracts in Denver. I bet there are some designated Opportunity Zones that we wouldn't think should be getting tax breaks, for example the Five Points area.
