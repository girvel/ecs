import pytest
import ecs.core


def test_metasystem():
  processed_entities = []

  metasystem = ecs.Metasystem()

  class system(ecs.Entity):
    ecs_targets = dict(
      entity=[]
    )

    def process(self, entity: "name"):
      processed_entities.append(entity.name)

  system = system()

  for e in [
    system,
    ecs.Entity(name="Hyde"),
    ecs.Entity(name="Jackie"),
  ]:
    metasystem.add(e)

  metasystem.update()

  assert set(processed_entities) == {
    "Hyde", "Jackie"
  }

def test_dynamic_distribution():
  processed_entities = []

  ms = ecs.Metasystem()

  @ms.add
  @ecs.create_system
  def process(entity: "name"):
    processed_entities.append(entity.name)

  e = ms.add(ecs.Entity())
  e.name = 'Mike'
  ms.update()

  assert set(processed_entities) == {'Mike'}
