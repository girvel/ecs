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
  e = [
    ecs.Entity(name='entity1'),
    ecs.Entity(name='entity2', something='123'),
    ecs.Entity(name_='entity3'),
  ]

  ecs.core.register(pairs_system, e[0])
  ecs.core.register(pairs_system, e[1])
  ecs.core.register(pairs_system, e[2])

  assert set(pairs_system.ecs_targets['first'])  == set(e[:2])
  assert set(pairs_system.ecs_targets['second']) == set(e[:2])



