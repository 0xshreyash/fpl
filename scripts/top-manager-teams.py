import requests
import pandas as pd

TOP_MANAGERS_FILE = './data/top-500-managers.csv'
PLAYERS_FILE = './data/players.csv'

CURR_GAMEWEEK = 6

PICKS_API = 'https://fantasy.premierleague.com/api/entry/{entry}/event/{game_week}/picks/'


def get_manager_team(manager, players):
    team_url = PICKS_API.format(entry=manager.entry, game_week=CURR_GAMEWEEK)
    picks = requests.get(team_url).json()['picks']
    picks = pd.DataFrame.from_records(picks, columns=picks[0].keys())
    picks = picks.set_index('element')
    team = picks.join(players)
    # print(len(team))
    return team


def most_selected(manager_teams):
    for entry, (manager, team) in manager_teams.items():
        print(manager, team)


def main():
    top_managers = pd.read_csv(TOP_MANAGERS_FILE)
    top_managers = top_managers.set_index('id')
    players = pd.read_csv(PLAYERS_FILE)
    players = players.set_index('id')
    manager_teams = {}
    teams = []
    count = 0
    for i, manager in top_managers.iterrows():
        team = get_manager_team(manager, players)
        manager_teams[manager.entry] = (manager, team)
        teams.append(team)
        if count % 10 == 0:
            print(count)
        count += 1

    teams = pd.concat(teams)
    teams.to_csv(f'./data/top-{int(len(teams) / 15)}-manager-teams.csv')


if __name__ == '__main__':
    main()

