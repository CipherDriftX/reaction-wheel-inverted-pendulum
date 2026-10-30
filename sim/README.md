# sim

The physics world. MuJoCo pretends to be gravity, the arm and the wheel.

- `model/` MuJoCo XML file + mesh files (by hand first, later from `cad/`)
- `*.py` scripts that load the model and run it

Rule: this folder only knows physics. No controller code here.
