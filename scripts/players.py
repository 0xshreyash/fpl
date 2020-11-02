import pandas as pd
import requests
from types import SimpleNamespace
from collections import namedtuple

BOOTSTRAP_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'


def main():
    content = requests.get(BOOTSTRAP_URL).json()
    player_list = content['elements']
    Player = namedtuple('Player', player_list[0].keys())
    players = []
    for player_details in player_list:
        player = Player._make(player_details.values())
        players.append(player)

    players.sort(key=lambda p: -p.total_points)
    players = pd.DataFrame.from_records(players, columns=players[0]._asdict().keys())
    players = players.set_index('id')
    players.to_csv('./data/players.csv')


if __name__ == '__main__':
    main()
