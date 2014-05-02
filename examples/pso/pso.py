#!/usr/bin/env python2.7
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
        "c_1": 2.0,
        "c_2": 2.0,

        "max_population": 20,
        "max_generations": 50,

        "max_velocity": [0.5, 0.5],
        "bounds": [[0, 10], [0, 10]],
        "objective_function": obj_func,

        "animate": True,
        "animation_frame_delay": 0.1
    }

    # generate random particles
    generator = PSOParticleGenerator(config)
    population = generator.init()

    # search
    pso_search(population, config)
