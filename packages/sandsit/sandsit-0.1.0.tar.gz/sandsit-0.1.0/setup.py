from setuptools import setup

setup(
    name = 'sandsit',
    version = '0.1.0',
    packages = ['sandsit'],
    entry_points = {
        'console_scripts': [
            'sandsit = sandsit.__main__:main'
        ]
    })
