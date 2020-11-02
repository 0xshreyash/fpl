import pandas as pd
import requests
from collections import namedtuple

OVERALL_LEAGUE = 314
LEAGUE_API = 'https://fantasy.premierleague.com/api/leagues-classic/'
STANDINGS = '/standings/?page_standings='
NUM_MANAGERS = 500  # 10000


def parse_standings_page(standings_page):
    Entry = namedtuple('Entry', standings_page['results'][0].keys())
    entries = []
    for entry_dict in standings_page['results']:
        entry = Entry._make(entry_dict.values())
        entries.append(entry)
    return entries


def main():
    url = LEAGUE_API + str(OVERALL_LEAGUE) + STANDINGS
    page = 1
    overall_league_standings = requests.get(
        LEAGUE_API + str(OVERALL_LEAGUE) + STANDINGS + str(page)
    ).json()['standings']
    standings = []
    while overall_league_standings['has_next'] and len(standings) < NUM_MANAGERS:
        standings.extend(parse_standings_page(overall_league_standings))
        page += 1
        overall_league_standings = requests.get(
            LEAGUE_API + str(OVERALL_LEAGUE) + STANDINGS + str(page)
        ).json()['standings']
        if len(standings) % 100 == 0:
            print(len(standings))
    standings.extend(parse_standings_page(overall_league_standings))

    standings = standings[:NUM_MANAGERS]
    standings = pd.DataFrame.from_records(standings, columns=standings[0]._asdict().keys())
    standings = standings.set_index('id')
    print(standings.head())
    standings.to_csv(f'./data/top-{NUM_MANAGERS}-managers.csv')


if __name__ == "__main__":
    main()
