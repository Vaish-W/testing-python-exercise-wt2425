"""
Tests for functionality checks in class SolveDiffusion2D
"""
import sys
import os

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from diffusion2d import SolveDiffusion2D
import numpy as np


def test_initialize_physical_parameters():
    """
    Integration test for initialize_physical_parameters and initialize_domain
    """
    solver = SolveDiffusion2D()
    
    # Initialize the domain
    solver.initialize_domain(w=10.0, h=10.0, dx=0.1, dy=0.1)
    
    # Initialize physical parameters
    D, T_cold, T_hot = 2.5, 250.0, 750.0
    solver.initialize_physical_parameters(d=D, T_cold=T_cold, T_hot=T_hot)
    
    # Manually compute expected dt
    dx2, dy2 = solver.dx ** 2, solver.dy ** 2
    expected_dt = dx2 * dy2 / (2 * D * (dx2 + dy2))
    
    # Assert dt is correctly calculated
    assert np.isclose(solver.dt, expected_dt, atol=1e-6), f"Expected dt: {expected_dt}, but got: {solver.dt}"


def test_set_initial_condition():
    """
    Integration test for set_initial_condition and initialize_domain
    """
    solver = SolveDiffusion2D()
    
    # Initialize the domain
    solver.initialize_domain(w=10.0, h=10.0, dx=1.0, dy=1.0)
    
    # Initialize physical parameters
    solver.T_cold = 300.0
    solver.T_hot = 700.0
    
    # Set initial conditions
    u = solver.set_initial_condition()
    
    # Manually compute the expected initial condition array
    expected_u = np.full((10, 10), 300.0)  # Initialize with T_cold
    r, cx, cy = 2, 5, 5
    r2 = r ** 2
    for i in range(10):
        for j in range(10):
            p2 = (i - cx) ** 2 + (j - cy) ** 2
            if p2 < r2:
                expected_u[i, j] = 700.0  # Set T_hot for points inside the circle
    
    # Assert the computed field matches the expected field
    assert np.array_equal(u, expected_u), "The initial condition array is incorrect"
