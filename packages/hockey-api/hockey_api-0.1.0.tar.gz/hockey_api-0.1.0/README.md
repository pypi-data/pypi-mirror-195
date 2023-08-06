# Hockey-API

## Purpose

The purpose of this package is to scrape data from ice hockey leagues, currently the NHL, 
from available APIs and websites. The information that is scraped is both play by play and
shift data, with support for all parts of the seasons (preseason, regular season, all star and playoffs)
for seasons starting from 2010-2011.

## Getting started
 
A short introduction to the prerequisites and installation.
 
### Prerequisites

This package is built on Python, particularly Python3. To use this package, the Python version should be 
at least 3.7.0.

### Installation

To install, simply open a terminal and run either of the following commands:

```python
pip install hockey_api
python -m pip install hockey_api
```

## Usage

To scrape data, three different functions are provided. Each function provides the same output structure, 
with a tuple containing play by play data for all the game(s) as well as the shifts.

- To scrape a list of games, where the input should be a list of game ids:
```python
from hockey_api import scrape_list_of_games

# Scrape the first three games of the 2021-2022 NHL season.
pbp, shifts = scrape_list_of_games(game_id_list=[2021020001, 2021020002, 2021020003])
```

- To scrape a list of games between two dates:
```python
from hockey_api import scrape_date_range

# Scrape the all the games during the month of October in 2021.
pbp, shifts = scrape_date_range(start_date="2021-10-01", end_date="2021-10-31")

# Scrape games from a given date.
pbp, shifts = scrape_date_range(start_date="2021-10-31")

```

- To scrape a specific part of a season:
```python
from hockey_api import scrape_season

# Scrape all games from the 2021-2022 NHL regular season.
pbp, shifts = scrape_season(season=2021, season_type="R")

# Scrape all games from the 2021-2022 NHL playoffs.
pbp_playoffs, shifts_playoffs = scrape_season(season=2021, season_type="P")
```

### Saving data


### Miscellaneous


## Contact


## Copyright
