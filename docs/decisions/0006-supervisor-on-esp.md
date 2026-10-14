# 0006 — Alignment supervisor lives on the ESP; HA switches are desired-only

**Context.** Intermittent ~45 % stalls left valves mid-travel. Reed→switch sync made HA's intent flap and HA automations fight the hardware. Doing the loop in HA adds network latency and fails if HA/Wi-Fi is down.

**Decision.** ESP runs a 500 ms desired-vs-actual supervisor with grace/debounce/cooldown/max-retries and fault latch. HA switches = desired only; HA reads actual/aligned/fault.

**Consequences.** Automations wanting physical truth must use *actual*/*aligned*. Unknown+desired-off = open-then-close (slam-closed-first kept as alternative).
