# opportunity-zones
<p align="center">
  <img src="images/header.png" width = 900 height = 150>
</p>
Paxton Hyde

Galvanize Data Science Immersive Capstone 2, February 2020

## Content
- [Context](#context)
- [Results](#results)
- [Takeaways](#takeaways)
- [Spark](#spark-efficiency)
- [References](#references)
## Background

The chief Executive of each state can nominate tracts as QOZs in their state. A tract will be eligible if it meets the requirements of a "low-income community" or if it is both: (a) adjacent to an LIC and (b) has a median household income of less than 1.25 times the income of the adjacent LIC. 

Up to one-quarter of the LIC census tracts in a state may be designated as QOZs, or up to 25 QOZs if the state has less than 100 LIC tracts. Up to five percent of tracts in a state may be designated as non-LIC or LIC-adjacent tracts (with fractional portions rounded up). A QOZ designation may be based on either 2011-2015 5-year ACS data or a more recent 5-year survey with appropriate justification.

(TODO: flow chart for how a tract can be designated)

The Tax Cuts and Jobs Act of 2017 included a new Opportunity Zone program, which provides capital gains tax deferrals and other benefits for investments in designated census tracts. The purpose of this program is to 
Any census tract that is 
 is eligible to that meets the definition low-income community or that are adjacent to low-income communities may be designated as Opportunity Zones. There have been rumors however, that the designation process was corrupted and that the program has become a boon for luxury projects with wealthy investors. (See New York Times:  "Trump Tax Break That Benefited the Rich Is Being Investigated", and "How a Trump Tax Break to Help Poor Communities Became a Windfall for the Rich".)

Even if only low-income and certain low-income-adjacent tracts can be designated as Opportunity Zones, the fact that there is evidence that the tax breaks are benefitting luxury projects is an indication that the designation process is probably too casual. I would guess that a good portion of the apparently mis-designated tracts are either sparsely populated or gentrifying. Although I don't know exactly what demographic statistics identify this type of tract, my assumption is that an unsupervised learning algorithm could tell the difference between an actual low-income community and these outlier tracts.


### Data
The data were collected through [the Moral Machine](http://moralmachine.mit.edu/), an online serious game created by MIT researchers. Users decide the morally preferable action for an autonomous vehicle from two scenarios presented by the game. Each game session is 13 choices long. At the end of the sessions, the user has the option to provide demographic information including their age, gender, annual income, country, and political and religious orientation on a sliding scale. 

An example of a choice on the Moral Machine.

![A choice](images/machine.png)

Moral Machine data are publicly [available](https://osf.io/3hvt2/?view_only=4bb49492edee4a8eb1758552a362a2cf). Nonetheless, the column names are fairly cryptic and understanding them required parsing the researchers' code in the project repository.
```
ScenarioOrder,Intervention,PedPed,Barrier,CrossingSignal,AttributeLevel,ScenarioTypeStrict,ScenarioType,
DefaultChoice,NonDefaultChoice,DefaultChoiceIsOmission,NumberOfCharacters,DiffNumberOFCharacters,Saved,Template,
DescriptionShown,LeftHand

13,0,0,0,0,Female,Gender,Gender,Male,Female,0,2,0,1,Desktop,0,0
```

Each row of the data represents either panel of each scenario. For the right panel in the image above:
```
Intervention = 0
PedPed = 1 // A choice between two groups of pedestrians
Barrier = 0
CrossingSignal = 1 // The character spared is crossing legally, 0 means there is no crossing signal
AttributeLevel = Hooman
ScenarioType = Species
DefaultChoice = Hoomans
NonDefaultChoice = Pets
DefaultChoiceIsOmission = 0 // Choosing the default choice does not require the car to change course
NumberOfCharacters = 1
DiffNumberOFCharacters = 0 // The number of characters killed is consistent no matter the choice
Saved = 1 // I choose the right panel
DescriptionShown = 0
LeftHand = 0
```

### Question

The authors of the Moral Machine paper found that there were some strong global preferences for saving humans over animals, more people over fewer, and the young over the old. They created three clusters of countries (West, East, and South) [each with a unique profile of preferences.](/images/MIT_cluster_profiles.png)

> I wanted to ask whether we can reasonably claim that moral preferences vary based on geography.

My goal was to group countries by metrics including cluster, type of political system, and percentile groups for different human development indexes (GII, GINI, CPI, etc.) and run significance tests for differences in each factor.

### Method

Unlike the [trolley problem](https://en.wikipedia.org/wiki/Trolley_problem), which is a choice between intervention and utility (saving the most lives), the Moral Machine has numerous dimensions. The authors of the paper used a conjoint analysis to calculate the effect of each factor in a user's choice. Replicating this analysis was beyond the scope of my project (read: "Their math is way over my head.").

I grouped the responses by country and calculated the mean preference for each country. Then I grouped the country means by my chosen metrics, calculate a weighted mean for each group, and compare the distributions of means between groups. My chosen significance level was 0.10.

I ran my calculations with Apache Spark on an Amazon Linux c4.8xlarge EC2 instance. The data generated from the pipeline was small enough (12 statistics x 130 countries) to be processed on my local machine using Pandas and NumPy.

## Results

After working through the calculations, I got as far as grouping by the country clusters identified in the Nature paper. Here I only present a hypothesis test for the difference in gender preferences by cluster.

Directly analyzing country-level means does not account for the relative number of responses from each country. I tried to avoid this shortcoming of my method by bootstrapping individual preferences for each country cluster. NumPy has a `.random.choice()` sampling method that makes it very easy to sample with weighted probabilities. The advantage of this method is that the country-level data was small and could be processed on a local machine.

After bootstrapping an independent *t*-test gave incredibly small *p*-values for almost all the preferences, which makes me somewhat skeptical of my methods. On the other hand, we would expect small *p*-values because the sample size of individual responses is quite large.

#### With bootstrapping
<p align="center">
  <img src="images/gender_histsbooted.png" width = 750 height = 800>
  <img src="images/gender_distributionsbooted.png" width = 600 height = 400>
</p>

*p*-values from an independent *t*-test with unequal variances for gender preferences between clusters show all significant differences for a significance level of 0.10.

|       |   West |   East |   South |
|-------|--------|--------|---------|
| West  |      - |      0 |       0 |
| East  |      0 |      - |       0 |
| South |      0 |      0 |       - |

(Note that these values are unrounded, maybe `scipy.stats.ttest_ind()` rounds very very small numbers to 0.)

#### Without bootstrapping
Note that this direct (non-bootstrapped) test of country-level means does not control for the relative number of responses from each country.

<p align="center">
  <img src="images/gender_hists.png" width = 750 height = 800>
  <img src="images/gender_distributions.png" width = 600 height = 400>
</p>

The *p*-values from an independent *t*-test with unequal variances for gender preferences between clusters still show some significant differences for a significance level of 0.10. The Eastern cluster seems significantly different from the other clusters, which is not exactly what we expect based on the professional results.<sup>[1](#footnote1)</sup>

|       |      West |      East |     South |
|-------|-----------|-----------|-----------|
| West  | -         | 0.0838754 | 0.281225  |
| East  | 0.0838754 | -        | 0.0147172 |
| South | 0.281225  | 0.0147172 | -         |

## Takeaways

1. Ambiguously-labelled data is a problem. I thought understood my dataset after reading the code used to generate the results in the Nature paper, but maybe not. I promise to document my own data carefully enough that another curious person would be able to interpret it.

2. Design the statistical test thoroughly before collecting data or writing the pipeline. I thought I had done this  well enough but my mind must still be more philosophical than statistical.

3. It is easy to end up with different file versions on AWS EC2 instance and your local machine. My solution was to write functions for reading and writing data that interact with an S3 bucket. `loaddata` looks first in the local directory before fetching from S3, and `uploaddata` writes both locally and to S3. This saves some `scp`'ing and makes it certain that the most up-to-date copy is on AWS.

4. Create an `~/.aws/credentials` file and put your EC2 instance credentials there before doing anything else on a new instance. Then you won't have to worry about it afterwards.

5. It is useful to know how to adjust the elastic block storage size on an EC2 instance by [adjusting the volume size](https://hackernoon.com/tutorial-how-to-extend-aws-ebs-volumes-with-no-downtime-ec7d9e82426e). 


## Spark Efficiency

While trying to make my computations faster, I reworked my pipeline function to reduce the number of Spark *actions* it called. The new function calls `.count()` twice rather than three times. Below are the results running on a `c4.8xlarge`.<sup>[2](#footnote2)</sup>
<p align="center">
  <img src="images/functions.png" width = 600 height = 600>
</p>

I also tested the speeds of several simple Spark functions for fun: `.filter()` and `.groupby()` are lazily-evaluated *transformations*, while `.count()` is an *action* and thus takes significantly longer to execute.

<p align="center">
  <img src="images/comparison2.png" width = 750 height = 800>
</p>

`.filter()` and `.groupby()` appear to be approximately constant time. `.count()` is slower, but almost appears constant up to a certain point when it increases.

Another interesting tidbit: the data graphed above actually omits the first datapoint on 10 samples. Below is the full data. I would guess that the first execution is longer either because the processor is switching tasks, or because Spark remembers something about the operation which makes subsequent executions of the same operation faster.
<p align="center">
  <img src="images/comparison.png" width = 750 height = 800>
</p>

[Back to top](#content)

## References
* [Internal Revenue Code (26 USC §§ 1400Z)](https://www.law.cornell.edu/uscode/text/26/subtitle-A/chapter-1/subchapter-Z)
* [Definition of "Low-Income Community" – (26 USC § 45D(e)(1))](https://www.law.cornell.edu/uscode/text/26/45D)
* [QOZ designation procedures (6 CFR 601.601: Rules and regulations)](https://www.irs.gov/pub/irs-drop/rp-18-16.pdf)
* [Opportunity Zones Resources (CDFI Fund)](https://www.cdfifund.gov/Pages/Opportunity-Zones.aspx)


#### Notes
<a name="footnote1">1</a>: "For example, countries belonging to the Southern cluster show a strong preference for sparing females compared to countries in other clusters."

<a name="footnote1">2</a>: By a back-of-the-napkin calculation, if the function execution time was reduced by 2 seconds, I saved myself (130 countries X 6 preferences X 2 seconds) = 1560 seconds or 26 minutes. Considering that the calculation took less than 10 minutes on the EC2, I can't be sure of this estimate.
