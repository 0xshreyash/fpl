import pandas as pd
import requests

from multiprocessing import Pool
from urllib.parse import urljoin

FPL_URL = 'https://fantasy.premierleague.com/'
API = 'api/'
ENTRY = 'entry/'
HISTORY = 'history/'

SHARDS = 1024

CURR_WEEK = 6
NUM_PARTICIPANTS = 7338639


def get_entry_history(entry_id):
    entry_path = API + ENTRY + str(entry_id) + '/' + HISTORY
    return urljoin(FPL_URL, entry_path)


def entry_overview(entry_id):
    entry_url = get_entry_history(entry_id=entry_id)
    try:
        content = requests.get(entry_url).json()

        current_season_stats = content['current']
        week_stats = current_season_stats[CURR_WEEK - 1]

        overall_rank = week_stats['overall_rank']
        total_points = week_stats['total_points']

        return entry_id, overall_rank, total_points
    except:
        return entry_id, -1, -1


def main():
    entries_per_shard = NUM_PARTICIPANTS // SHARDS
    start = 200649
    for shard in range(29, SHARDS + 1):

        if shard == SHARDS:
            entries = NUM_PARTICIPANTS - entries_per_shard * (SHARDS - 1)
        else:
            entries = entries_per_shard

        with Pool(processes=512) as pool:
            res = pool.map(entry_overview, range(start, start + entries))
        start = start + entries

        overview_df = pd.DataFrame(
            res, columns=['Entry ID', 'Overall Rank', 'Total Points']
        )
        overview_df = overview_df.set_index('Entry ID')
        overview_df.to_csv(f'./data/rankings-{str(shard).zfill(len(str(SHARDS)))}.csv')


if __name__ == "__main__":
    main()
