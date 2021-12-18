class Entity:
	def __init__(self, **parameters):
		for k, v in parameters.items():
			setattr(self, k, v)
			
	def __getattr__(self, index):
		return None

	def __getitem__(self, item):
		return getattr(self, item)

	def __repr__(self):
		return str(self.__dict__)


def register(system, entity):
	assert hasattr(system, 'ecs_targets') and hasattr(system, 'process')

	for member_name, annotation in system.process.__annotations__.items():
		if all(entity[p] is not None for p in annotation.split(', ')):
			system.ecs_targets[member_name].append(entity)
