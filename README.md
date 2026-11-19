# Football-Stats-Analysis

A Python project that collects, processes, and explores player-level match statistics from **UEFA Euro 2020**.

> **Status:** Data was collected from [FBref](https://fbref.com) in 2021. The site's structure has since changed, so the scraping script (`ScrapingData.py`) may need updates. The processing and analysis scripts work on the saved CSV files and do not need the scraper to run.

## What it does

The project is a three-step pipeline, each step a separate script:

| Step | Script | Description |
|------|--------|-------------|
| 1. Collect | `ScrapingData.py` | Takes the FBref URL of a match and uses Selenium and BeautifulSoup to scrape the player stats tables of both teams (summary, passing, passing types, defending, possession, misc). Saves each table as a CSV and registers the match in `MatchList.csv`. |
| 2. Process | `MatchRecopilation.py` | Merges the six tables of each team into a single dataset per team and a combined dataset per match, removing duplicated columns. |
| 3. Explore | `StatsAnalysis.py` | Interactive command-line tool. Pick a match, choose a team (or both), and see the top players in 10 categories, or open the full profile of a single player. |

### Categories available in the analysis tool

Shooting (goals, shots, xG, npxG), passing, receiving, creativity (SCA, GCA, key passes, xA), dribbling, carries, tackling, pressing, aerial duels, and fouls and cards.

## Tech stack

Python, pandas, Selenium, BeautifulSoup (lxml), toolz

## Usage

```bash
pip install pandas selenium beautifulsoup4 lxml toolz

python ScrapingData.py        # 1. scrape a match (needs ChromeDriver)
python MatchRecopilation.py   # 2. build the per-team and per-match datasets
python StatsAnalysis.py       # 3. explore the stats from the command line
```

Data is stored under `Directory/UEFA-Euro-2020/`, with one folder per match inside `Matches/` and a `MatchList.csv` that tracks which matches have been processed.

## Known limitations

- The scraper was written in 2021 against the Selenium 3 API and pandas 1.x. It relies on hardcoded element positions on the FBref match page and on the structure of the match URL, so it will need updating.
- The ChromeDriver path is hardcoded for a Windows machine.

## Possible improvements

- Update the scraper to the current Selenium and pandas APIs and to FBref's current page structure.
- Replace hardcoded positions and URL slicing with more robust selectors.
- Add charts for team and player comparisons.
