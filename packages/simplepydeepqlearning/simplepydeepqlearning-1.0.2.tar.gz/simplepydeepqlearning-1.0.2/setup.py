import setuptools
from setuptools import setup

setup(
    name='simplepydeepqlearning',
    version='1.0.2',
    packages=setuptools.find_packages(),
    url='https://github.com/AdrienDumontet',
    license='Let the package like is it',
    author_email='',
    author='LeLaboDuGame, https://twitch.tv/LeLaboDuGame',
    description='A simple python lib to do Deep Q Learning',
    install_requires=[
        "numpy",
        "tqdm",
        "simplepyai>=2.0.1a0"
    ]
)
