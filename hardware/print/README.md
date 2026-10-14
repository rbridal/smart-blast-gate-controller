# 3D print files

`smart-blast-gate.3mf`: Rob's current Bambu Studio project (added 2026-10-14).

## Objects
| Object | Material | Purpose |
|---|---|---|
| Smart Blast Gate Outside Shell | PLA | Valve case |
| rotator | PLA | Ball-valve rotor |
| flange-seal (×2) | TPU (AMS) | Hose/duct flange seals |
| Servo Mount (4) | PLA | _Unknown, pending Rob_ |
| Servo Mount (5) | PLA | _Unknown, pending Rob_ |
| Servo Mount (13) | PLA | _Unknown, pending Rob_ |
| Servo Mount (15) | PLA | _Unknown, pending Rob_ |
| Servo Mount (21) | PLA | _Unknown, pending Rob_ |
| Servo Mount (26) | PLA | _Unknown, pending Rob_ |

Bearings are printed in PLA. They aren't a separate object in this 3MF, though they may be part of another object.
Servo mounts are PLA.

## Known print settings
- PLA for every part except the flange seals, which are TPU. Translucent PETG was tried first, but the parts were too fragile; PLA turned out much stronger.
- 0.20 mm layers
- 4–6 walls
- 35–40 % gyroid infill

Hard stops are printed flat with the reed inside, leaving about 1 mm of plastic between the reed and the magnet path.

## Servo arm

The rotator and servo mounts are modeled to fit the [MECCANIXITY metal 25T single-arm servo horn](https://www.amazon.com/dp/B0G2CFPKC6) (aluminum, split clamp, 28 mm long, 7.5 mm thick, 3 mm hole) exactly. The design was modified from the original to take this metal arm in place of the stock plastic horn, which stripped.
