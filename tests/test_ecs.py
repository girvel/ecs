import pytest
import ecs


@pytest.fixture
def pairs_system():
  class PairsSystem:
    class Members:
      first = ["name"]
      second = ["name"]
      list_container = ["pairs"]
    
    @staticmethod
    def process(first, second, list_container):
        


def test_entity_creation():
  entity = ecs.Entity(
    name='custom-entity',
    some_parameter=42,
  )

  assert entity.name == 'custom-entity'
  assert entity.some_parameter == 42
  

def test_entity_undefined_parameters_are_none():
  entity = ecs.Entity()
  
  assert entity.undefined_parameter == None
