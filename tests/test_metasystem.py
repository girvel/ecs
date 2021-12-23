import pytest
import ecs.core


def test_metasystem():
  processed_entities = []

  metasystem = ecs.core.Metasystem.clone()

  @ecs.Entity.make
  class System:
    ecs_targets = dict(
      entity=[]
    )

    def process(entity: "name"):
      processed_entities.append(entity.name)

  for e in [
    ecs.Entity(name="Hyde"),
    ecs.Entity(name="Jackie"),
    System,
  ]:
    metasystem.add(e)

  metasystem.update()
  
