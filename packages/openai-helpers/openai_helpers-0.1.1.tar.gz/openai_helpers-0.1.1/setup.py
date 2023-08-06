from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='openai_helpers',
    version='0.1.1',
    packages=find_packages(),
    install_requires=requirements,
)
