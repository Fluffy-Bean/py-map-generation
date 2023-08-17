# -*- coding: utf-8 -*-
from .main import GenerateMap

GenerateMap = GenerateMap

if __name__ == "__main__":
    world = GenerateMap((200, 200))
    world.generate_map()
    # world.make_img()
