# cad

The real design lives in Onshape (in the cloud). This folder keeps copies.

- Onshape link: (paste here)
- `step/` STEP exports, for sharing and backup
- `stl/` STL exports, for 3D printing

Main parts: base frame, pendulum arm, pivot joint, reaction wheel, motor mount.

For MuJoCo, the tool `onshape-to-robot` turns the Onshape assembly into
a MuJoCo model. It reads mates whose name starts with `dof_`
(example: a revolute mate called `dof_pivot`). Its output goes to `sim/model/`.
