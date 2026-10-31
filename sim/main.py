"""Step 3: check the sim against the hand math. No motor, only gravity."""

import math
import time
from pathlib import Path

import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path(str(Path(__file__).parent / "model" / "pendulum.xml"))
data = mujoco.MjData(model)

# Test 1: hanging, small push. One swing should take 0.770 s (docs/math).
data.qpos[0] = math.pi + 0.05              # qpos[0] = arm angle. 0 = up, pi = down
turns = []
while len(turns) < 2:
    old_speed = data.qvel[0]               # qvel[0] = arm speed
    mujoco.mj_step(model, data)            # move time forward 1 ms
    if old_speed < 0 <= data.qvel[0]:      # arm stops and turns back, always on the same side
        turns.append(data.time)
print(f"swing time: {turns[1] - turns[0]:.3f} s   (hand math: 0.770 s)")

# Test 2: almost upright. It must fall. Watch it.
mujoco.mj_resetData(model, data)
data.qpos[0] = 0.05
with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()                      # draw the new state
        time.sleep(model.opt.timestep)     # run at about real speed
