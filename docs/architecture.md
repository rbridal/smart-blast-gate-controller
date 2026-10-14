# Architecture

```
Shelly EM (CT) ─► HA: spindle_running ─┐
Override (display tap / helper) ───────┼─► cnc_desired ─► switch.*_cnc_blast_gate (DESIRED)
Hose button (webhook) / display ───────┘                         │  ESPHome API
                                                                  ▼
                       ESP32: servo write ─► valve ─► reeds ─► actual text_sensor
                                ▲                                  │
                                └──── alignment supervisor (500 ms)┘
HA: any gate requested ─► shop_vac_requested ─► YoLink outlet (vac)
```

## Desired vs actual
- **Desired** = the ESPHome template switches *CNC Blast Gate* / *Hose Blast Gate*.
  Command only — reeds never write back into them (that "reed sync" was removed
  2026-09-22; it made HA's intent flap whenever a valve stalled).
- **Actual** (`text_sensor`, 250 ms), from `cnc-bg-p1.yaml`:

| Condition | actual |
|---|---|
| a motion script is running (`motion_busy_*`) | `moving` |
| closed reed ON and open reed ON | `fault` (impossible → wiring/magnet problem) |
| closed only | `closed` |
| open only | `open` |
| neither | `unknown` (mid-travel / stalled / lost) |

- **Aligned** = (desired ON & actual `open`) or (desired OFF & actual `closed`).

## Supervisor (`cnc-bg-p3b.yaml`, 500 ms interval, per gate)
Runs only when *Alignment correction* is ON, no fault is latched, and the gate isn't moving.
1. Wait out **Align grace** (default 4 s) after any commanded move and **Align cooldown** (5 s) after any correction.
2. Aligned → reset retries; set detach policy (hold if open, detach after *Closed detach time* if closed).
3. `moving` → wait. `fault` → latch align fault.
4. Misaligned/unknown for **Align debounce** (1.5 s) → retry #n; if n > **Align max retries** (3) → latch fault. *Clear align fault* button resets.

All timings are HA `number` entities with `restore_value` (no recompile).

### Recovery moves
| actual | desired | move |
|---|---|---|
| `open` / `closed` wrong | any | drive to desired |
| `unknown` | ON (open) | close, then open |
| `unknown` | OFF (closed) | **open, then close** (chosen 2026-09-22 for simplicity) |

**Alternative kept on file:** for unknown + desired-off, *slam closed first; only if
still not closed, do open→close*. Fewer moves in the common case; switch to it if
open-then-close proves annoying (e.g. a puff of suction to the wrong branch).

## Other behaviour
- **Detach:** hold PWM while open (suction torque can back-drive an unpowered MG996R);
  detach after *Closed detach time* (1.5 s; 0 = hold) when closed — the closed stop carries the load and the servo stays cool/quiet.
- **Last-gate close delay** (3 s, 0–15): when closing the only open gate, wait so the vac coasts down before seating against suction. If another gate is still open, close immediately.
- **Boot:** wait 2 s for 5 V, apply closed-detach, reseat both closed.
- **Limits:** CNC open 45 / closed −69, Hose open 69 / closed −42 (servo %, defaults in YAML; live values live in NVS). Jog numbers for calibration.
