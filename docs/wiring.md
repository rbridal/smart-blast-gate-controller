# Wiring

## Production controller (`esphome/cnc-blast-gate.yaml`, ESP32 DevKit 38-pin)
| GPIO | Use |
|---|---|
| 18 | CNC servo PWM (LEDC 50 Hz) |
| 19 | Hose servo PWM |
| 21 | CNC reed — closed stop (INPUT_PULLUP, inverted) |
| 22 | CNC reed — open stop |
| 23 | Hose reed — closed stop |
| 25 | Hose reed — open stop |

Reeds: one lead → GND, other → GPIO. Magnet at stop → LOW → binary ON.
Reeds sit in the printed stops behind ~1 mm of plastic; magnets ride on the 60 mm double horn.

## Prototype (`esphome/prototype/`)
Servo GPIO18; reed closed GPIO19; reed open GPIO21.

## Power
Two 5 V supplies — servos on one, ESP logic on the other — with **common GND**
(ADR 0007). Supply ratings, connectors and enclosure layout: **unknown / not documented yet**.
No relays or other outputs exist on the controller today.

## Free GPIOs (for future outputs, e.g. CNC air-blast enable)
Good general outputs not used: **GPIO 4, 13, 16, 17, 26, 27, 32, 33** (16/17 are free on
WROOM; on WROVER/PSRAM modules they're taken). Avoid: 0/2/5/12/15 (strapping),
1/3 (UART0), 6–11 (flash), 34/35/36/39 (input-only). 14 is OK but PWMs at boot.
