"""
Tests for functions in class SolveDiffusion2D using pytest
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from diffusion2d import SolveDiffusion2D


def test_initialize_domain():
    """
    Check function SolveDiffusion2D.initialize_domain
    """
    solver = SolveDiffusion2D()

    solver.initialize_domain(w=4.0, h=6.0, dx=0.2, dy=0.3)

    # Assert the values of the domain parameters
    assert solver.nx == 20  # 4.0 / 0.2
    assert solver.ny == 20  # 6.0 / 0.3


def test_initialize_physical_parameters():
    """
    Checks function SolveDiffusion2D.initialize_domain
    """
    solver = SolveDiffusion2D()
    solver.initialize_domain(w=10.0, h=10.0, dx=0.5, dy=0.5)
    solver.initialize_physical_parameters(d=1.0, T_cold=300.0, T_hot=700.0)

    # Assert the values of the physical parameters
    assert solver.D == 1.0
    assert solver.T_cold == 300.0
    assert solver.T_hot == 700.0

    # Assert the computed time step
    dx2, dy2 = solver.dx ** 2, solver.dy ** 2
    expected_dt = dx2 * dy2 / (2 * solver.D * (dx2 + dy2))
    assert solver.dt == expected_dt


def test_set_initial_condition():
    """
    Checks function SolveDiffusion2D.get_initial_function
    """
    solver = SolveDiffusion2D()
    solver.initialize_domain(w=10.0, h=10.0, dx=1.0, dy=1.0)
    solver.initialize_physical_parameters(d=1.0, T_cold=300.0, T_hot=700.0)
    u = solver.set_initial_condition()

    # Assert the shape of the initial condition array
    assert u.shape == (10, 10)

    # Assert the initial temperature values in the domain
    assert (u == 300.0).sum() > 0  
    assert (u == 700.0).sum() > 0  
