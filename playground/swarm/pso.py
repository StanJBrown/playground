#!/usr/bin/env python2.7
import os
import sys
import time
from random import random
from random import uniform
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import matplotlib.pylab as plt

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
            # calcuate cognitive and social components
            cog = c_1 * random() * (self.best_position[i] - self.position[i])
            soc = c_2 * random() * (best.best_position[i] - self.position[i])

            # update velocity
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
    def __init__(self, config):
        self.config = config

        self.bounds = config.get("bounds", None)
        self.max_velocity = config.get("max_velocity", None)
        self.obj_func = config.get("objective_function", None)

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


def pso_search(population, config):
    obj_func = config["objective_function"]
    gbest = population.find_best_individuals()[0]
    max_generations = config["max_generations"]
    c_1 = config["c_1"]
    c_2 = config["c_2"]

    # search loop
    for gen in range(max_generations):
        # update particles
        for particle in population.individuals:
            particle.update_velocity(gbest, c_1, c_2)
            particle.update_position()
            particle.score = obj_func(particle.position)
            particle.update_best_position()

        # update global best
        population.sort_individuals()
        gen_best = population.find_best_individuals()[0]
        if gen_best.score < gbest.score:
            gbest = PSOParticle(
                score=gen_best.score,
                position=list(gen_best.position),
                velocity=list(gen_best.velocity),
                bounds=gen_best.bounds,
                max_velocity=gen_best.max_velocity
            )

        # print
        print " > gen {0}, fitness={1}".format(gen, gbest.score)

        # display animation
        if config.get("animate", False):
            # pre-check
            if len(config["bounds"]) > 2:
                raise RuntimeError("Animate does not support > 2 dimensions!")

            # animate swarm
            x = [p.position[0] for p in population.individuals]
            y = [p.position[1] for p in population.individuals]

            plt.clf()  # clear figure
            plt.scatter(x, y)
            plt.xlim(config["bounds"][0])
            plt.ylim(config["bounds"][1])
            plt.draw()
            plt.show(block=False)
            time.sleep(config.get("animation_frame_delay", 0.1))

    return (gbest.position, gbest.score)
