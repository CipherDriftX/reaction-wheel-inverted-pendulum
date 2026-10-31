"""LQR balance, live in MuJoCo. Push the arm with the mouse and watch it recover.
If it falls, the wheel swings it back up to the top, then LQR catches it.

Push: double-click the arm, then hold Ctrl and drag with the right mouse button.
Physics numbers come from docs/math/equations-of-motion.md.
"""

import time
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np
from scipy.linalg import solve_continuous_are

J, I_w, mgl = 0.00389, 0.000146, 0.259   # arm inertia, wheel inertia, gravity strength
CATCH = 0.5                               # rad. Inside: LQR balances. Outside: LQR's math is wrong, so swing up instead

# x = [lean, arm speed, wheel speed].   x' = A x + B push
A = np.array([[0,        1, 0],
              [mgl / J,  0, 0],
              [-mgl / J, 0, 0]])
B = np.array([[0], [-1 / J], [1 / I_w + 1 / J]])

# Bryson's rule: weight = 1 / (biggest value we accept)^2
Q = np.diag([1 / 0.1**2, 1 / 1**2, 1 / 100**2])   # lean 0.1 rad, arm 1 rad/s, wheel 100 rad/s
R = np.array([[1 / 0.1**2]])                       # push 0.1 N·m

K = np.linalg.inv(R) @ B.T @ solve_continuous_are(A, B, Q, R)   # the best gains for these weights
print("K =", K.round(4))

model = mujoco.MjModel.from_xml_path(str(Path(__file__).parents[2] / "sim/model/pendulum.xml"))
data = mujoco.MjData(model)
MAX_PUSH = model.actuator_gainprm[0, 0]            # motor's full torque, from pendulum.xml
data.qpos[0] = 0.1                                 # start leaning 0.1 rad

with mujoco.viewer.launch_passive(model, data) as viewer:
    start = time.time()
    while viewer.is_running():
        while data.time < time.time() - start:     # step physics until it catches up with the real clock
            lean = (data.qpos[0] + np.pi) % (2 * np.pi) - np.pi   # after a full spin, 2*pi is upright again
            x = np.array([lean, data.qvel[0], data.qvel[1]])
            energy = 0.5 * J * data.qvel[0]**2 + mgl * (np.cos(lean) - 1)   # 0 = just enough swing to reach the top
            if abs(lean) < CATCH:
                push = (-K @ x)[0]                 # near the top: LQR balances
            else:
                push = 100 * energy * data.qvel[0] # too little swing: push with it. Too much: brake it
            data.ctrl[0] = np.clip(push / MAX_PUSH, -1, 1)          # motor takes -1..+1
            mujoco.mj_step(model, data)
        viewer.sync()                              # draw, and send your mouse push into the sim
        print(f"\rlean {lean:+.3f} rad   wheel {data.qvel[1]:+7.1f} rad/s   motor {data.actuator_force[0]:+.3f} N·m   ", end="")
        time.sleep(0.01)                           # redraw about 100 times per second
