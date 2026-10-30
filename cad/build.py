"""Reaction wheel inverted pendulum: parametric CAD.

Run:  .venv/bin/python cad/build.py
Out:  cad/step/assembly.step   (import into Onshape: Create > Import)
      cad/step/<part>.step     (one file per part)
      cad/stl/<part>.stl       (3D printing)

Units: mm. Axes: X = left/right, Y = front(-)/back(+), Z = up.
The pivot shaft runs along Y. The pendulum swings in the XZ plane,
in front of the upright plate (y < 0), above the base box.
"""

import math
from pathlib import Path

import cadquery as cq

# ---------------------------------------------------------------------------
# Parameters. Change these, rerun, re-import.
# ---------------------------------------------------------------------------

L = 150.0               # pivot axis -> wheel axis (the pendulum length)
WHEEL_OD = 120.0        # reaction wheel outer diameter
WHEEL_T = 10.0          # wheel thickness (along Y)
RIM_W = 12.0            # radial width of the heavy rim
WEIGHT_HOLES = 12       # M4 holes in rim: add bolts + nuts to tune inertia
CLEAR = 20.0            # gap between hanging wheel and box top

# Nidec 24H. UNVERIFIED: sources disagree. Measure with calipers before printing.
MOTOR_D = 42.0          # body diameter (listing: 41.9)
MOTOR_H = 34.0          # body length
MOTOR_SHAFT_D = 6.0     # listing says 6 mm with D-flat; one drawing says 4 mm
MOTOR_SHAFT_FLAT = 4.5  # D-flat across-flats size; set to None for round shaft
MOTOR_SLOT_R = (14.0, 23.0)  # M3 slots span this radius range, so any bolt circle fits

# Pivot: 8 mm steel rod in two 608 bearings (8 x 22 x 7).
SHAFT_D = 8.0
BEARING_OD = 22.0
BEARING_W = 7.0

# Base box (holds ESP32, power, ballast).
BOX_X, BOX_Y, BOX_Z = 200.0, 160.0, 60.0
WALL = 4.0

# Upright plate.
UP_W = 120.0
UP_T = 8.0
BOSS_T = 16.0           # bearing boss depth = 2 bearings + 2 mm lip
FOOT_D = 40.0           # foot depth on box top

# Derived. Pivot height above box top: hanging wheel must clear the box.
PIVOT_Z = L + WHEEL_OD / 2 + CLEAR
UP_H = PIVOT_Z + 25.0

# Y stack, from the upright front face (y=0) toward the viewer (-y).
HUB_Y0, HUB_Y1 = -3.0, -46.0     # pivot hub on shaft; leaves room for motor body behind arm
ARM_T = 4.0                      # arm plate thickness at motor mount
ARM_Y0 = HUB_Y1 + ARM_T          # arm plate back face (-42)
ARM_W = 24.0
RIB_D = 10.0                     # stiffening rib behind arm plate
WHEEL_GAP = 1.5                  # arm front face -> wheel back face

STEP_DIR = Path(__file__).resolve().parent / "step"
STL_DIR = Path(__file__).resolve().parent / "stl"


# ---------------------------------------------------------------------------
# Parts
# ---------------------------------------------------------------------------

def y_cyl(d, y0, y1, x=0.0, z=0.0):
    """Cylinder along Y from y0 to y1."""
    lo, hi = min(y0, y1), max(y0, y1)
    return (cq.Workplane("XZ", origin=(x, hi, z)).circle(d / 2).extrude(hi - lo))


def base_box():
    # Open-bottom tray: top plate + walls. Print upside down, no supports.
    # Back edge sits under the upright, front reaches under the pendulum.
    y_back = UP_T / 2 + FOOT_D / 2 + 6.0
    outer = cq.Workplane("XY").box(BOX_X, BOX_Y, BOX_Z, centered=(True, False, False))
    inner = cq.Workplane("XY").box(BOX_X - 2 * WALL, BOX_Y - 2 * WALL, BOX_Z - WALL,
                                   centered=(True, False, False)).translate((0, WALL, 0))
    box = outer.cut(inner).translate((0, y_back - BOX_Y, -BOX_Z))
    # 4 x M4 holes for the upright foot.
    fy = UP_T / 2
    box = box.cut(cq.Workplane("XY").pushPoints([(x, fy + dy) for x in (-45, 45) for dy in (-12, 12)])
                  .circle(2.2).extrude(-WALL - 1))
    # Cable hole just in front of the foot.
    box = box.cut(cq.Workplane("XY").center(0, fy - FOOT_D / 2 - 10).rect(30, 12).extrude(-WALL - 1))
    return box


