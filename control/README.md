# control

The brain. Reads the pendulum angle, decides the motor torque.
Tested against the model in `sim/`.

- `pid/` simplest controller, start here
- `lqr/` controller from the physics math
- `rl/` reinforcement learning (training scripts; big trained files stay out of git)

The winner gets rewritten in C++ inside `firmware/`.
