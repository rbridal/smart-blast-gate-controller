# 0003 — Flat printed hard stops + soft % targets (not stall-to-limit)

**Context.** Driving the servo past the end and letting it stall heats it, draws current (brownouts) and wears gears.

**Decision.** Print flat hard stops at each end; command a calibrated % just short of/at the stop. Limits are HA numbers per gate (restore in NVS), with jog for calibration.

**Consequences.** Needs calibration per valve; drift detected by reeds.
