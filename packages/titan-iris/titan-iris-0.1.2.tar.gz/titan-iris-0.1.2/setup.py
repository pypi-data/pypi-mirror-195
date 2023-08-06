import os
import sys

from setuptools import find_packages, setup

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + "/requirements.txt"
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
    name="titan-iris",
    version="0.1.2",
    install_requires=[
        "typer ~= 0.7.0",
        "rich ~= 13.3.1",
        "omegaconf ~= 2.3.0",
        "requests ~= 2.28.2",
        "auth0-python ~= 3.24.1",
        "python-dotenv ~= 0.19.1",
        "docker ~= 6.0.1",
        "tqdm ~=4.64.1",
        "wget ~= 3.2",
        "jmespath ~= 1.0"
    ],
    entry_points={"console_scripts": ["iris = iris.main:main"]},
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
)
