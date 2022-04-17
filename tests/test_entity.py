import ecs


def test_creates_anonymous_object():
  entity = ecs.Entity(
    name='custom-entity',
    some_parameter=42,
  )

  assert entity.name == 'custom-entity'
  assert entity.some_parameter == 42


def test_undefined_parameters_are_none():
  entity = ecs.Entity()

  assert entity.undefined_parameter is None


def test_is_lua_style_object():
  entity = ecs.Entity()

  entity['first_field'] = 1
  entity.second_field = 2
  entity['Third field'] = 3

  assert entity.first_field == 1
  assert entity['second_field'] == 2
  assert entity['Third field'] == 3
  assert 'Third field' in entity


def test_is_easily_convertible_to_a_dict():
  assert dict(ecs.Entity(a=1, b=2)) == {'a': 1, 'b': 2}


def test_is_iterable():
  assert list(ecs.Entity(a=1, b=2)) == [('a', 1), ('b', 2)]
