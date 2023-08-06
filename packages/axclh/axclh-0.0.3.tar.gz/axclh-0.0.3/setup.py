from setuptools import setup, find_packages

with open('requirements.txt', 'r') as req_file:
    REQUIREMNTS = req_file.readlines()

setup(
    name='axclh',
    version='0.0.3',
    packages=['axclh'],
    author="axdjuraev",
    description="Package that helps find quick answers realy quick",
    install_requires=REQUIREMNTS,
    entry_points='''
        [console_scripts]
        ac=my_package.cli:main
    '''
)
