"""
Python Map Generation
=====================
Simple python world generation
"""

from setuptools import setup, find_packages

setup(
    name="py-map-generation",
    version="0.0.1",
    license="Unlicensed",
    author="Michał Gdula (Fluffy-Bean)",
    author_email="<michal-gdula@protonmail.com>",
    description="Simple python world generation",
    packages=find_packages(),
    py_modules=["py_map_generation"],
    install_requires=[
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
