from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='openai_helpers',
    version='0.1.2',
    url='https://github.com/et0x/openai-helpers',
    packages=find_packages(),
    install_requires=requirements,
)
