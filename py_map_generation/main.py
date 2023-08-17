# -*- coding: utf-8 -*-

"""
Python Map Generation
=====================
Simple python world generation
"""

import os
import random
import numpy
from PIL import Image


class GenerateMap:
    """Generate a map main class"""

    def __init__(self, dimension: tuple, seed: int = 621) -> None:
        """
        :param dimension: x, y tuple for the size of the map
        :param seed: seed for random, must be int
        """
        random.seed(seed)

        self._map_border = 17
        self._land_density = 70
        self._temp_and_elev_choice = (-100, 200)
        self._environment = {
            "ice": -5,
            "snow": 0,
            "grassland": 10,
            "savanna": 20,
            "desert": 35,
        }

        self.sea_level = 0
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
                    self.nodes,
                    {
                        "elevation": 0,
                        "temperature": 0,
                        "environment": "grassland",
                    },
                )

        self.nodes = numpy.reshape(self.nodes, self.dimension)

    def _fill_nodes(self) -> None:
        """
        Fills nodes with random data
        :return: None
        """
        for node in numpy.ndenumerate(self.nodes):
            if (
                self._map_border < node[0][0] < (self.dimension[0] - self._map_border)
                and self._map_border
                < node[0][1]
                < (self.dimension[1] - self._map_border)
                and random.randint(0, 1000) <= self._land_density
            ):
                node[1]["elevation"] = random.choice(self._temp_and_elev_choice)
                node[1]["temperature"] = random.choice(self._temp_and_elev_choice)

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
            if node[1]["elevation"] > 0 and random.randrange(0, 125) < 1:
                node[1]["temperature"] += 10

    def _set_environment(self) -> None:
        for node in numpy.ndenumerate(self.nodes):
            if node[1]["elevation"] < self.sea_level:
                node[1]["environment"] = "sea"
            else:
                for environment in self._environment:
                    if node[1]["temperature"] <= self._environment[environment]:
                        node[1]["environment"] = environment
                        break

    def generate_map(self, multiplier: int = 1) -> numpy.array:
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
        for _ in range(115 * multiplier):
            self._smooth_map()

        self._set_environment()

        return self.nodes

    def make_map(self, file: str = "map.png", full_path: str = ".") -> None:
        """
        Makes an image of the map
        :param file: file name to save the image as, defaults to `map.png`
        :param full_path: full path to save the image to, defaults to `.` (current directory)
        :return: None
        """

        image = Image.new("RGB", self.dimension)
        file_path = os.path.join(full_path, file)

        colours = {
            # "sea": (0, 0, 165),
            # "ice": (130, 215, 200),
            # "snow": (205, 240, 250),
            # "grassland": (30, 115, 30),
            # "savanna": (10, 175, 5),
            # "desert": (230, 215, 135),
            "sea": (66, 77, 79),
            "ice": (149, 155, 161),
            "snow": (149, 155, 161),
            "grassland": (48, 50, 23),
            "savanna": (64, 47, 30),
            "desert": (132, 102, 76),
        }

        for node in numpy.ndenumerate(self.nodes):
            image.putpixel(node[0], colours[node[1]["environment"]])

        image.save(file_path)
        image.close()


if __name__ == "__main__":
    world = GenerateMap((250, 250))
    world.generate_map()
    world.make_map()
