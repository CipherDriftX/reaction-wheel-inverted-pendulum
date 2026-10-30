# firmware

Code for the ESP32. This whole folder is one PlatformIO project.

Create it yourself from inside this folder:

    pio project init --board esp32dev

Wokwi needs two files here, next to `platformio.ini`:

- `wokwi.toml` tells Wokwi where the built firmware is
- `diagram.json` the virtual circuit (ESP32, IMU, motor driver...)

Wokwi only simulates the chip and its parts. It does not simulate the
pendulum physics. Physics is tested in `sim/`.
