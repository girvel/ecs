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
    metasystem.add(e)

  metasystem.update()

  assert set(processed_entities) == {"Hyde", "Jackie"}

def test_dynamic_distribution():
  processed_entities = []  # maybe a fixture for a system?

  ms = ecs.Metasystem()

  @ms.add
  @ecs.create_system
  def process(entity: "name"):
    processed_entities.append(entity.name)

  e = ms.add(ecs.Entity())

  e.name = 'Mike'
  ms.update()
  assert processed_entities == ['Mike']

  del e.name
  ms.update()
  assert processed_entities == ['Mike']
