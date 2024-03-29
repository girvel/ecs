from ecs.entity import Entity
from ecs.essentials import add, update, remove


class PairsSystem(Entity):
    def __init__(self):
        self.ecs_targets = dict(
            first=[],
            second=[],
            container=[],
        )

        self.ecs_requirements = dict(
            first={'name'},
            second={'name'},
            container={'pairs'},
        )

        self.ecs_generators = {}

    @staticmethod
    def ecs_process(first, second, container):
        container.pairs.append("{} & {}".format(first.name, second.name))


class NamedEntity:
    def __init__(self, name):
        self.name = name
        self.__metasystem__ = None


class SecretlyNamedEntity:
    def __init__(self, name_):
        self.name_ = name_
        self.__metasystem__ = None


class ContainerEntity:
    def __init__(self):
        self.pairs = []
        self.__metasystem__ = None


class TestAdd:
    def test_adds_targets(self):
        pairs_system = PairsSystem()

        entities = [
            NamedEntity('OwnedEntity1'),
            NamedEntity('OwnedEntity2'),
            SecretlyNamedEntity('OwnedEntity3'),
        ]

        for e in entities:
            add(pairs_system, e)

        assert set(pairs_system.ecs_targets['first']) == set(entities[:2])
        assert set(pairs_system.ecs_targets['second']) == set(entities[:2])

    def test_is_repetition_safe(self):
        pairs_system = PairsSystem()

        e = NamedEntity('OwnedEntity1')

        add(pairs_system, e)
        add(pairs_system, e)

        assert len(pairs_system.ecs_targets['first']) == 1
        assert len(pairs_system.ecs_targets['second']) == 1


class TestRemove:
    def test_removes_targets(self):
        pairs_system = PairsSystem()
        pairs_system.ecs_targets['first'].append(e := NamedEntity("OwnedEntity1"))

        remove(pairs_system, e)
        assert len(pairs_system.ecs_targets['first']) == 0

        remove(pairs_system, e)
        assert len(pairs_system.ecs_targets['first']) == 0


class TestUpdate:
    def test_bruteforces_entities(self):
        pairs_system = PairsSystem()

        npcs = [
            NamedEntity('Eric'),
            NamedEntity('Red'),
            NamedEntity('Kitty'),
        ]

        container = ContainerEntity()

        pairs_system.ecs_targets['first'].extend(npcs)
        pairs_system.ecs_targets['second'].extend(npcs)
        pairs_system.ecs_targets['container'].append(container)

        update(pairs_system)

        assert set(container.pairs) == {
            'Eric & Eric',  'Eric & Red',  'Eric & Kitty',
            'Red & Eric',   'Red & Red',   'Red & Kitty',
            'Kitty & Eric', 'Kitty & Red', 'Kitty & Kitty',
        }
