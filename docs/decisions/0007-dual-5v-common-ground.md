# 0007 — Dual 5 V supplies with common ground

**Context.** Servo inrush/stall current browned out the ESP.

**Decision.** Separate 5 V supply for servos and for logic, grounds tied together (PWM needs a shared reference). Boot waits 2 s for 5 V before seating.

**Consequences.** Ratings undocumented — TODO.
