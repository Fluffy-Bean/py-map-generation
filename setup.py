"""
Python Map Generation
=====================
Simple python world generation
"""

from setuptools import setup, find_packages

VERSION = "0.1.0"
setup(
    name="py-map-generation",
    version=VERSION,
    license="Unlicense",
    author="Michał Gdula (Fluffy-Bean)",
    author_email="<michal-gdula@protonmail.com>",
    description="Simple python world generation",
    packages=find_packages(),
    py_modules=["py_map_generation"],
    install_requires=["numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
