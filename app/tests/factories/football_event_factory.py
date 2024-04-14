import factory
from faker import Faker


fake = Faker()

class EventFactory(factory.Factory):
    class Meta:
        model = dict

    match_id = factory.Sequence(lambda n: n)
    match_name = fake.name()
    team_id = factory.Sequence(lambda n: n)
    team_name = fake.name()
    is_home = fake.boolean()
    player_id = factory.Sequence(lambda n: n)
    player_name = fake.name()
    goals_scored = fake.random_number(digits=2)
    minutes_played = fake.random_number(digits=2)

class FootballEventNormalizeFactory(factory.Factory):

    input_file = 'test_input.csv'
    output_ext = 'jsonl'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        processor = model_class(*args, **kwargs)
        processor.run()
        return processor