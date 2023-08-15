import random
import numpy
from PIL import Image


class GenerateMap:
    def __init__(self, dimension: tuple, seed: int = 621, **kwargs):
        random.seed(seed)

        self.choice = (-100, 200)
        self.sea_level = 0
        self.density = 50
        self.nodes = []

        self.dimension = dimension
        self.seed = seed

        if kwargs:
            [setattr(self, item, kwargs[item]) for item in kwargs]

        self._generate_nodes()
        self._get_neighbors()
        self._fill_nodes()

    def _generate_nodes(self):
        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                self.nodes.append(Node((i, j)))

    def _get_neighbors(self):
        _ = [n for n in self.nodes]

        for n in self.nodes:
            _.pop(0)

            for n2 in _:
                if n == n2:
                    continue

                if n.position[0] == n2.position[0] and n2.position[1] == n.position[1] + 1:
                    n.neighbors.append(n2)
                elif n.position[1] == n2.position[1] and n2.position[0] == n.position[0] + 1:
                    n.neighbors.append(n2)

                if len(n.neighbors) >= 2:
                    break

    def _fill_nodes(self):
        for n in self.nodes:
            if 40 < n.position[0] < 160 and 20 < n.position[1] < 80:
                if random.randint(0, 1000) <= self.density:
                    n.elevation = random.choice(self.choice)
                    n.temperature = random.choice(self.choice)

    def smooth_map(self):
        for n1 in self.nodes:
            for n2 in n1.neighbors:
                if n1.elevation != n2.elevation:
                    if random.randrange(0, 100) < 5:
                        a = (n1.elevation + n2.elevation) / 2
                        n1.elevation = a
                        n2.elevation = a
                    elif random.randrange(0, 100) < 5:
                        a = (n1.temperature + n2.temperature) / 2
                        n1.temperature = a
                        n2.temperature = a

    def raise_land(self):
        for n in self.nodes:
            if n.elevation > 0:
                if random.randrange(0, 100) < 1:
                    n.elevation += 100

    def lower_sea(self):
        for n in self.nodes:
            if n.elevation <= 0:
                if random.randrange(0, 100) < 1:
                    n.elevation -= 100

    def raise_temperature(self):
        for n in self.nodes:
            if n.elevation > 0:
                if random.randrange(0, 100) < 1:
                    n.temperature += 10


class Node:
    def __init__(self, position: tuple):
        self.position = position
        self.elevation = 0
        self.temperature = 0
        self.neighbors = []


if __name__ == '__main__':
    world = GenerateMap((200, 100))

    print('0')
    for i in range(100):
        world.smooth_map()
        world.raise_temperature()
    print('1')
    for i in range(15):
        world.lower_sea()
        world.raise_land()
    print('2')
    for i in range(150):
        world.smooth_map()

    img = Image.new('RGB', (200, 100), color='blue')

    for n in world.nodes:
        if n.elevation <= (-25):
            img.putpixel(n.position, (0, 0, 0))
        elif n.elevation <= world.sea_level:
            img.putpixel(n.position, (0, 0, 255))
        elif n.elevation <= 25 and n.temperature <= 0:
            img.putpixel(n.position, (0, 255, 255))
        elif n.elevation <= 25 and n.temperature <= 5:
            img.putpixel(n.position, (0, 255, 0))
        elif n.elevation <= 25 and n.temperature <= 10:
            img.putpixel(n.position, (255, 255, 0))
        elif n.elevation <= 25 and n.temperature <= 100:
            img.putpixel(n.position, (255, 0, 0))
        else:
            img.putpixel(n.position, (255, 255, 255))

    img.save('map.png')
