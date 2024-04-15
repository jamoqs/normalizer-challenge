import unittest
from app.tests.factories.football_event_factory import EventFactory


class TestFootballEventNormalizer(unittest.TestCase):
    def setUp(self):
        self.normalizer = FootballEventNormalizer()

    def test_process_matches(self):
        event = EventFactory.build(
            match_id=1, match_name="Match1", team_id=1, is_home=True
        )
        self.normalizer.process_matches(event, True)
        self.assertEqual(
            self.normalizer.matches[1],
            {
                "Match Id": 1,
                "Match Name": "Match1",
                "Home Team Id": 1,
                "Away Team Id": None,
                "Home Goals": 0,
                "Away Goals": 0,
            },
        )

    def test_process_teams(self):
        event = EventFactory.build(team_id=1, team_name="Team1")
        self.normalizer.process_teams(event)
        self.assertEqual(self.normalizer.teams[1], {"Team Id": 1, "Team Name": "Team1"})

    def test_process_players(self):
        event = EventFactory.build(player_id=1, team_id=1, player_name="Player1")
        self.normalizer.process_players(event)
        self.assertEqual(
            self.normalizer.players[1],
            {"Player Id": 1, "Team Id": 1, "Player Name": "Player1"},
        )

    def test_process_statistics(self):
        event = EventFactory.build(
            match_id=1, player_id=1, goals_scored=2, minutes_played=90
        )
        self.normalizer.process_statistics(event)
        self.assertEqual(
            self.normalizer.statistics[0],
            {
                "Stat Id": 1,
                "Player Id": 1,
                "Match Id": 1,
                "Goals Scored": 2,
                "Minutes Played": 90,
                "Fraction of total minutes played": 1.0,
                "Fraction of total goals scored": 1.0,
            },
        )
        self.assertEqual(self.normalizer.match_player_stats[1][1], 2)


if __name__ == "__main__":
    unittest.main()
