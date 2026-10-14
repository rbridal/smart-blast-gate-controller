# 0009 — Shelly EM + CT for spindle sense (not YoLink)

**Context.** Carbide Motion exposes no link to HA; spindle state must be sensed electrically. The earlier YoLink power-sense plan was replaced.

**Decision.** Shelly EM Gen3 with CT on the spindle circuit → template `binary_sensor.shop_cnc_spindle_running`; 2 s debounce in the CNC automation.

**Consequences.** Spindle signal lives in HA only — it is not wired to the ESP. _Why Shelly beat YoLink (latency/resolution?) not recorded._
