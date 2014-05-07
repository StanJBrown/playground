#!/usr/bin/env python2
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.swarm.pso import PSOParticle
from playground.swarm.pso import PSOParticleGenerator
from playground.swarm.pso import pso_search


class PSOParticleTests(unittest.TestCase):
    def setUp(self):
        self.max_velocity = [10.0, 10.0]
        self.bounds = [[0, 10], [0, 10]]

        self.best = PSOParticle(
            score=0.0,
            position=[1.0, 1.0],
            velocity=[1.0, 1.0],
            max_velocity=self.max_velocity,
            bounds=self.bounds
        )

        self.particle = PSOParticle(
            score=0.1,
            position=[3.0, 4.0],
            velocity=[1.0, 1.0],
            max_velocity=self.max_velocity,
            bounds=self.bounds
        )

    def tearDown(self):
        pass

    def test_update_velocity(self):
        # update velocity
        vel_before = list(self.particle.velocity)
        self.particle.update_velocity(self.best, 2.0, 2.0)
        vel_after = list(self.particle.velocity)

        # print "VELOCITY BEFORE", vel_before
        # print "VELOCITY AFTER", vel_after

        # assert
        self.assertNotEquals(vel_before, vel_after)

        # update velocity with max velocity
        self.particle.velocity = [100, 100]
        vel_before = list(self.particle.velocity)
        self.particle.update_velocity(self.best, 2.0, 2.0)
        vel_after = list(self.particle.velocity)

        # print "VELOCITY BEFORE", vel_before
        # print "VELOCITY AFTER", vel_after

        # assert
        self.assertNotEquals(vel_before, vel_after)
        self.assertEquals(vel_after, self.max_velocity)

    def test_check_over_bounds(self):
        # check no boundary violation
        self.particle.position = [5, 5]
        before = list(self.particle.position)
        self.particle.check_over_bounds()
        after = list(self.particle.position)

        # assert
        self.assertEquals(before, after)

        # check x-axis under bounds
        self.particle.position = [-1, 5]
        before = list(self.particle.position)
        self.particle.check_over_bounds()
        after = list(self.particle.position)
        # print "x-axis under bounds[BEFORE]:", before
        # print "x-axis under bounds[AFTER]:", after

        # assert
        self.assertEquals(self.particle.position, [1, 5])

        # check x-axis over bounds
        self.particle.position = [11, 5]
        before = list(self.particle.position)
        self.particle.check_over_bounds()
        after = list(self.particle.position)
        # print "x-axis over bounds[BEFORE]:", before
        # print "x-axis over bounds[AFTER]:", after

        # assert
        self.assertEquals(self.particle.position, [9, 5])

        # check y-axis under bounds
        self.particle.position = [5, -1]
        before = list(self.particle.position)
        self.particle.check_over_bounds()
        after = list(self.particle.position)
        # print "y-axis over bounds[BEFORE]:", before
        # print "y-axis over bounds[AFTER]:", after

        # assert
        self.assertEquals(self.particle.position, [5, 1])

        # check y-axis over bounds
        self.particle.position = [5, 11]
        before = list(self.particle.position)
        self.particle.check_over_bounds()
        after = list(self.particle.position)
        # print "y-axis over bounds[BEFORE]:", before
        # print "y-axis over bounds[AFTER]:", after

        # assert
        self.assertEquals(self.particle.position, [5, 9])

    def test_update_position(self):
        # update position
        pos_before = list(self.particle.position)
        self.particle.update_position()
        pos_after = list(self.particle.position)

        # print "VELOCITY", self.particle.velocity
        # print "POSITION BEFORE", pos_before
        # print "POSITION AFTER", pos_after

        # assert
        self.assertNotEquals(pos_before, pos_after)


class PSOParticleGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.max_velocity = [10.0, 10.0]
        self.bounds = [[0, 10], [0, 10]]

        config = {
            "max_population": 5,
            "max_velocity": self.max_velocity,
            "bounds": self.bounds,
            "objective_function": self.obj_func
        }

        self.particle = PSOParticle(
            score=0.0,
            position=[1.0, 1.0],
            velocity=[1.0, 1.0],
            max_velocity=self.max_velocity,
            bounds=self.bounds
        )

        self.generator = PSOParticleGenerator(config)

    def tearDown(self):
        pass

    def obj_func(self, vector):
        result = map(lambda el: el ** 2, vector)
        result = reduce(lambda x, y: x + y, result)
        return result

    def test_random_vector(self):
        # test random position vector
        test = 100
        for i in range(test):
            result = self.generator.random_position_vector()

            # x-axis is between the min and max boundary
            self.assertTrue(result[0] >= self.bounds[0][0])
            self.assertTrue(result[0] <= self.bounds[0][1])

            # y-axis is between the min and max boundary
            self.assertTrue(result[1] >= self.bounds[1][0])
            self.assertTrue(result[1] <= self.bounds[1][1])

    def test_random_velocity_vector(self):
        # test random velocity vector
        test = 100
        for i in range(test):
            result = self.generator.random_velocity_vector()

            # x-axis is between the within the max velocity
            self.assertTrue(result[0] <= self.max_velocity[0])
            self.assertTrue(result[0] >= -self.max_velocity[0])

            # y-axis is between the within the max velocity
            self.assertTrue(result[1] <= self.max_velocity[1])
            self.assertTrue(result[1] >= -self.max_velocity[1])

    def test_create_particle(self):
        # test create particle
        result = self.generator.create_particle()

        # print "POSITION:", result.position
        # print "VELOCITY:", result.velocity
        # print "SCORE:", result.score
        # print "BEST SCORE:", result.best_score

        # essential fields cannot be None
        self.assertIsNotNone(result.position)
        self.assertIsNotNone(result.velocity)
        self.assertIsNotNone(result.score)
        self.assertIsNotNone(result.best_score)
        self.assertIsNotNone(result.bounds)
        self.assertIsNotNone(result.max_velocity)

        self.assertEquals(result.score, result.best_score)

        # make sure position and velocity is within boundaries
        self.assertTrue(result.position[0] >= self.bounds[0][0])
        self.assertTrue(result.position[0] <= self.bounds[0][1])
        self.assertTrue(result.position[1] >= self.bounds[1][0])
        self.assertTrue(result.position[1] <= self.bounds[1][1])

        self.assertTrue(result.velocity[0] <= self.max_velocity[0])
        self.assertTrue(result.velocity[0] >= -self.max_velocity[0])
        self.assertTrue(result.velocity[1] <= self.max_velocity[1])
        self.assertTrue(result.velocity[1] >= -self.max_velocity[1])

    def test_init(self):
        population = self.generator.init()

        for particle in population.individuals:
            # print "POSITION:", particle.position
            # print "VELOCITY:", particle.velocity
            # print "SCORE:", particle.score
            # print "BEST SCORE:", particle.best_score

            # essential fields cannot be None
            self.assertIsNotNone(particle.position)
            self.assertIsNotNone(particle.velocity)
            self.assertIsNotNone(particle.score)
            self.assertIsNotNone(particle.best_score)
            self.assertIsNotNone(particle.bounds)
            self.assertIsNotNone(particle.max_velocity)

            self.assertEquals(particle.score, particle.best_score)

            # make sure position and velocity is within boundaries
            self.assertTrue(particle.position[0] >= self.bounds[0][0])
            self.assertTrue(particle.position[0] <= self.bounds[0][1])
            self.assertTrue(particle.position[1] >= self.bounds[1][0])
            self.assertTrue(particle.position[1] <= self.bounds[1][1])

            self.assertTrue(particle.velocity[0] <= self.max_velocity[0])
            self.assertTrue(particle.velocity[0] >= -self.max_velocity[0])
            self.assertTrue(particle.velocity[1] <= self.max_velocity[1])
            self.assertTrue(particle.velocity[1] >= -self.max_velocity[1])


class PSOTest(unittest.TestCase):
    def setUp(self):
        self.config = {
            "c_1": 2.0,
            "c_2": 2.0,

            "max_population": 10,
            "max_generations": 20,

            "max_velocity": [0.5, 0.5],
            "bounds": [[0, 10], [0, 10]],
            "objective_function": self.obj_func,

            "animate": True,
            "animation_frame_delay": 0.0
        }

        # generate random particles
        generator = PSOParticleGenerator(self.config)
        self.population = generator.init()

    def obj_func(self, vector):
        result = map(lambda el: el ** 2, vector)
        result = reduce(lambda x, y: x + y, result)
        return result

    def test_pso_search(self):
        result = pso_search(self.population, self.config)
        self.assertTrue(result[0][0] < 1.0)
        self.assertTrue(result[0][1] < 1.0)
        self.assertTrue(result[1] < 1.0)


if __name__ == "__main__":
    unittest.main()
