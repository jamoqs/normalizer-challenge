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
        self.match_player_stats = defaultdict(lambda: defaultdict(int))

    def read_csv_file(self):
        try:
            with open(self.input, 'r') as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.input} not found.") from e
        except csv.Error as e:
            raise csv.Error(f"Error reading CSV file {self.input}: {str(e)}") from e
        
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