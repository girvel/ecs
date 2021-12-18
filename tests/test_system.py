import pytest

import ecs.core


@pytest.fixture
def pairs_system():
  # TODO @ecs.make_entity
  class PairsSystem:
    ecs_targets = dict(
      first=[],
      second=[],
      container=[],
    )

    @staticmethod
    def process(
      first: 'name',
      second: 'name',
      container: 'pairs',
    ):
      container.pairs.append("{} & {}".format(first.name, second.name))

  return PairsSystem


def test_registering(pairs_system):
  entities = [
    ecs.Entity(name='entity1'),
    ecs.Entity(name='entity2', something='123'),
    ecs.Entity(name_='entity3'),
  ]

  for e in entities:
    ecs.core.register(pairs_system, e)

  assert set(pairs_system.ecs_targets['first'])  == set(entities[:2])
  assert set(pairs_system.ecs_targets['second']) == set(entities[:2])


def test_updating(pairs_system):
  people = [
    ecs.Entity(name='Eric'),
    ecs.Entity(name='Red'),
    ecs.Entity(name='Kitty'),
  ]

  container = ecs.Entity(pairs=[])

  pairs_system.ecs_targets['first'] += people
  pairs_system.ecs_targets['second'] += people
  pairs_system.ecs_targets['container'].append(container)

  ecs.core.update(pairs_system)

  assert set(container.pairs) == {
    'Eric & Eric',  'Eric & Red',  'Eric & Kitty',
    'Red & Eric',   'Red & Red',   'Red & Kitty',
    'Kitty & Eric', 'Kitty & Red', 'Kitty & Kitty',
  }



