# Reed endstop mounts (MG996R)

Print these so the magnet does **not** need to fit under the servo.

## Parts

| File | What |
|------|------|
| `mg996r-horn-flag-magnet.stl` | Arm that bolts onto the stock servo horn; tip holds a **~6 mm** neo disc |
| `reed-bracket-servo-side.stl` | L-ish bracket with reed channel; M3 holes to screw to your servo mount / backplate |
| `reed-bracket-ziptie-pad.stl` | Simpler pad + reed channel if you’d rather zip-tie to the servo body |

## Print (PETG or PLA)

- 0.20 mm, 3–4 walls, 25–40% infill
- Flat on bed as exported (no supports needed for these)
- 1× flag per valve, 1× reed bracket per valve

## Hardware

- **Magnet:** Ø6 × 2 mm neodymium disc (press into tip from the top; lip retains it). Bigger kit magnets won’t fit — use a small disc.
- **Reed:** glass or plastic-case reed from the LBY kit, press into the channel (leads out the open end)
- **Screws:** M2/M3 through flag → existing horn holes; M3 for bracket

## Install

1. Put valve at **CNC open** (calibrate 0%).
2. Mount flag on the horn so the magnet tip points sideways, clear of the servo body.
3. Mount reed bracket so the reed sits next to the magnet **only** at that angle. Rotate bracket / loosen and nudge until HA `Gate reed CNC` flips on at open and off when you leave open.
4. Hot-glue the reed in the channel once the position is right.
5. Wire reed: one lead → `P21` (CNC) or `P22` (hose), other → **GND**.

## Tune

If the magnet never gets close enough, print the flag again scaled **110% in X only**, or shim the bracket toward the horn. If it stays on too long (too sensitive), add 1–2 mm spacing or a bit of tape over the magnet.
