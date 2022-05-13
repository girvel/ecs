class Entity:
	"""Entity represents any object inside the game"""

	def __init__(self, **attributes):
		"""
		Args:
			**attributes: entity's future attributes in format
		"""
		for k, v in attributes.items():
			setattr(self, k, v)

	def __delitem__(self, key):
		return delattr(self, key)

	def __getitem__(self, item):
		return getattr(self, item)

	def __setitem__(self, item, value):
		return setattr(self, item, value)

	def __contains__(self, item):
		return hasattr(self, item)

	def __repr__(self):
		return f'Entity(name={self.name})'

	def __iter__(self):
		for attr_name in dir(self):
			if not attr_name.startswith('__') or not attr_name.endswith('__'):
				yield attr_name, getattr(self, attr_name)


def add(system, entity):
	assert hasattr(system, 'ecs_targets') and hasattr(system, 'process')

	for member_name, annotation in system.process.__annotations__.items():
		if all(p in entity for p in annotation.split(', ')):
			system.ecs_targets[member_name].append(entity)


def update(system):
	keys = list(system.ecs_targets.keys())

	def _update(members):
		i = len(members)
		if i == len(keys):
			system.process(**members)
			return

		if len(system.ecs_targets[keys[i]]) > 0:
			for target in system.ecs_targets[keys[i]]:
				members[keys[i]] = target
				_update(members)

			del members[keys[i]]

	return _update({})


def create_system(protosystem) -> Entity:
	"""Creates system from an annotated function

	Args:
		protosystem: function annotated in ECS style

	Returns:
		New entity with `process` and `ecs_targets` fields
	"""

	return Entity(
		process=protosystem,
		ecs_targets={
			member_name: [] for member_name in protosystem.__annotations__
		},
	)


class Metasystem(Entity):
	ecs_targets = dict(
		system=[]
	)

	def process(self, system: "process"):
		update(system)

	def add(self, entity):
		for system in self.ecs_targets["system"]:
			add(system, entity)
		add(self, entity)
		return entity

	def update(self):
		update(self)
