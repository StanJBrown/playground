#!/usr/bin/env python
from random import rand
import numpy as np

from playground.population import Population


class PSOParticle(object):
    def __init__(self, **kwargs):
        # score
        self.score = kwargs.get("score", None)
        self.best_score = kwargs.get("best_score", None)

        # position
        self.position = kwargs.get("position", None)
        self.best_position = kwargs.get("best_position", None)

        # velocity
        self.velocity = kwargs.get("velocity", None)

    def update_velocity(self, population, c_1, c_2):
        best = population.best_individuals[0]

        # convert python list to numpy array
        self.best_position = np.array(self.best_position)
        self.position = np.array(self.position)
        best.position = np.array(best.position)

        # calculate cognitive and social components
        cog = c_1 * rand() * (self.best_position - self.position).tolist()
        soc = c_2 * rand() * (best.best_position - self.position).tolist()

        # convert numpy array back to python list
        self.best_position = self.best_position.tolist()
        self.position = self.position.tolist()
        best.position = best.position.tolist()

        # update velocity
        self.velocity = self.velocity + cog + soc

    def update_position(self, bounds):
        # convert python list to numpy array
        self.position = np.array(self.position)
        self.velocity = np.array(self.velocity)

        # update position
        self.position = self.position + self.velocity

        # convert numpy array back to python list
        self.position = self.position.tolist()

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
        particle.score = obj_func(particle.position)
        particle.best_score = particle.cost

        # position
        particle.position = self.random_vector()
        particle.best_position = particle.position

        # velocity
        particle.velocity = self.random_vector()

        return particle

    def initialize_particles(self, obj_func, config):
        max_pop = config["max_population"]
        population = Population()

        for i in range(max_pop):
            population.individuals.append(self.create_particle(obj_func))




def pso_search(population, objective_function):
    pass


if __name__ == "__main__":
    pass
