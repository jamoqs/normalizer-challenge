import csv
import json
from collections import defaultdict


class FootballEventNormalizer:
    def __init__(self, input="input.csv", output="output.jsonl"):
        self.input = input
        self.output = output
        self.matches = defaultdict(lambda: defaultdict(str))
        self.teams = defaultdict(dict)
        self.players = defaultdict(dict)
        self.statistics = []
        self.match_player_stats = defaultdict(lambda: defaultdict(int))

    def read_csv_file(self):
        try:
            with open(self.input, "r") as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.input} not found.") from e
        except csv.Error as e:
            raise csv.Error(f"Error reading CSV file {self.input}: {str(e)}") from e

    def process_matches(self, event):
        try:
            match_id = int(event["match_id"])
            team_id = int(event["team_id"])
            
            if match_id not in self.matches:
                self.matches[match_id]["Match Id"] = match_id
                self.matches[match_id]["Match Name"] = event["match_name"]
                self.matches[match_id]["Home Goals"] = 0
                self.matches[match_id]["Away Goals"] = 0

            match_data = self.matches[match_id]
            match_data["Home Team Id"] = team_id if event['is_home'] == 'True' else self.matches[match_id].get("Home Team Id", None)
            match_data["Away Team Id"] = team_id if event['is_home'] == 'False' else self.matches[match_id].get("Away Team Id", None)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data in event: {event}.") from e

    def process_teams(self, event):
        try:
            team_id = int(event["team_id"])
            self.teams[team_id]["Team Id"] = team_id
            self.teams[team_id]["Team Name"] = event["team_name"]
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data in event: {event}.") from e

    def process_players(self, event):
        try:
            player_id = int(event["player_id"])
            team_id = int(event["team_id"])
            self.players[player_id]["Player Id"] = player_id
            self.players[player_id]["Team Id"] = team_id
            self.players[player_id]["Player Name"] = event["player_name"]
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data in event: {event}.") from e

    def process_statistics(self, event):
        try:
            player_id = int(event["player_id"])
            goals_scored = int(event["goals_scored"])
            minutes_played = int(event["minutes_played"])

            # Update existing statistics or create new statistics
            if player_id in self.match_player_stats:
                self.match_player_stats[player_id] += goals_scored
            else:
                self.match_player_stats[player_id] = goals_scored

            fraction_minutes_played = minutes_played / 90
            fraction_goals_scored = self.match_player_stats[player_id] / goals_scored if goals_scored > 0 else 0

            # Create or update statistics
            statistic = {
                "Player Id": player_id,
                "Goals Scored": self.match_player_stats[player_id],
                "Minutes Played": minutes_played,
                "Fraction of total minutes played": fraction_minutes_played,
                "Fraction of total goals scored": fraction_goals_scored,
            }

            # Check if player already has a statistic
            existing_statistic = None
            for i in self.statistics:
                if i["Player Id"] == player_id:
                    existing_statistic = i
                    break

            if existing_statistic:
                # Update existing statistic
                existing_statistic.update(statistic)
            else:
                # Add new statistic
                stat_id = len(self.statistics) + 1
                statistic = {"Stat Id": stat_id, **statistic}
                self.statistics.append(statistic)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data in event: {event}.") from e


    def transform_data(self):
        try:
            input_data = self.read_csv_file()
            for event in input_data:
                self.process_matches(event)
                self.process_teams(event)
                self.process_players(event)
                self.process_statistics(event)

                goals_scored = int(event["goals_scored"])
                match_id = int(event["match_id"])
                if event['is_home'] == 'True':
                    self.matches[match_id]["Home Goals"] += goals_scored
                else:
                    self.matches[match_id]["Away Goals"] += goals_scored

        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {str(e)}") from e

    def save_to_json_lines(self, data, file_path):
        try:
            with open(file_path, "w") as file:
                for item in data:
                    json.dump(item, file)
                    file.write("\n")
        except IOError as e:
            raise IOError(f"Error writing to file {file_path}: {str(e)}") from e

    def save_data(self):
        self.save_to_json_lines(list(self.matches.values()), f"match.{self.output}")
        self.save_to_json_lines(list(self.teams.values()), f"team.{self.output}")
        self.save_to_json_lines(list(self.players.values()), f"player.{self.output}")
        self.save_to_json_lines(self.statistics, f"statistic.{self.output}")

    def run(self):
        self.transform_data()
        self.save_data()
