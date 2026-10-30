# Reaction Wheel Inverted Pendulum

A pendulum that balances itself upright by spinning a wheel at its top.
Built first in software (Onshape, MuJoCo, PlatformIO, Wokwi), then in real parts.

| Folder      | What lives there                              | Tool        |
|-------------|-----------------------------------------------|-------------|
| `docs/`     | Notes, decisions, math, parts list, datasheets | any         |
| `cad/`      | Exports from the Onshape design               | Onshape     |
| `sim/`      | Physics model of the robot                    | MuJoCo      |
| `control/`  | The brain: PID, LQR, RL                       | Python      |
| `firmware/` | Code that runs on the ESP32                   | PlatformIO + Wokwi |

How the pieces connect:

    cad  ──export──▶  sim  ◀──tests──  control  ──port to C++──▶  firmware
