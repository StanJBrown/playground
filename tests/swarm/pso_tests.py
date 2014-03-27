#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from playground.swarm.pso import PSOParticle


class PSOParticleTests(unittest.TestCase):
    def setUp(self):
        self.max_velocity = [10.0, 10.0]
        self.bounds = [[0, 0], [10, 10]]

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

    def test_over_bounds(self):
        pass

    def test_update_position(self):
        # update position
        pos_before = list(self.particle.position)
        self.particle.update_position()
        pos_after = list(self.particle.position)

        print "VELOCITY", self.particle.velocity
        print "POSITION BEFORE", pos_before
        print "POSITION AFTER", pos_after

        # assert
        self.assertNotEquals(pos_before, pos_after)

    # def test_update_position_at_boundary(self):
    #     print "HERE--------"
    #     # update position with boundary condition
    #     self.particle.position = [10, 10]
    #     pos_before = list(self.particle.position)
    #     self.particle.update_position()
    #     pos_after = list(self.particle.position)

    #     print "POSITION BEFORE", pos_before
    #     print "POSITION AFTER", pos_after

    #     # assert
    #     self.assertNotEquals(pos_before, pos_after)


if __name__ == "__main__":
    unittest.main()
