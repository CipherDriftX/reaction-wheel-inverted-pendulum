# Mathematics behind the motion

## Arm
### 0.00389 x arm_speedup = 0.259 x sin(lean) - motor_push

Why this shape: the same Newton law, now for the arm swinging on the pivot. Two things turn it: gravity (+) and the wheel's kick back (−). It's like jumping off a skateboard: you push it one way and you go the other way.
Why sin(lean): gravity only turns the arm by the sideways part of the lean. Straight up gives sin = 0, so no turning. Fully sideways gives sin = 1, the most turning.
Why 0.00389: the same mass × distance² idea, about the pivot:

| Piece | Mass × distance² | Result |
|---|---|---|
| Arm + motor | 0.182 kg × 0.0986 m × 0.0986 m | 0.00177 |
| Wheel | 0.056 kg × 0.15 m × 0.15 m | 0.00126 |
| Arm is long, not a dot | its extra spread | 0.00086 |
| **Total** | | **0.00389** |

Why 0.259: gravity's turning power = mass × 9.81 × height of the centre above the pivot:

| Piece | Calculation | Result |
|---|---|---|
| Arm + motor | 0.182 × 9.81 × 0.0986 | 0.176 |
| Wheel | 0.056 × 9.81 × 0.15 | 0.082 |
| **Total** | | **0.259** |

---

## Wheel
### 0.000146 x (arm_speedup + wheel_speedup) = motor_push

Why this shape: Newton's law for spinning things is push = spin heaviness × speedup. The wheel rides on the arm, so its real spin is the arm's turn plus its own spin.
Why 0.000146: spin heaviness = mass × (distance from centre)². Most of the wheel's mass is the rim, about 48 g sitting about 5.4 cm out. So 0.048 × 0.054 × 0.054 ≈ 0.00014. The spokes and hub add a little, which gives 0.000146.

---

## Arm, small lean
### arm_speedup = 66.6 x lean - 257 x motor_push

Why: for small angles, sin(lean) ≈ lean (sin 5° = 0.0872, and 5° = 0.0873 rad, almost the same). Then divide equation 2 by 0.00389.
66.6 = 0.259 / 0.00389
257 = 1 / 0.00389

---

## Wheel speedup
### wheel_speedup = 7100 x motor_push - 66.6 x lean

Why: take equation 1, move the arm part to the other side, then put equation 3 in.
7100 = 1/0.000146 + 1/0.00389 = 6842 + 257

---

## Swing time
### 2 x 3.14 x sqrt(0.00389 / 0.259) = 0.77 s

Why: this is the normal pendulum clock formula. A swing is slower when it's harder to swing (0.00389) and faster when gravity pulls harder (0.259).