# Corona Virus Cases Server
This server currently just plots current corona virus testing results per state
in the US. Each plot presents the number of positive and negative tests per day
per state.

Simple server for plotting out corona virus cases.
Using [plotly](https://plotly.com/python/plotly-express).

## The data

### US data
Data comes from the [COVID tracking project](https://covidtracking.com/).
The data is at most 10 minutes out of date with the data from the
COVID tracking project. The data being downloaded is updated less frequently.

### Canada Data
Canada data comes from the government of 
Canada [website](https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html).
The data is at most 10 minutes out of date. The data being downloaded is updated less frequently.




## Routes
Visit the `/` route for more information.

## Heroku
This is currently live on heroku [here](http://jrm-corona-flask.herokuapp.com).


# Setup
## Commands

### Update requirements for the flask server
Requirements are managed using poetry. However, heroku uses the traditional requirements.txt file. When updating dependencies with poetry, this requirements file must be manually updated:
```bash
make update_requirements
```

### Update poetry lock file
```bash
poetry lock
```


### Install current package requirements from lock file
```bash
poetry install
```

### Run linting
```bash
poetry run flake8
poetry run pylint
poetry run typechecking
```


# About
Just wanted to have my own custom statistics and learn about heroku, but I hope
this might be useful for others. I don't intend on maintaining this.
