from setuptools import setup, find_packages

with open('requirements.txt', 'r') as req_file:
    REQUIREMNTS = req_file.readlines()

setup(
    name='axclh',
    version='0.0.1',
    packages=find_packages(),
    install_requires=REQUIREMNTS,
    entry_points={
        'console_scripts': [
            'ac=axclh.main:search'
        ]
    }
)
