# Smart Blast Gate Controller

Public memorial of the dual-valve ESPHome blast gate controller built for a shop dust collection system (CNC + spot hose), integrated with Home Assistant.

**Secrets redacted.** API encryption keys, WiFi, and OTA passwords use `!secret` placeholders. Generate your own.

## Overview

- **Hardware**: ESP32 DevKit (38-pin), dual MG996R servos (GPIO18 CNC, GPIO19 Hose), RC-34A-style reed switches for open/closed stops per valve.
- **Software**: ESPHome with a desired-vs-actual alignment supervisor (grace / debounce / cooldown / max retries). Holds PWM while open; auto-detaches only after close (configurable).
- **Safety**: Last-gate close delay so the shop vac can spin down before seating against suction.
- **HA integration**: Template switches for CNC/Hose gates, numbers for open/closed %, detach time, alignment timings, jog. Binary sensors for aligned/fault. Text sensors for actual state.
- **Displays**: Separate ESP32-S3 round displays for status and manual override (not included in full detail here; see shop-ha ESPHome).
- **Prototype**: Single-valve bench version existed first; production is dual independent valves.

## Alignment Supervisor

Desired state comes only from the HA switches (never overwritten by reeds).
Actual state is derived from reeds + motion busy flags: `closed` | `open` | `moving` | `unknown` | `fault`.
When "Alignment correction" is on, the supervisor corrects mismatches after grace + debounce, with cooldown between retries, and latches a fault after max retries.

Unknown actual + desired open → close then open (to find a stop).
Unknown actual + desired closed → open then closed.

## Home Assistant Side (memorialized from live config)

Key helpers and automations (entity IDs approximate; confirm in your HA):

- `input_boolean.dust_collection_cnc_override` — manual override for pencil-in-collet / warmup.
- `binary_sensor.dust_collection_cnc_desired` — spindle running AND NOT override.
- Vac request is OR of CNC/Hose gates; YoLink outlet for shop vac.
- Automations: Dust Collection CNC, Hose, Vac, CNC Override (clears override on spindle stop; rejects while spindle off).
- Display taps call override toggle.

See project memory for full history of migration from prototype, reed alignment, detach policy, last-gate delay, and display color logic.

## Files

- `esphome/cnc-blast-gate.yaml` — main production config (packages the parts).
- `esphome/cnc-bg-p1.yaml` — outputs, servos, reed binary sensors, actual text sensors.
- `esphome/cnc-bg-p2a.yaml` / `p2b.yaml` — write/seat scripts and correction scripts.
- `esphome/cnc-bg-p3a.yaml` / `p3b.yaml` — template switches, numbers (limits, timings, jog), buttons, and the 500ms supervisor interval.

## Hardware Notes

- Reeds: one lead to GND, other to GPIO with pull-up. Magnet at stop → GPIO low. `inverted: true` so binary ON = at stop.
- Servo pins fixed at 18/19. Reed pins: CNC closed 21 / open 22; Hose closed 23 / open 25.
- Boot: 2s power delay, apply closed detach, seat both closed.

## License

Memorial / educational. Use at your own risk. No warranty.

Built by rbridal for the shop dust collection system.
