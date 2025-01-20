"""
Tests for functions in class SolveDiffusion2D using unittest
"""
import sys
import os

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest
from diffusion2d import SolveDiffusion2D


class TestSolveDiffusion2D(unittest.TestCase):
    def setUp(self):
        self.solver = SolveDiffusion2D()

    def test_initialize_domain(self):
        self.solver.initialize_domain(w=4.0, h=6.0, dx=0.2, dy=0.3)

        # Verify calculated nx and ny
        self.assertEqual(self.solver.nx, 20, "nx calculation is incorrect")
        self.assertEqual(self.solver.ny, 20, "ny calculation is incorrect")

    def test_initialize_physical_parameters(self):
        self.solver.dx = 0.1
        self.solver.dy = 0.1
        self.solver.initialize_physical_parameters(d=2.5, T_cold=250.0, T_hot=750.0)

        expected_dt = (self.solver.dx ** 2) * (self.solver.dy ** 2) / (2 * 2.5 * ((self.solver.dx ** 2) + (self.solver.dy ** 2)))
        self.assertAlmostEqual(self.solver.dt, expected_dt, places=6, msg="dt calculation is incorrect")

    def test_set_initial_condition(self):
        self.solver.initialize_domain(w=10.0, h=10.0, dx=1.0, dy=1.0)
        self.solver.T_cold = 300.0
        self.solver.T_hot = 700.0

        u = self.solver.set_initial_condition()

        # Verify shape and temperature values
        self.assertEqual(u.shape, (10, 10), "Initial condition array shape is incorrect")
        self.assertGreater((u == 300.0).sum(), 0, "T_cold is not set correctly")
        self.assertGreater((u == 700.0).sum(), 0, "T_hot is not set correctly")


if __name__ == "__main__":
    unittest.main()