def upright():
    plate = cq.Workplane("XY").box(UP_W, UP_T, UP_H, centered=(True, False, False))
    foot = (cq.Workplane("XY").box(UP_W, FOOT_D, 6.0, centered=(True, True, False))
            .translate((0, UP_T / 2, 0)))
    boss = y_cyl(BEARING_OD + 12, 0, BOSS_T, z=PIVOT_Z)
    # Gussets front and back so the tall plate does not flex when the wheel kicks.
    g = FOOT_D / 2 - UP_T / 2
    back = cq.Workplane("YZ").polyline([(UP_T, 6), (UP_T + g, 6), (UP_T, 70)]).close().extrude(6)
    front = cq.Workplane("YZ").polyline([(0, 6), (-g, 6), (0, 70)]).close().extrude(6)
    body = plate.union(foot).union(boss)
    for x in (-UP_W / 2, UP_W / 2 - 6):
        body = body.union(back.translate((x, 0, 0))).union(front.translate((x, 0, 0)))
    # Bearing seats from both sides, 2 mm lip between them.
    body = body.cut(y_cyl(BEARING_OD + 0.1, -1, BEARING_W, z=PIVOT_Z))
    body = body.cut(y_cyl(BEARING_OD + 0.1, BOSS_T - BEARING_W, BOSS_T + 1, z=PIVOT_Z))
    body = body.cut(y_cyl(SHAFT_D + 4, -1, BOSS_T + 1, z=PIVOT_Z))
    # Foot holes (match base box).
    body = body.cut(cq.Workplane("XY").pushPoints([(x, UP_T / 2 + dy) for x in (-45, 45) for dy in (-12, 12)])
                    .circle(2.2).extrude(7))
    # M3 pilot holes for the sensor bracket legs.
    body = body.cut(cq.Workplane("XZ", origin=(0, UP_T + 1, PIVOT_Z))
                    .pushPoints([(-24, 10), (-24, -10), (24, 10), (24, -10)]).circle(1.25).extrude(UP_T + 2))
    return body


def sensor_bracket():
    # Holds the AS5600 board ~2 mm behind the magnet glued on the shaft end.
    # Slots fit most AS5600 breakout boards. Check against yours.
    y0 = BOSS_T + 1.0 + 2.5 + 2.0        # shaft end + magnet + air gap
    t = 3.0
    plate = cq.Workplane("XZ", origin=(0, y0 + t, PIVOT_Z)).rect(56, 36).extrude(t)
    plate = plate.cut(cq.Workplane("XZ", origin=(0, y0 + t + 1, PIVOT_Z))
                      .pushPoints([(-11, 0), (11, 0)]).slot2D(10, 3.4, 90).extrude(t + 2))
    legs = (cq.Workplane("XZ", origin=(0, y0 + t, PIVOT_Z)).pushPoints([(-24, 0), (24, 0)])
            .rect(8, 36).extrude(y0 + t - UP_T))
    holes = (cq.Workplane("XZ", origin=(0, y0 + t + 1, PIVOT_Z))
             .pushPoints([(-24, 10), (-24, -10), (24, 10), (24, -10)])
             .circle(1.7).extrude(y0 + t - UP_T + 2))
    return plate.union(legs).cut(holes)


def arm():
    # Hub clamps the 8 mm shaft (M3 set screw). Plate carries the motor at z = L.
    hub = y_cyl(26, HUB_Y0, HUB_Y1, z=PIVOT_Z)
    plate = (cq.Workplane("XZ", origin=(0, ARM_Y0, PIVOT_Z))
             .center(0, L / 2 - 6).rect(ARM_W, L + 12).extrude(ARM_T))
    mount = cq.Workplane("XZ", origin=(0, ARM_Y0, PIVOT_Z + L)).circle(MOTOR_D / 2 + 6).extrude(ARM_T)
    rib = (cq.Workplane("XZ", origin=(0, ARM_Y0 + RIB_D, PIVOT_Z))
           .center(0, (L - MOTOR_D / 2 - 4) / 2).rect(6, L - MOTOR_D / 2 - 4).extrude(RIB_D))
    body = hub.union(plate).union(mount).union(rib)
    body = body.cut(y_cyl(SHAFT_D + 0.2, HUB_Y0 + 1, HUB_Y1 - 1, z=PIVOT_Z))
    # M3 set screws into the shaft, two along the hub.
    for yy in (HUB_Y0 - 10, HUB_Y1 + 10):
        body = body.cut(cq.Workplane("XY", origin=(0, yy, PIVOT_Z)).circle(1.35).extrude(-20))
    # Motor shaft clearance + 3 radial M3 slots (fit any bolt circle in MOTOR_SLOT_R).
    body = body.cut(y_cyl(14, ARM_Y0 + 1, HUB_Y1 - 1, z=PIVOT_Z + L))
    r0, r1 = MOTOR_SLOT_R
    for ang in (90, 210, 330):
        slot = (cq.Workplane("XZ", origin=(0, ARM_Y0 + 1, PIVOT_Z + L))
                .center((r0 + r1) / 2, 0).slot2D(r1 - r0 + 3.4, 3.4, 0).extrude(ARM_T + 2)
                .rotate((0, ARM_Y0, PIVOT_Z + L), (0, ARM_Y0 + 1, PIVOT_Z + L), ang))
        body = body.cut(slot)
    return body


def motor():
    # Placeholder for the Nidec 24H: body behind the arm, shaft through it.
    body = y_cyl(MOTOR_D, ARM_Y0, ARM_Y0 + MOTOR_H, z=PIVOT_Z + L)
    shaft = y_cyl(MOTOR_SHAFT_D, ARM_Y0, HUB_Y1 - WHEEL_GAP - WHEEL_T, z=PIVOT_Z + L)
    return body.union(shaft)


