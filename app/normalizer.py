import csv
import json
from collections import defaultdict


class FootballEventNormalizer:
    def __init__(self, input='input.csv', output='output.jsonl'):
        self.input = input
        self.output = output
        self.matches = defaultdict(dict)
        self.teams = defaultdict(dict)
        self.players = defaultdict(dict)
        self.statistics = []
        self.match_player_stats = defaultdict(dict)

    def read_csv_file(self):
        try:
            with open(self.input, 'r') as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.input} not found.") from e
        except csv.Error as e:
            raise csv.Error(f"Error reading CSV file {self.input}: {str(e)}") from e
        
    def process_matches(self, event, is_home):
        try:
            match_id = event['Match Id']
            team_id = event['Team Id']
            match_data = self.matches[match_id]
            match_data['Match Id'] = match_id
            match_data['Match Name'] = event['Match Name']
            match_data['Home Team Id'] = team_id if is_home else None
            match_data['Away Team Id'] = team_id if not is_home else None
            match_data['Home Goals'] = match_data.get('Home Goals', 0)
            match_data['Away Goals'] = match_data.get('Away Goals', 0)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data in event: {event}.") from e

    def process_teams(self, event):
        try:
            team_id = event['Team Id']
            self.teams[team_id]['Team Id'] = team_id
            self.teams[team_id]['Team Name'] = event['Team Name']
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data in event: {event}.") from e

    def process_players(self, event):
        try:
            player_id = event['Player Id']
            team_id = event['Team Id']
            self.players[player_id]['Player Id'] = player_id
            self.players[player_id]['Team Id'] = team_id
            self.players[player_id]['Player Name'] = event['Player Name']
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data in event: {event}.") from e

    def process_statistics(self, event):
        try:
            match_id = event['Match Id']
            player_id = event['Player Id']
            goals_scored = event['Goals Scored']
            minutes_played = event['Minutes Played']
            match_goals = self.match_player_stats[match_id][player_id] + goals_scored
            self.match_player_stats[match_id][player_id] = match_goals
            fraction_minutes_played = minutes_played / 90
            fraction_goals_scored = goals_scored / match_goals if match_goals > 0 else 0
            self.statistics.append({
                'Stat Id': len(self.statistics) + 1,
                'Player Id': player_id,
                'Match Id': match_id,
                'Goals Scored': goals_scored,
                'Minutes Played': minutes_played,
                'Fraction of total minutes played': fraction_minutes_played,
                'Fraction of total goals scored': fraction_goals_scored
            })
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data in event: {event}.") from e

    def transform_data(self):
        try:
            input_data = self.read_csv_file()
            for event in input_data:
                is_home = event['Is Home'] == 'True'
                self.process_matches(event, is_home)
                self.process_teams(event)
                self.process_players(event)
                self.process_statistics(event)

                goals_scored = event['Goals Scored']
                match_id = event['Match Id']
                if is_home:
                    self.matches[match_id]['Home Goals'] += goals_scored
                else:
                    self.matches[match_id]['Away Goals'] += goals_scored
                    
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {str(e)}") from e   
        
    def save_to_json_lines(self, data, file_path):
        try:
            with open(file_path, 'w') as file:
                for item in data:
                    json.dump(item, file)
                    file.write('\n')
        except IOError as e:
            raise IOError(f"Error writing to file {file_path}: {str(e)}") from e

    def save_data(self):
        self.save_to_json_lines(list(self.matches.values()), f'match.{self.output}')
        self.save_to_json_lines(list(self.teams.values()), f'team.{self.output}')
        self.save_to_json_lines(list(self.players.values()), f'player.{self.output}')
        self.save_to_json_lines(self.statistics, f'statistic.{self.output}')    