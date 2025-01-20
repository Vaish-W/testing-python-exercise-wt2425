# Python code to solve the diffusion equation in 2D

Please follow the instructions in [python_testing_exercise.md](https://github.com/Simulation-Software-Engineering/Lecture-Material/blob/main/05_testing_and_ci/python_testing_exercise.md).

## Test logs (for submission)

### pytest log
After changing self.nx = int(w / dx) to self.nx = int(h / dx)

PS D:\COMMAS\SSE\testing-python-exercise-wt2425> pytest tests/unit/test_diffusion2d_functions.py
================================================================ test session starts =================================================================
platform win32 -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: D:\COMMAS\SSE\testing-python-exercise-wt2425
collected 3 items

tests\unit\test_diffusion2d_functions.py F..                                                                                                    [100%]

====================================================================== FAILURES====================================================================== 
_______________________________________________________________ test_initialize_domain _______________________________________________________________ 

    def test_initialize_domain():
        """
        Check function SolveDiffusion2D.initialize_domain
        """
        solver = SolveDiffusion2D()

        solver.initialize_domain(w=4.0, h=6.0, dx=0.2, dy=0.3)

        # Assert the values of the domain parameters
>       assert solver.nx == 20  # 4.0 / 0.2
E       assert 30 == 20
E        +  where 30 = <diffusion2d.SolveDiffusion2D object at 0x000001A05432FCB0>.nx

tests\unit\test_diffusion2d_functions.py:21: AssertionError
============================================================== short test summary info=============================================================== 
FAILED tests/unit/test_diffusion2d_functions.py::test_initialize_domain - assert 30 == 20
============================================================ 1 failed, 2 passed in 0.59s============================================================= 
### unittest log
- Failure:

.dt = 0.0010000000000000002
F.
======================================================================
FAIL: test_initialize_physical_parameters (__main__.TestSolveDiffusion2D.test_initialize_physical_parameters)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\COMMAS\SSE\testing-python-exercise-wt2425\tests\unit\test_diffusion2d_functions_unittest.py", line 31, in test_initialize_physical_parameters
    self.assertAlmostEqual(self.solver.dt, expected_dt, places=6, msg="dt calculation is incorrect")
AssertionError: 0.0010000000000000002 != 0.010000000000000002 within 6 places (0.009000000000000001 difference) : dt calculation is incorrect

----------------------------------------------------------------------
Ran 3 tests in 0.004s

FAILED (failures=1)
Backend tkagg is interactive backend. Turning interactive mode on.


- After updating formula for dt

.dt = 0.0010000000000000002
..
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK

- with self.nx = int(h / dx) an intentional bug
Fdt = 0.0010000000000000002
..
======================================================================
FAIL: test_initialize_domain (__main__.TestSolveDiffusion2D.test_initialize_domain)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\COMMAS\SSE\testing-python-exercise-wt2425\tests\unit\test_diffusion2d_functions_unittest.py", line 22, in test_initialize_domain
    self.assertEqual(self.solver.nx, 20, "nx calculation is incorrect")
AssertionError: 30 != 20 : nx calculation is incorrect

----------------------------------------------------------------------
Ran 3 tests in 0.003s

FAILED (failures=1)
Backend tkagg is interactive backend. Turning interactive mode on.

### integration_test log
- with intensional bug in initialize_physical_parameters and set_initial_condition

================================================================ test session starts================================================================= 
platform win32 -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: D:\COMMAS\SSE\testing-python-exercise-wt2425
collected 2 items

tests\integration\test_diffusion2d.py F.                                                                                                        [100%]

====================================================================== FAILURES====================================================================== 
________________________________________________________ test_initialize_physical_parameters _________________________________________________________ 

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
>       assert np.isclose(solver.dt, expected_dt, atol=1e-6), f"Expected dt: {expected_dt}, but got: {solver.dt}"
E       AssertionError: Expected dt: 0.0010000000000000002, but got: 0.1
E       assert np.False_
E        +  where np.False_ = <function isclose at 0x000001DCB2B3A8F0>(0.1, 0.0010000000000000002, atol=1e-06)
E        +    where <function isclose at 0x000001DCB2B3A8F0> = np.isclose
E        +    and   0.1 = <diffusion2d.SolveDiffusion2D object at 0x000001DCB52575F0>.dt

tests\integration\test_diffusion2d.py:31: AssertionError
---------------------------------------------------------------- Captured stdout call---------------------------------------------------------------- 
dt = 0.1
============================================================== short test summary info=============================================================== 
FAILED tests/integration/test_diffusion2d.py::test_initialize_physical_parameters - AssertionError: Expected dt: 0.0010000000000000002, but got: 0.1   
============================================================ 1 failed, 1 passed in 0.58s============================================================= 

================================================================ test session starts =================================================================
platform win32 -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: D:\COMMAS\SSE\testing-python-exercise-wt2425
collected 2 items

tests\integration\test_diffusion2d.py .F                                                                                                        [100%]

====================================================================== FAILURES====================================================================== 
_____________________________________________________________ test_set_initial_condition _____________________________________________________________ 

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
>       assert np.array_equal(u, expected_u), "The initial condition array is incorrect"
E       AssertionError: The initial condition array is incorrect
E       assert False
E        +  where False = <function array_equal at 0x000002536C642030>(array([[700., 700., 700., 700., 700., 700., 700., 700., 700., 700.],\n       [700., 700., 700., 700., 700., 700., 700.,... 700., 700., 700., 700., 700., 700., 700., 700.],\n       [700., 700., 700., 700., 700., 700., 700., 700., 700., 700.]]), array([[300., 300., 300., 300., 300., 300., 300., 300., 300., 300.],\n       [300., 300., 300., 300., 300., 300., 300.,... 300., 300., 300., 300., 300., 300., 300., 300.],\n       [300., 300., 300., 300., 300., 300., 300., 300., 300., 300.]]))
E        +    where <function array_equal at 0x000002536C642030> = np.array_equal

tests\integration\test_diffusion2d.py:61: AssertionError
============================================================== short test summary info=============================================================== 
FAILED tests/integration/test_diffusion2d.py::test_set_initial_condition - AssertionError: The initial condition array is incorrect
============================================================ 1 failed, 1 passed in 0.57s============================================================= 
## Citing

The code used in this exercise is based on [Chapter 7 of the book "Learning Scientific Programming with Python"](https://scipython.com/book/chapter-7-matplotlib/examples/the-two-dimensional-diffusion-equation/).
