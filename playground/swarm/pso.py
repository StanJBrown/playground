#!/usr/bin/env python
import os
import sys
from random import random
from random import uniform
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.population import Population


class PSOParticle(object):
    def __init__(self, **kwargs):
        self.score = kwargs.get("score", None)
        self.best_score = self.score

        self.position = kwargs.get("position", None)
        self.best_position = self.position

        self.velocity = kwargs.get("velocity", None)

        self.bounds = kwargs.get("bounds", None)
        self.max_velocity = kwargs.get("max_velocity", None)

    def update_velocity(self, best, c_1, c_2):
        if self.max_velocity is None:
            raise RuntimeError("max_velocity is None!")

        # loop through each dimension
        for i in range(len(self.position)):
            # update velocity
            cog = c_1 * random() * (self.best_position[i] - self.position[i])
            soc = c_2 * random() * (best.best_position[i] - self.position[i])
            self.velocity[i] = self.velocity[i] + cog + soc

            # if velocity reaches max, cap the velocity
            if self.velocity[i] > self.max_velocity[i]:
                self.velocity[i] = self.max_velocity[i]
            elif self.velocity[i] < -self.max_velocity[i]:
                self.velocity[i] = -self.max_velocity[i]

    def check_over_bounds(self):
        if self.bounds is None:
            raise RuntimeError("bounds is None!")

        # loop through each dimension
        for i in range(len(self.bounds)):
            # get min and max boundary for i-th dimension
            min_bound = self.bounds[i][0]
            max_bound = self.bounds[i][1]

            # check for over the boundary
            if self.position[i] > max_bound:
                diff = abs(self.position[i] - max_bound)
                self.position[i] = max_bound - diff
                self.velocity[i] *= -1.0  # reverse direction

            # check for under the boundary
            elif self.position[i] < min_bound:
                diff = abs(self.position[i] - min_bound)
                self.position[i] = min_bound + diff
                self.velocity[i] *= -1.0  # reverse direction

    def update_position(self):
        # loop through each dimension
        for i in range(len(self.position)):
            # update position
            self.position[i] = self.position[i] + self.velocity[i]

        # check if over bounds
        self.check_over_bounds()

    def update_best_position(self):
        if self.score < self.best_score:
            self.best_score = self.score
            self.best_position = self.position


class PSOParticleGenerator(object):
    def __init__(self, config, **kwargs):
        self.config = config

        self.bounds = kwargs.get("bounds", None)
        self.max_velocity = kwargs.get("max_velocity", None)
        self.obj_func = kwargs.get("obj_func", None)

    def random_velocity_vector(self):
        if self.max_velocity is None:
            raise RuntimeError("max velocity is None!")

        random_vector = []
        for i in range(len(self.max_velocity)):
            min_bound = self.max_velocity[i]
            max_bound = -self.max_velocity[i]

            random_num = uniform(min_bound, max_bound)
            random_vector.append(random_num)

        return random_vector

    def random_position_vector(self):
        if self.bounds is None:
            raise RuntimeError("bounds is None!")

        random_vector = []
        for i in range(len(self.bounds)):
            min_bound = self.bounds[i][0]
            max_bound = self.bounds[i][1]

            random_num = uniform(min_bound, max_bound)
            random_vector.append(random_num)

        return random_vector

    def create_particle(self):
        if self.obj_func is None:
            raise RuntimeError("obj_func is None!")

        particle = PSOParticle()

        # position
        particle.position = self.random_position_vector()
        particle.best_position = particle.position

        # velocity
        particle.velocity = self.random_velocity_vector()

        # score
        particle.score = self.obj_func(particle.position)
        particle.best_score = particle.score

        # boundaries for position and velocity
        particle.bounds = self.bounds
        particle.max_velocity = self.max_velocity

        return particle

    def init(self):
        population = Population(self.config)

        for i in range(self.config["max_population"]):
            particle = self.create_particle()
            population.individuals.append(particle)

        return population


def obj_func(vector):
    result = map(lambda el: el ** 2, vector)
    result = reduce(lambda x, y: x + y, result)
    return result


def pso_search(population, max_generations, c_1, c_2, obj_func):
    gbest = population.find_best_individuals()[0]

    for gen in range(max_generations):
        for particle in population.individuals:
            particle.update_velocity(gbest, c_1, c_2)
            particle.update_position()
            particle.score = obj_func(particle.position)
            particle.update_best_position()

        population.sort_individuals()
        gbest = population.find_best_individuals()[0]

        print " > gen {0}, fitness={1}".format(gen, gbest.score)


if __name__ == "__main__":
    config = {
        "max_population": 5
    }

    max_velocity = [10.0, 10.0]
    bounds = [[0, 10], [0, 10]]

    generator = PSOParticleGenerator(
        config,
        max_velocity=max_velocity,
        bounds=bounds,
        obj_func=obj_func
    )

    population = generator.init()
    print len(population.individuals)

    pso_search(population, 10, 1.0, 1.0, obj_func)
    pass
