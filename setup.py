#!/usr/bin/env python
from setuptools import setup
from setuptools import find_packages

setup(
    name="playground",
    version="0.1",
    description="Evoluationary Algorithms Library",
    author="Chris Choi",
    author_email="chutsu@gmail.com",
    packages=find_packages(),
    data_files=[
        (
            'examples/symbolic_regression',
            ['examples/symbolic_regression/config.json'],

            'examples/symbolic_regression/training_data',
            ['examples/symbolic_regression/training_data/sine.dat'],

            'playground/recorder',
            [
                'recorder/schemas/default.sql',
                'recorder/schemas/purge_default.sql'
            ]
        )
    ]
)
