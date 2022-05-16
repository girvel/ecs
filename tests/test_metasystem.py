import pytest
import ecs.core


def test_metasystem():
  processed_entities = []

  metasystem = ecs.Metasystem()

  class system(ecs.Entity):
    ecs_targets = dict(
      entity=set()
    )

    ecs_requirements = dict(
      entity={'name'}
    )

    def process(self, entity):
      processed_entities.append(entity.name)

  system = system()

  for e in [
    system,
    ecs.Entity(name="Hyde"),
    ecs.Entity(name="Jackie"),
  ]:
    metasystem.create(**dict(e))

  metasystem.update()

  assert set(processed_entities) == {"Hyde", "Jackie"}

def test_dynamic_distribution():
  processed_entities = []  # TODO maybe a fixture for a system?

  ms = ecs.Metasystem()

  @ecs.create_system
  def test_system(entity: "name"):
    processed_entities.append(entity.name)

  ms.create(**dict(test_system))

  e = ms.create()

  e.name = 'Mike'
  ms.update()
  assert processed_entities == ['Mike']

  del e.name
  ms.update()
  assert processed_entities == ['Mike']
