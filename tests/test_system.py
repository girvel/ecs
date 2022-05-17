import pytest

import ecs.core


@pytest.fixture
def pairs_system():
  class PairsSystem(ecs.Entity):
    ecs_targets = dict(
      first=set(),
      second=set(),
      container=set(),
    )

    ecs_requirements = dict(
      first={'name'},
      second={'name'},
      container={'pairs'},
    )

    def process(self, first, second, container):
      container.pairs.append("{} & {}".format(first.name, second.name))

  return PairsSystem()


def test_add_forms_ecs_targets(pairs_system):
  entities = [
    ecs.Entity(name='entity1'),
    ecs.Entity(name='entity2', something='123'),
    ecs.Entity(name_='entity3'),
  ]

  for e in entities:
    ecs.core.add(pairs_system, e)

  assert set(pairs_system.ecs_targets['first'])  == set(entities[:2])
  assert set(pairs_system.ecs_targets['second']) == set(entities[:2])


def test_update_bruteforces_entities(pairs_system):
  npcs = [
    ecs.Entity(name='Eric'),
    ecs.Entity(name='Red'),
    ecs.Entity(name='Kitty'),
  ]

  container = ecs.Entity(pairs=[])

  pairs_system.ecs_targets['first'] |= set(npcs)
  pairs_system.ecs_targets['second'] |= set(npcs)
  pairs_system.ecs_targets['container'].add(container)

  ecs.core.update(pairs_system)

  assert set(container.pairs) == {
    'Eric & Eric',  'Eric & Red',  'Eric & Kitty',
    'Red & Eric',   'Red & Red',   'Red & Kitty',
    'Kitty & Eric', 'Kitty & Red', 'Kitty & Kitty',
  }



