

from setuptools import setup, find_packages

with open('requirements.txt') as file:
    INSTALL_REQUIERES = file.read().splitlines()

setup(
	author="GeoMak",
	description="Travelling salesman problem",
	name="tspnoq",
	version="0.0.5",
	py_modules=["tspnoq"],
	packages=find_packages(include=['tspnoq']),
	install_requires= INSTALL_REQUIERES
	
	)





						
