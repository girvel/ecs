import pytest
import ecs


def test_entity():
  entity = ecs.Entity(
    name='custom-entity',
    some_parameter=42,
  )

  assert entity.name == 'custom-entity'
  assert entity.some_parameter == 42
