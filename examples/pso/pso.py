#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.swarm.pso import PSOParticleGenerator
from playground.swarm.pso import pso_search


def obj_func(vector):
    result = map(lambda el: el ** 2, vector)
    result = reduce(lambda x, y: x + y, result)
    return result


if __name__ == "__main__":
    config = {
        "max_population": 20
    }
    c_1 = 2.0
    c_2 = 2.0
    max_generations = 100

    max_velocity = [10.0, 10.0]
    bounds = [[0, 10], [0, 10]]

    # generate random particles
    generator = PSOParticleGenerator(
        config,
        max_velocity=max_velocity,
        bounds=bounds,
        obj_func=obj_func
    )
    population = generator.init()

    # search
    pso_search(population, max_generations, c_1, c_2, obj_func)
