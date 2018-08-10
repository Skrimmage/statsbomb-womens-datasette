import json
import csv
import os
from pathlib import Path


def get_files(target_dir):
    item_list = os.listdir(target_dir)

    file_list = list()
    for item in item_list:
        item_dir = os.path.join(target_dir, item)
        if os.path.isdir(item_dir):
            file_list += get_files(item_dir)
        else:
            file_list.append(item_dir)
    return file_list


def get_events():
    events_files = get_files('./open-data/data/events')

    data = []

    for file in events_files:
        with open(file) as data_file:
            data.append([Path(file).stem, json.loads(data_file.read())])

    with open('./csv/events.csv', 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Headers
        writer.writerow([
            'match_id',
            'timestamp',
            'type_id',
            'type_name',
            'team_id',
            'team_name',
            'player_id',
            'player_name',
            'shot_xg',
            'shot_result_id',
            'shot_result'
        ])

        for match_id, match in data:
            for event in match:

                if event.get('shot') is None:
                    continue

                row = [
                    match_id,
                    event['timestamp'],
                    event['type']['id'],
                    event['type']['name'],
                    event['team']['id'],
                    event['team']['name'],
                    event['player']['id'],
                    event['player']['name'],
                    event['shot'].get('statsbomb_xg',0),
                    event['shot']['outcome']['id'],
                    event['shot']['outcome']['name']
                ]

                writer.writerow(row)


def get_matches():
    match_files = get_files('./open-data/data/matches')

    data = []

    for file in match_files:
        with open(file) as data_file:
            data.append(json.loads(data_file.read()))

    with open('./csv/matches.csv', 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Headers
        writer.writerow(['match_id', 'match_date', 'competition_id', 'competition_country_name', 'competition_name', 'home_team_id', 'home_team_name', 'away_team_id', 'away_team_name', 'home_score', 'away_score'])

        for comp in data:
            for match in comp:
                row = [
                    match['match_id'],
                    match['match_date'],
                    match['competition']['competition_id'],
                    match['competition']['country_name'],
                    match['competition']['competition_name'],
                    match['home_team']['home_team_id'],
                    match['home_team']['home_team_name'],
                    match['away_team']['away_team_id'],
                    match['away_team']['away_team_name'],
                    match['home_score'],
                    match['away_score']
                ]

                writer.writerow(row)


if __name__ == "__main__":
    Path('./csv').mkdir(parents=True, exist_ok=True)

    get_matches()
    get_events()
