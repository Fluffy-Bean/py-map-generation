# -*- coding: utf-8 -*-

"""
Python Map Generation
=====================
Simple python world generation
"""

import random
import numpy


class GenerateMap:
    """Generate a map main class"""

    def __init__(self, dimension: tuple, seed: int = 621) -> None:
        """
        :param dimension: x, y tuple for the size of the map
        :param seed: seed for random, must be int
        """
        random.seed(seed)

        self.border = 15
        self.sea_level = 0
        self.density = 70
        self.choice = (-100, 200)
        self.nodes = numpy.array([])

        self.dimension = dimension
        self.seed = seed

        self._generate_nodes()
        self._fill_nodes()

    def _generate_nodes(self) -> None:
        """
        Generates default nodes/chunks
        :return: None
        """
        for x in range(self.dimension[0]):
            for y in range(self.dimension[1]):
                self.nodes = numpy.append(
                    self.nodes, {"elevation": 0, "temperature": 0}
                )

        self.nodes = numpy.reshape(self.nodes, self.dimension)

    def _fill_nodes(self) -> None:
        """
        Fills nodes with random data
        :return: None
        """
        for node in numpy.ndenumerate(self.nodes):
            if (
                self.border < node[0][0] < (self.dimension[0] - self.border)
                and self.border < node[0][1] < (self.dimension[1] - self.border)
                and random.randint(0, 1000) <= self.density
            ):
                node[1]["elevation"] = random.choice(self.choice)
                node[1]["temperature"] = random.choice(self.choice)

    def _smooth_map(self) -> None:
        """
        Smooths the map using nodes to the right and below
        to average out the elevation and temperature.
        :return: None
        """
        for x in range(self.dimension[0] - 1):
            for y in range(self.dimension[1] - 1):
                node = self.nodes[x][y]
                neighbors = [self.nodes[x + 1][y], self.nodes[x][y + 1]]

                for neighbor in neighbors:
                    if node["elevation"] != neighbor["elevation"]:
                        if random.randrange(0, 100) < 5:
                            a = (node["elevation"] + neighbor["elevation"]) / 2
                            node["elevation"] = a
                            neighbor["elevation"] = a
                        elif random.randrange(0, 100) < 5:
                            a = (node["temperature"] + neighbor["temperature"]) / 2
                            node["temperature"] = a
                            neighbor["temperature"] = a

    def _raise_land(self) -> None:
        """
        Raises land by 100 if the elevation is above 0
        :return: None
        """
        for node in numpy.ndenumerate(self.nodes):
            if node[1]["elevation"] > 0 and random.randrange(0, 100) < 1:
                node[1]["elevation"] += 100

    def _lower_sea(self) -> None:
        """
        Lowers sea by 100 if the elevation is below 0
        :return: None
        """
        for node in numpy.ndenumerate(self.nodes):
            if node[1]["elevation"] <= 0 and random.randrange(0, 100) < 1:
                node[1]["elevation"] -= 100

    def _raise_temperature(self) -> None:
        """
        Raises temperature by 10 if the elevation is above 0
        :return: None
        """
        for node in numpy.ndenumerate(self.nodes):
            if node[1]["elevation"] > 0 and random.randrange(0, 100) < 1:
                node[1]["temperature"] += 10

    def generate_map(self, multiplier: int = 1) -> None:
        """
        :param multiplier: how many times to run the generation
        :return: None
        """
        for _ in range(100 * multiplier):
            self._smooth_map()
            self._raise_temperature()
        for _ in range(15 * multiplier):
            self._lower_sea()
            self._raise_land()
        for _ in range(125 * multiplier):
            self._smooth_map()

    # def make_img(self, file: str = "map.png") -> None:
    #     """
    #     Makes an image of the map
    #     :param file: file name to save the image as, defaults to `map.png`
    #     :return: None
    #     """
    #     from PIL import Image
    #
    #     img = Image.new("RGB", self.dimension)
    #
    #     colours = {
    #         "deep_water": (0, 0, 165),
    #         "shallow_water": (80, 78, 250),
    #         "ice": (130, 215, 200),
    #         "snow": (205, 240, 250),
    #         "forest": (30, 115, 30),
    #         "planes": (10, 175, 5),
    #         "desert": (230, 215, 135),
    #     }
    #
    #     for node in numpy.ndenumerate(self.nodes):
    #         if node[1]["elevation"] <= (-25):
    #             img.putpixel(node[0], colours["deep_water"])
    #         elif node[1]["elevation"] <= self.sea_level:
    #             img.putpixel(node[0], colours["shallow_water"])
    #         else:
    #             if node[1]["temperature"] <= -10:
    #                 img.putpixel(node[0], colours["ice"])
    #             elif node[1]["temperature"] <= 0:
    #                 img.putpixel(node[0], colours["snow"])
    #             elif node[1]["temperature"] <= 10:
    #                 img.putpixel(node[0], colours["forest"])
    #             elif node[1]["temperature"] <= 20:
    #                 img.putpixel(node[0], colours["planes"])
    #             elif node[1]["temperature"] <= 38:
    #                 img.putpixel(node[0], colours["desert"])
    #             else:
    #                 img.putpixel(node[0], (0, 0, 0))
    #
    #     img.save(file)
    #     img.close()


if __name__ == "__main__":
    world = GenerateMap((200, 200))
    world.generate_map()
    # world.make_img()
