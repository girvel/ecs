class Entity:
	def __init__(self, **parameters):
		for k, v in parameters.items():
			setattr(self, k, v)

	@classmethod
	def make(cls, object_):
		return cls(**{
			k: v for k, v in object_.__dict__.items()
			if k not in ('__dict__', '__weakref__')
		})
			
	def __getattr__(self, index):
		return None

	def __getitem__(self, item):
		return getattr(self, item)

	def __repr__(self):
		return str(self.__dict__)


def add(system, entity):
	assert hasattr(system, 'ecs_targets') and hasattr(system, 'process')

	for member_name, annotation in system.process.__annotations__.items():
		if all(entity[p] is not None for p in annotation.split(', ')):
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

	def update(self):
		update(self)
