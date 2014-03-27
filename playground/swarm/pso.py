#!/usr/bin/env python
from random import random

from playground.population import Population


class PSOParticle(object):
    def __init__(self, **kwargs):
        self.score = kwargs.get("score", None)
        self.best_score = self.score

        self.position = kwargs.get("position", None)
        self.best_position = self.position

        self.velocity = kwargs.get("velocity", None)
        self.max_velocity = kwargs.get("max_velocity", None)

        self.bounds = kwargs.get("bounds", None)

    def update_velocity(self, best, c_1, c_2):
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

    def over_bounds(self, i):
        print i
        # loop through every boundary
        for bound in self.bounds:
            print bound
            # check if position is over the boundary
            if self.position[i] > bound[i]:
                print "HIT 1!"
                diff = abs(self.position[i] - bound[i])
                print "BEFORE CORRECT", self.position[i]
                self.position[i] = bound[i] - diff
                print "CORRECT", self.position[i]
                self.velocity[i] *= -1.0  # reverse direction

            # under the bound
            elif self.position[i] < bound[i]:
                print "HIT 2!"
                diff = abs(self.position[i] - bound[i])
                print "BEFORE CORRECT", self.position[i]
                self.position[i] = bound[i] + diff
                print "CORRECT", self.position[i]
                self.velocity[i] *= -1.0  # reverse direction

    def update_position(self):
        # loop through each dimension
        for i in range(len(self.position)):
            # update position
            self.position[i] = self.position[i] + self.velocity[i]

            # check if over bounds
            # self.over_bounds(i, self.bounds)

    def update_best_position(self):
        if self.score < self.best_score:
            self.best_score = self.score
            self.best_position = self.position


class PSOParticleGenerator(object):
    def random_vector(self):
        pass

    def create_particle(self, obj_func):
        particle = PSOParticle()

        # score
        particle.score = obj_func(particle.pos)
        particle.best_score = particle.cost

        # position
        particle.pos = self.random_vector()
        particle.bpos = particle.pos

        # velocity
        particle.velocity = self.random_vector()

        return particle

    def initialize_particles(self, obj_func, config):
        max_pop = config["max_population"]
        population = Population()

        for i in range(max_pop):
            population.individuals.append(self.create_particle(obj_func))


def obj_func(vector):
    result = map(lambda el: el ** 2, vector)
    result = reduce(lambda x, y: x + y, result)
    return result


def pso_search(population, objective_function):
    pass


if __name__ == "__main__":
    pass
