# 0001 — Hobby servos instead of NEMA17 / 28BYJ-48 steppers

**Context.** A ball valve only needs two positions (quarter turn).

**Decision.** Use MG996R servos. A servo gives absolute position with one PWM pin and no driver board; a NEMA17 needs a driver, more power and homing; a 28BYJ-48 is too weak/slow for a seal under suction and also needs homing.

**Consequences.** Position is open-loop, so end-stop sensing (reeds) is added later. _Rationale partly reconstructed — confirm with Rob._
