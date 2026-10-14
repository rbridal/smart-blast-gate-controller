# Smart Blast Gate Controller

Automatic dust collection for a small shop: two servo-driven 2½″ ball valves
(Shapeoko CNC + spot hose) on an ESP32 running ESPHome, reed switches at both
end stops of each valve, a round touch display for status/override, and Home
Assistant deciding *when* suction is wanted (spindle current via Shelly EM,
buttons, display taps) and switching the shop vac.

> 📷 _Photo placeholder — current install (enclosure not finished yet). Add `docs/img/install.jpg`._

**Secrets:** every key/password/SSID here is a `!secret` reference. Bring your own `secrets.yaml`.

## How it works (one paragraph)
HA flips a **desired** switch per gate. The ESP drives the servo to a soft %
target against a flat printed hard stop, and derives an **actual** state from
the two reeds (`closed | open | moving | unknown | fault`). A 500 ms
**alignment supervisor** on the ESP compares desired vs actual and, after a
grace + debounce window, re-drives a misaligned gate with cooldown between
retries, latching a fault after N retries. Open gates hold PWM; closed gates
detach. Closing the last open gate waits for the vac to coast down. Details:
[`docs/architecture.md`](docs/architecture.md), the *why*: [`docs/decisions/`](docs/decisions/).

## Repo map
| Path | What |
|---|---|
| `esphome/cnc-blast-gate.yaml` + `cnc-bg-p*.yaml` | Production dual-gate controller (thin main + packages, split to fit Builder upload size) |
| `esphome/prototype/` | Single-gate bench prototype (same supervisor) |
| `esphome/displays/` | ESP32-S3 round AMOLED (CO5300) status/override displays |
| `home-assistant/` | Live automation export + entity map |
| `docs/architecture.md` | Supervisor, states, timings, boot |
| `docs/wiring.md` | Pins, reeds, power, free GPIOs |
| `docs/decisions/` | ADRs — why each design choice was made |
| `docs/timeline.md` | Iteration history |
| `hardware/print/` | 3D print files (Rob's current versions — pending) |
| `hardware/lightburn/` | Laser faceplate / label / reed-plate SVGs |
| `hardware/legacy-blast-gate-c/` | Earlier "Blast Gate C" no-reed config + horn-flag reed mounts (superseded) |

## Bill of materials (as known)
| Qty | Part | Notes |
|---|---|---|
| 1 | ESP32 DevKit, 38-pin (`esp32dev`) | Controller |
| 2 | MG996R servo | **Metal 25T horns + threadlocker** (stock horns stripped) |
| 2 | 2½″ printed ball valve (case/rotator/bearings) | Translucent PETG; TPU flange seals |
| 4 | RC-34A-style reed switch | One per end stop, set in the printed stops |
| 2+ | Small neodymium magnets | On the 60 mm double horn |
| 2 | 5 V supplies (servo / logic) | Common GND — see ADR 0007. Ratings: **unknown** |
| 1 | Shelly EM Gen3 + CT clamp | Spindle-running sense |
| 1 | YoLink smart outlet | Shop vac |
| — | Woodcraft 2½″ hose + WoodRiver Y fitting | Ducting |
| 1 | ESP32-S3 1.8–2.16″ round AMOLED (CO5300) | Display / override (exact board: see display YAML) |

## Flashing
ESPHome Builder → device → Validate → Install. Rollback = previous YAML in git.
