# Corona Virus Cases Server
This server currently just plots current corona virus testing results per state
in the US. Each plot presents the number of positive and negative tests per day
per state.


Simple server for plotting out corona virus cases.
Using [bokeh](https://docs.bokeh.org/en/latest/index.html),
if you haven't heard of it, is a growing
library filling in the much needed stagnating plotting
alternatives in python.

## The data
Data comes from the [COVID tracking project](https://covidtracking.com/).
The data is at most 10 minutes out of date with the data from the
COVID tracking project.


## Routes
Just look at `corona_stats/routes.py` for the routes used.
As of this writing, there are two routes:
    - `corona/byState/NY`: Where NY may we any state code (case-sensitive)
    - `corona/allStates`

## Heroku
This is currently live on heroku:
    - All states: http://jrm-corona-flask.herokuapp.com/corona/allStates
    - For New York: http://jrm-corona-flask.herokuapp.com/corona/byState/NY


# About
Just wanted to have my own custom statistics and learn about heroku, but I hope
this might be useful for others. I don't intend on mainting this, but may add
more plots I may find useful.
