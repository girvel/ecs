import pytest
from ecs.dynamic_entity import DynamicEntity
from ecs.essentials import add, update


@pytest.fixture
def pairs_system():
    class PairsSystem(DynamicEntity):
        ecs_targets = dict(
            first=[],
            second=[],
            container=[],
        )

        ecs_requirements = dict(
            first={'name'},
            second={'name'},
            container={'pairs'},
        )

        def process(self, first, second, container):
            container.pairs.append("{} & {}".format(first.name, second.name))

    return PairsSystem()


class TestAdd:
    def test_adds_targets(self, pairs_system):
        entities = [
            DynamicEntity(name='OwnedEntity1'),
            DynamicEntity(name='OwnedEntity2', something='123'),
            DynamicEntity(name_='OwnedEntity3'),
        ]

        for e in entities:
            add(pairs_system, e)

        assert set(pairs_system.ecs_targets['first'])  == set(entities[:2])
        assert set(pairs_system.ecs_targets['second']) == set(entities[:2])

    def test_is_repetition_safe(self, pairs_system):
        e = DynamicEntity(name='OwnedEntity1')

        add(pairs_system, e)
        add(pairs_system, e)

        assert len(pairs_system.ecs_targets['first']) == 1
        assert len(pairs_system.ecs_targets['second']) == 1


class TestUpdate:
    def test_bruteforces_entities(self, pairs_system):
        npcs = [
            DynamicEntity(name='Eric'),
            DynamicEntity(name='Red'),
            DynamicEntity(name='Kitty'),
        ]

        container = DynamicEntity(pairs=[])

        pairs_system.ecs_targets['first'] += npcs
        pairs_system.ecs_targets['second'] += npcs
        pairs_system.ecs_targets['container'] += [container]

        update(pairs_system)

        assert set(container.pairs) == {
            'Eric & Eric',  'Eric & Red',  'Eric & Kitty',
            'Red & Eric',   'Red & Red',   'Red & Kitty',
            'Kitty & Eric', 'Kitty & Red', 'Kitty & Kitty',
        }
