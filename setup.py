#!/usr/bin/env python
from distutils.core import setup

setup(
    name="playground",
    version="0.1",
    description="Genetic Programming Framework",
    author="Chris Choi",
    author_email="chutsu@gmail.com",
    packages=[
        "playground",
        "playground.benchmark",
        "playground.ga",
        "playground.gp",
        "playground.gp.tree",
        "playground.gp.cartesian",
        "playground.operators",
        "playground.playnode",
        "playground.recorder"
    ]
)
