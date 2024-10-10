from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        # Exclude Git-based dependencies from 'install_requires'
        requirements = [line for line in lines if not line.startswith("git+")]
        return requirements

def parse_dependency_links(filename):
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        # Only include Git-based dependencies in 'dependency_links'
        dependency_links = [line for line in lines if line.startswith("git+")]
        return dependency_links

setup(
    name="file-processing",
    version="1.0.0",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    dependency_links=parse_dependency_links('requirements.txt'),
)
