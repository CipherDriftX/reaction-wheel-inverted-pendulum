# cad

The design is code: `build.py` (CadQuery) makes every part.
Change a number at the top of `build.py`, rerun, and the files below are rebuilt.

- `build.py` the design. All sizes are parameters at the top.
- `step/` one STEP per part + `assembly.step` (whole machine)
- `stl/` printed parts only, for the 3D printer

## Rebuild

```
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python cadquery
.venv/bin/python cad/build.py
```

## Parts

Printed: `base_box`, `upright`, `arm`, `wheel`, `sensor_bracket`.
Bought parts and what to measure first: `docs/parts.md`.

Design numbers (defaults):

- Pendulum length L (pivot to wheel axis): 150 mm
- Wheel: 120 mm OD, 12 mm rim, 12 x M4 holes for tuning inertia
- Pivot height above box top: L + wheel radius + 20 mm = 230 mm
- Upright height: 255 mm. Fits a 256 mm printer.

## Onshape and MuJoCo

In Onshape: Create > Import `step/assembly.step`, then insert it into an Assembly.
An imported STEP is a fixed solid, so size changes happen in `build.py`, not in Onshape.

- Onshape link: (paste here)

For MuJoCo, `onshape-to-robot` turns the Onshape Assembly into a MuJoCo model.
It reads mates whose name starts with `dof_`: add a revolute mate `dof_pivot`
(upright ↔ arm) and `dof_wheel` (arm ↔ wheel). Its output goes to `sim/model/`.
