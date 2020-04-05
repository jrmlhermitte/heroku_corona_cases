# Corona Virus Cases Server


Simple server for plotting out corona virus cases.
Using [bokeh](https://docs.bokeh.org/en/latest/index.html),
if you haven't heard of it, is a growing
library filling in the much needed stagnating plotting
alternatives in python.


## Routes
Just look at `corona_stats/routes.py` for the routes used.
As of this writing, there are two routes:
    - `corona/byState/NY`: Where NY may we any state code (case-sensitive)
    - `corona/allStates`
