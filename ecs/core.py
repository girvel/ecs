class Entity:
	"""Entity is a mixture of dict and object.

	You can access attributes as items.
	"""

	def __init__(self, **attributes):
		"""
		Args:
			**attributes: entity's future attributes in format
		"""
		for k, v in attributes.items():
			setattr(self, k, v)

	def __delitem__(self, key):
		"""Deletes an attribute with the given name."""
		return delattr(self, key)

	def __getitem__(self, item):
		"""Gets an attribute with the given name."""
		return getattr(self, item)

	def __setitem__(self, item, value):
		"""Sets an attribute with the given name."""
		return setattr(self, item, value)

	def __contains__(self, item):
		"""Checks if entity contains an attribute with the given name."""
		return hasattr(self, item)

	def __len__(self):
		"""Counts number of attributes inside the entity."""
		return len(list(self.__iter__()))

	def __repr__(self):
		return f'Entity(name={getattr(self, "name", None)})'

	def __iter__(self):
		"""Iterates entity as pairs: (attribute_name, attribute_value)"""

		for attr_name in dir(self):
			if not attr_name.startswith('__') or not attr_name.endswith('__'):
				yield attr_name, getattr(self, attr_name)


def add(system, entity):
	assert all(hasattr(system, a) for a in (
		'process', 'ecs_targets', 'ecs_requirements'
	))

	for member_name, requirements in system.ecs_requirements.items():
		if all(p in entity for p in requirements):
			system.ecs_targets[member_name].add(entity)

def remove(system, entity):
	for targets in system.ecs_targets.values():
		targets.discard(entity)

def update(system):
	keys = list(system.ecs_targets.keys())

	def _update(members):
		i = len(members)
		if i == len(keys):
			system.process(**members)
			return

		if len(system.ecs_targets[keys[i]]) > 0:
			for target in system.ecs_targets[keys[i]].copy():
				members[keys[i]] = target
				_update(members)

			del members[keys[i]]

	return _update({})

def register_attribute(metasystem, entity, attribute):
	add(metasystem, entity)
	for system in metasystem.ecs_targets["system"]:
		if any(attribute in r for r in system.ecs_requirements.values()):
			add(system, entity)

	return entity

def unregister_attribute(metasystem, entity, attribute=None):
	systems = [metasystem, *metasystem.ecs_targets["system"]]

	if attribute is None:
		entity.ecs_metasystem = None
	else:
		systems = [
			s for s in systems
			if any(
				attribute in r for r in s.ecs_requirements.values()
			)
		]

	for system in systems:
		remove(system, entity)

	return entity

def create_system(protosystem) -> Entity:
	"""Creates system from an annotated function

	Args:
		protosystem: function annotated in ECS style

	Returns:
		New entity with `process`, `ecs_targets` and `ecs_requirements` fields
	"""

	return Entity(
		process=protosystem,
		ecs_targets={
			member_name: set() for member_name in protosystem.__annotations__
		},
		ecs_requirements={
			member_name: set(annotation.split(', '))
			for member_name, annotation
			in protosystem.__annotations__.items()
		}
	)


class OwnedEntity(Entity):
	"""Represents an entity that belongs to some metasystem."""

	def __init__(self, metasystem, /, **attributes):
		self.ecs_metasystem = metasystem
		super().__init__(**attributes)

	def __setattr__(self, key, value):
		super().__setattr__(key, value)
		register_attribute(self.ecs_metasystem, self, key)

	def __delattr__(self, item):
		super().__delattr__(item)
		unregister_attribute(self.ecs_metasystem, self, item)


class Metasystem(Entity):
	"""Metasystem is a system that brute-forces systems and a facade to all
	interactions with the game.
	"""

	def __init__(self):
		self.ecs_targets = {'system': set(),}
		self.ecs_requirements = {
			'system': {'process', 'ecs_requirements', 'ecs_targets'}
		}
		self.name = 'metasystem'

	def process(self, system):
		update(system)

	def create(self, **attributes):
		"""Creates in-game entity.

		Args:
			**attributes: attributes (components) that entity will contain

		Returns:
			In-game entity
		"""

		return OwnedEntity(self, **attributes)

	def delete(self, entity):
		"""Removes entity from the game.

		Args:
			entity: in-game entity to be removed
		"""

		unregister_attribute(self, entity)

	def update(self):
		"""Updates all the systems once."""

		update(self)

	def create_system(self, protosystem):
		"""Creates system from an annotated function and adds it to the world.

		Args:
			protosystem: function annotated in ECS style

		Returns:
			New owned entity with `process`, `ecs_targets` and `ecs_requirements` fields
		"""

		return OwnedEntity(
			self,
			name=protosystem.__name__,
			process=protosystem,
			ecs_targets={
				member_name: set() for member_name in protosystem.__annotations__
			},
			ecs_requirements={
				member_name: set(annotation.split(', '))
				for member_name, annotation
				in protosystem.__annotations__.items()
			}
		)
