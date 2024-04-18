import unittest
from app.tests.factories.football_event_factory import EventFactory
from app.normalizer import FootballEventNormalizer
import os
import factory


class TestFootballEventNormalizer(unittest.TestCase):
    def setUp(self):
        self.normalizer = FootballEventNormalizer()

    def test_process_matches(self):
        event = factory.build(
            dict,
            FACTORY_CLASS=EventFactory,
            match_id=1,
            match_name="Match1",
            team_id=1,
            is_home="True",
        )
        self.normalizer.process_matches(event)
        expected_matches = {
            1: {
                "Match Id": 1,
                "Match Name": "Match1",
                "Home Team Id": 1,
                "Away Team Id": None,
                "Home Goals": 0,
                "Away Goals": 0,
            }
        }
        actual_matches = {k: dict(v) for k, v in self.normalizer.matches.items()}
        self.assertEqual(actual_matches, expected_matches)

    def test_process_players(self):
        event = EventFactory.build(player_id=1, team_id=1, player_name="Player1")
        self.normalizer.process_players(event)
        expected_players = {1: {"Player Id": 1, "Team Id": 1, "Player Name": "Player1"}}
        self.assertEqual(self.normalizer.players, expected_players)

    def test_process_statistics(self):
        event = factory.build(
            dict,
            FACTORY_CLASS=EventFactory,
            player_id=1,
            match_id=1,
            goals_scored=2,
            minutes_played=90,
            match_name="Match1",
            team_id=1,
        )
        self.normalizer.process_statistics(event)

        expected_statistic = {
            "Stat Id": 1,
            "Match Id": 1,
            "Player Id": 1,
            "Goals Scored": 2,
            "Minutes Played": 90,
            "Fraction of total minutes played": 1.0,
            "Fraction of total goals scored": 1.0,
        }

        self.assertEqual(self.normalizer.statistics[0], expected_statistic)

        event = factory.build(
            dict,
            FACTORY_CLASS=EventFactory,
            player_id=1,
            match_id=1,
            goals_scored=3,
            minutes_played=90,
            match_name="Match1",
            team_id=1,
        )
        self.normalizer.process_statistics(event)

        expected_statistic = {
            "Stat Id": 1,
            "Match Id": 1,
            "Player Id": 1,
            "Goals Scored": 5,
            "Minutes Played": 90,
            "Fraction of total minutes played": 1.0,
            "Fraction of total goals scored": 0.6,
        }

        self.assertEqual(self.normalizer.statistics[0], expected_statistic)

    def test_fraction_of_total_minutes_played(self):
        events = [
            EventFactory.build(player_id=1, goals_scored=1, minutes_played=45),
            EventFactory.build(player_id=2, goals_scored=0, minutes_played=60),
            EventFactory.build(player_id=3, goals_scored=2, minutes_played=90),
        ]

        for event in events:
            self.normalizer.process_statistics(event)

        expected_fractions = {1: 45 / 90, 2: 60 / 90, 3: 90 / 90}

        for player_id, expected_fraction in expected_fractions.items():
            actual_fraction = next(
                item["Fraction of total minutes played"]
                for item in self.normalizer.statistics
                if item["Player Id"] == player_id
            )
            self.assertEqual(actual_fraction, expected_fraction)

    def test_transform_data(self):
        self.normalizer.transform_data()

    def test_save_to_json_lines(self):
        data = [{"Test": "Data"}]
        file_path = "test.jsonl"
        self.normalizer.save_to_json_lines(data, file_path)
        self.assertTrue(os.path.isfile(file_path))
        os.remove(file_path)

    def test_save_data(self):
        self.normalizer.save_data()

    def test_run(self):
        self.normalizer.run()
