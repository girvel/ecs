from ecs import Metasystem, create_system
import time


# 1. You create a metasystem
ms = Metasystem()

dt = 0.04

# 2. You create systems and add them to metasystem
@ms.add
@create_system
def gravity(
    object: 'vy',
    constants: 'g',
):
    object.vy += constants.g * dt

@ms.add
@create_system
def inertion(object: 'x, y, vx, vy'):
    object.x += object.vx * dt
    object.y += object.vy * dt

@ms.add
@create_system
def output(object: 'name, x, y'):
    yield from range(int(1 / dt) - 1)  # skips 24 out of 25 frames
    print(f'{object.name}: {object.x:.2f}, {object.y:.2f}')

# 3. You create objects
ms.create(name='falling_guy1', x=0, y=0, vx=0, vy=0)
ms.create(name='falling_guy2', x=100, y=0, vx=0, vy=0)
ms.create(g=10)

# 4. Game loop
while True:
    ms.update()
    time.sleep(dt)