def wheel():
    y_back = HUB_Y1 - WHEEL_GAP
    y_front = y_back - WHEEL_T
    z = PIVOT_Z + L
    r = WHEEL_OD / 2
    rim = y_cyl(WHEEL_OD, y_back, y_front, z=z).cut(y_cyl(WHEEL_OD - 2 * RIM_W, y_back + 1, y_front - 1, z=z))
    web_t = 3.0
    spoke = (cq.Workplane("XZ", origin=(0, y_back, z)).center(0, (r - RIM_W / 2) / 2)
             .rect(6, r - RIM_W / 2).extrude(web_t))
    spokes = spoke
    for i in range(1, 5):
        spokes = spokes.union(spoke.rotate((0, y_back, z), (0, y_back - 1, z), i * 72))
    hub = y_cyl(20, y_back, y_front, z=z)
    body = rim.union(spokes).union(hub)
    # Motor shaft bore (D-flat if set).
    bore = cq.Workplane("XZ", origin=(0, y_back + 1, z)).circle(MOTOR_SHAFT_D / 2 + 0.05).extrude(WHEEL_T + 2)
    if MOTOR_SHAFT_FLAT:
        r = MOTOR_SHAFT_D / 2
        flat = (cq.Workplane("XZ", origin=(0, y_back + 1, z)).center(MOTOR_SHAFT_FLAT - r + MOTOR_SHAFT_D / 2, 0)
                .rect(MOTOR_SHAFT_D, MOTOR_SHAFT_D + 2).extrude(WHEEL_T + 2))
        bore = bore.cut(flat)
    body = body.cut(bore)
    r = WHEEL_OD / 2
    # Set screw into the shaft.
    body = body.cut(cq.Workplane("XY", origin=(0, (y_back + y_front) / 2, z)).circle(1.35).extrude(12))
    # M4 weight holes around the rim.
    pts = []
    for i in range(WEIGHT_HOLES):
        a = 2 * math.pi * (i + 0.5) / WEIGHT_HOLES
        pts.append(((r - RIM_W / 2) * math.cos(a), (r - RIM_W / 2) * math.sin(a)))
    body = body.cut(cq.Workplane("XZ", origin=(0, y_back + 1, z)).pushPoints(pts).circle(2.2).extrude(WHEEL_T + 2))
    return body


def pivot_shaft():
    return y_cyl(SHAFT_D, HUB_Y1 + 1, BOSS_T + 1, z=PIVOT_Z)


def bearings():
    one = lambda y0: y_cyl(BEARING_OD, y0, y0 + BEARING_W, z=PIVOT_Z).cut(
        y_cyl(SHAFT_D, y0 - 1, y0 + BEARING_W + 1, z=PIVOT_Z))
    return one(0).union(one(BOSS_T - BEARING_W))


def magnet():
    return y_cyl(6, BOSS_T + 1, BOSS_T + 3.5, z=PIVOT_Z)


# ---------------------------------------------------------------------------
# Build + export
# ---------------------------------------------------------------------------

PRINTED = {
    "base_box": (base_box, (0.6, 0.6, 0.6)),
    "upright": (upright, (0.27, 0.51, 0.71)),
    "arm": (arm, (1.0, 0.55, 0.0)),
    "wheel": (wheel, (0.85, 0.1, 0.1)),
    "sensor_bracket": (sensor_bracket, (0.1, 0.6, 0.2)),
}
BOUGHT = {
    "motor_nidec_24h": (motor, (0.1, 0.1, 0.1)),
    "pivot_shaft_8mm": (pivot_shaft, (0.8, 0.8, 0.82)),
    "bearings_608": (bearings, (0.8, 0.8, 0.82)),
    "magnet_6x2.5": (magnet, (0.5, 0.2, 0.7)),
}


def main():
    STEP_DIR.mkdir(exist_ok=True)
    STL_DIR.mkdir(exist_ok=True)
    asm = cq.Assembly(name="reaction_wheel_pendulum")
    for name, (fn, color) in {**PRINTED, **BOUGHT}.items():
        part = fn()
        asm.add(part, name=name, color=cq.Color(*color))
        cq.exporters.export(part, str(STEP_DIR / f"{name}.step"))
        if name in PRINTED:
            cq.exporters.export(part, str(STL_DIR / f"{name}.stl"), tolerance=0.05, angularTolerance=0.1)
        bb = part.val().BoundingBox()
        vol_cm3 = part.val().Volume() / 1000
        print(f"{name:18s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:6.1f} mm   "
              f"solid PLA ~{vol_cm3 * 1.24:6.1f} g" if name in PRINTED else
              f"{name:18s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:6.1f} mm")
    asm.save(str(STEP_DIR / "assembly.step"))
    print(f"\npivot height above box top: {PIVOT_Z:.0f} mm, upright height: {UP_H:.0f} mm")
    print(f"wrote {STEP_DIR / 'assembly.step'}")


if __name__ == "__main__":
    main()
