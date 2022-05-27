import ecs.core as ecs
import pytest


class TestEntity:
    def test_is_anonymous_object(self):
        entity = ecs.Entity(
            name='custom-entity',
            some_parameter=42,
        )

        assert entity.name == 'custom-entity'
        assert entity.some_parameter == 42

    def test_attribute_is_item(self):
        entity = ecs.Entity()

        entity['first_field'] = 1
        entity.second_field = 2
        entity['Third field'] = 3

        assert entity.first_field == 1
        assert entity['second_field'] == 2
        assert entity['Third field'] == 3
        assert 'Third field' in entity

    def test_converts_to_dict(self):
        assert dict(ecs.Entity(a=1, b=2)) == {'a': 1, 'b': 2}

    def test_is_iterable(self):
        assert list(ecs.Entity(a=1, b=2)) == [('a', 1), ('b', 2)]


class TestCreateSystem:
    def test_creation(self):
        def protosystem(subject: "attribute1"):
            pass

        system = ecs.create_system(protosystem)

        assert system.process is protosystem
        assert system.ecs_targets is not None


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


class TestAdd:
    def test_adds_targets(self, pairs_system):
        entities = [
            ecs.Entity(name='entity1'),
            ecs.Entity(name='entity2', something='123'),
            ecs.Entity(name_='entity3'),
        ]

        for e in entities:
            ecs.add(pairs_system, e)

        assert set(pairs_system.ecs_targets['first'])  == set(entities[:2])
        assert set(pairs_system.ecs_targets['second']) == set(entities[:2])

    def test_is_repetition_safe(self, pairs_system):
        e = ecs.Entity(name='entity1')

        ecs.add(pairs_system, e)
        ecs.add(pairs_system, e)

        assert len(pairs_system.ecs_targets['first']) == 1
        assert len(pairs_system.ecs_targets['second']) == 1


class TestUpdate:
    def test_bruteforces_entities(self, pairs_system):
        npcs = [
            ecs.Entity(name='Eric'),
            ecs.Entity(name='Red'),
            ecs.Entity(name='Kitty'),
        ]

        container = ecs.Entity(pairs=[])

        pairs_system.ecs_targets['first'] |= set(npcs)
        pairs_system.ecs_targets['second'] |= set(npcs)
        pairs_system.ecs_targets['container'].add(container)

        ecs.update(pairs_system)

        assert set(container.pairs) == {
            'Eric & Eric',  'Eric & Red',  'Eric & Kitty',
            'Red & Eric',   'Red & Red',   'Red & Kitty',
            'Kitty & Eric', 'Kitty & Red', 'Kitty & Kitty',
        }


class TestMetasystem:
    def test_works(self):
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

    def test_dynamic_distribution(self):
        processed_entities = []    # TODO maybe a fixture for a system?

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

