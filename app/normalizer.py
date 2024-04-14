import csv
from collections import defaultdict

class FootballEventNormalizer:
    def __init__(self, input_file='input.csv', output_ext='jsonl'):
        self.input_file = input_file
        self.output_ext = output_ext
        self.matches = defaultdict(dict)
        self.teams = defaultdict(dict)
        self.players = defaultdict(dict)
        self.statistics = []
        self.match_player_stats = defaultdict(lambda: defaultdict(int))

    def read_csv_file(self):
        try:
            with open(self.input_file, 'r') as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.input_file} not found.") from e
        except csv.Error as e:
            raise csv.Error(f"Error reading CSV file {self.input_file}: {str(e)}") from e