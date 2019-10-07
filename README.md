# MeleeMatchupData
Super Smash Bros Melee. Competitive Matchup History

This repository contains some Python code which is used to scrape matchup data from Liquidpedia. Some downloaded data is in the ``data`` folder. The format of the data is ``Sqlite3``.

Use the tool at your own risk. The Liquidpedia API warns that excessive scraping may result in your IP being blocked from their site.

## Getting started

### Data 

The data in data folder looks like this:

#### SSBM Rank

![](https://raw.githubusercontent.com/nathanesau/MeleeMatchupData/master/screenshots/ssbm_rank_demo.PNG)

#### Matchup Data (Set Counts Over Entire Career)

![](https://raw.githubusercontent.com/nathanesau/MeleeMatchupData/master/screenshots/matchup_table_demo.PNG)

Data was last updated on Oct 6, 2019.

### Python Code

* Function ``scrapeSSBMRankData()`` can be used to download SSBM Rank Lists (going back as far as 2013). These are top 50 or top 100 rankings for player performance over a certain time period.

* Function ``scrapeSetCount()`` returns the set count between two players.

* Some code is provided to loop through all player matchup combinations (for all players in a ranking list), get the set count between each combination of players and write all the data to the database.

Note: packages ``bs4`` and ``PyQt5`` are used and should be installed using ``pip``.
