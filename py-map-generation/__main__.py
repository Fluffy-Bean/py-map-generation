import random
from PIL import Image


class GenerateMap:
    def __init__(self, dimension: tuple, c_level: int = 0, seed: int = 69, choice: list = (-100, 200)):
        self.dimension = dimension
        self.c_level = c_level
        self.choice = choice
        self.nodes = []
        self.seed = seed

        random.seed(seed)

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

                if n.position[0] == n2.position[0]:
                    if n2.position[1] == n.position[1] + 1:
                        n.neighbors.append(n2)
                elif n.position[1] == n2.position[1]:
                    if n2.position[0] == n.position[0] + 1:
                        n.neighbors.append(n2)

                if len(n.neighbors) >= 2:
                    break

    def _fill_nodes(self):
        for n in self.nodes:
            if 40 < n.position[0] < 160 and 20 < n.position[1] < 80:
                if random.randint(0, 1000) <= self.seed:
                    n.elevation = random.choice(self.choice)
                    n.temperature = random.choice(self.choice)

    def smooth_map(self):
        for n1 in self.nodes:
            n1.active = False
            for n2 in n1.neighbors:
                if n2.active == True:
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

    def lower_land(self):
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
        self.active = True

    def set_active(self):
        self.active = True


if __name__ == '__main__':
    world = GenerateMap((200, 100))

    def process1():
        [n.set_active() for n in world.nodes]
        world.smooth_map()

    def process2():
        [n.set_active() for n in world.nodes]
        world.lower_land()

    def process3():
        [n.set_active() for n in world.nodes]
        world.raise_land()

    def process4():
        [n.set_active() for n in world.nodes]
        world.raise_temperature()


    print('0')
    for i in range(100):
        process1()
        process4()
    print('1')
    for i in range(15):
        process2()
        process3()
    print('2')
    for i in range(100):
        process1()

    img = Image.new('RGB', (200, 100), color='blue')

    for n in world.nodes:
        if n.elevation <= (-25):
            img.putpixel(n.position, (0, 0, 0))
        elif n.elevation <= world.c_level:
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
