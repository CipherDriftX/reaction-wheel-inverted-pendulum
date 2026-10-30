# Parts

## Bought

| Part | Note | Price |
|---|---|---|
| Nidec 24H BLDC (built-in driver + encoder) | Reaction wheel motor | |
| 8 mm steel rod, ~65 mm | Pivot shaft | |
| 2 x 608 bearings (8 x 22 x 7) | Pivot | |
| 6 x 2.5 mm diametric magnet | Glued to shaft end, read by AS5600 | |
| AS5600 board | Pendulum angle | |
| ESP32-S3 DevKit | Controller | |
| M3 / M4 screws, nuts | Assembly + rim weights | |
| ~1 kg ballast in the base box | Base must not move | |

## Printed

`base_box`, `upright`, `arm`, `wheel`, `sensor_bracket`. Files in `cad/stl/`.

## Measure before printing

These come from a marketplace listing and one unconfirmed drawing that disagree:

- Nidec 24H body diameter (set 42 mm) and length (34 mm)
- Motor shaft diameter (set 6 mm with 4.5 mm D-flat; one drawing says 4 mm)
- Motor shaft length (needs about 16 mm to pass the arm and fill the wheel hub)
- Motor mounting screws: the arm has radial slots from r = 14 to 23 mm, so most bolt circles fit
- Which side of the motor carries the mounting holes. The model assumes the shaft side bolts to the back of the arm and the body sits behind it.
