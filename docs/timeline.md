# Timeline
Dates America/Denver. Sources: agent work history and config files; gaps marked.

- **≤ 2026-09-06 — "Blast Gate C" (no reeds).** Dual servo ball valves, independent CNC/Hose switches, buttons, calibrate-% numbers. Faceplate SVGs for LightBurn; horn-flag reed mounts printed but unused. Valve parts in translucent PETG, TPU-for-AMS flange seals, 0.20 mm / 4–6 walls / 35–40 % gyroid. HA logic sketched around YoLink CNC power sense + Flics (Carbide Motion has no native link). → `hardware/legacy-blast-gate-c/`
- **September — servo hardening.** MG996R stock horns stripped → metal 25T horns + threadlocker. Moved from stall-to-limit to flat printed hard stops with soft % targets. open%/closed% mapping reworked (historically open→0 %, closed→100 %; now signed −100…100 per gate). _Exact dates unknown._
- **September — reeds in the stops.** Catch magnets removed (interfered with reeds). Reeds embedded in stops (~1 mm gap), magnets on 60 mm double horn. Reeds initially synced back into the HA switch.
- **September — power.** Servo brownouts → dual 5 V supplies, common GND. _Date unknown._
- **Spindle sense** moved from YoLink to **Shelly EM Gen3 + CT**. Override helper + auto-clear automation; round AMOLED display taps.
- **2026-09-21/22 — detach + supervisor.** Closed-only detach (hold PWM while open) refined on prototype, ported to dual controller with reed sync. Intermittent ~45 % stalls → decided on ESP-side desired-vs-actual alignment supervisor; HA switches become desired-only. Pre-align backup kept. Prototype parts reused for the production unit.
- **2026-09-23** — Prototype ported to the same supervisor (single gate).
- **2026-10-14** — Repo exported from chat; restructured to document the design.
