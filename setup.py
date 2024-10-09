from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()

setup(
    name="file-processing",
    version="1.0.0",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
)