from setuptools import setup

# Read requirements from requirements.txt
def read_requirements():
    with open("requirements.txt") as req_file:
        return req_file.readlines()

setup(
    name="file-processing",
    version="1.0.0",
    install_requires=read_requirements(),
)
