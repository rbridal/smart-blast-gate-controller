# 0005 — Hold PWM while open; detach only when closed

**Context.** Suction can back-drive an unpowered servo out of the open position; while closed, the stop and vacuum hold the valve seated.

**Decision.** Auto-detach time 0 while open; after closing, detach after *Closed detach time* (default 1.5 s).

**Consequences.** Servo hums/draws while open; cool and quiet while closed.
