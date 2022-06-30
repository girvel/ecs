import inspect

from lib.ecs.ecs.formatting import pretty


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
		"""Gets an attribute with the given name.

		Args:
			item: a name of the attribute or a tuple (name, default_value)

		Returns:
			Attribute value or default value if specified
		"""
		if isinstance(item, tuple):
			return getattr(self, *item)

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
		name = self["name", None]

		return 'Entity{}({})'.format(
			name and f" '{name}'" or "",
			', '.join(
				f'{key}={pretty(value)}'
				for key, value in self
				if key != 'name'
			)
		)

	def __iter__(self):
		"""Iterates entity as pairs: (attribute_name, attribute_value)"""

		for attr_name in dir(self):
			if not attr_name.startswith('__') or not attr_name.endswith('__'):
				yield attr_name, getattr(self, attr_name)


class OwnedEntity(Entity):
	"""Represents an entity that belongs to some metasystem."""

	def __setattr__(self, key, value):
		super().__setattr__(key, value)

		if '__metasystem__' in self:
			register_attribute(self.__metasystem__, self, key)

	def __delattr__(self, item):
		super().__delattr__(item)
		if '__metasystem__' in self:
			unregister_attribute(self.__metasystem__, self, item)


def add(system, entity):
	assert all(hasattr(system, a) for a in (
		'process', 'ecs_targets', 'ecs_requirements'
	))

	for member_name, requirements in system.ecs_requirements.items():
		if all(p in entity for p in requirements):
			targets = system.ecs_targets[member_name]
			if entity not in targets:
				targets.append(entity)

def remove(system, entity):
	for targets in system.ecs_targets.values():
		if entity in targets:
			targets.remove(entity)

def update(system):
	keys = list(system.ecs_targets.keys())

	def _update(members):
		i = len(members)
		if i == len(keys):
			if inspect.isgeneratorfunction(system.process):
				tuple_members = tuple(members.values())
				if tuple_members not in system.ecs_generators:
					system.ecs_generators[tuple_members] \
						= system.process(**members)

				try:
					next(system.ecs_generators[tuple_members])
				except StopIteration:
					del system.ecs_generators[tuple_members]
			else:
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
		entity.__metasystem__ = None
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

def create_system(protosystem) -> OwnedEntity:
	"""Creates system from an annotated function

	Args:
		protosystem: function annotated in ECS style

	Returns:
		New entity with `process`, `ecs_targets` and `ecs_requirements` fields
	"""

	result = OwnedEntity(
		name=protosystem.__name__,
		process=protosystem,
		ecs_targets={
			member_name: [] for member_name in protosystem.__annotations__
		},
		ecs_requirements={
			member_name: set(annotation.split(', '))
			for member_name, annotation
			in protosystem.__annotations__.items()
		}
	)

	if inspect.isgeneratorfunction(protosystem):
		result.ecs_generators = {}

	return result


class OwnershipException(Exception):
	pass


class Metasystem(Entity):
	"""Metasystem is a system that brute-forces systems and a facade to all
	interactions with the game.
	"""

	def __init__(self):
		self.ecs_targets = {'system': [],}
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

		return self.add(OwnedEntity(**attributes))

	def add(self, entity):
		"""Adds an entity to the metasystem; adds __metasystem__ attribute."""

		if '__metasystem__' in entity:
			raise OwnershipException(
				"Entity {entity} is already belongs to a metasystem"
			)

		entity.__metasystem__ = self

		for attribute, _ in entity:
			register_attribute(self, entity, attribute)

		return entity

	def delete(self, entity):
		"""Removes entity from the game.

		Args:
			entity: in-game entity to be removed
		"""

		unregister_attribute(self, entity)

	def update(self):
		"""Updates all the systems once."""

		update(self)
