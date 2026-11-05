# 0009 — Shelly EM + CT for spindle sense (not YoLink); VFD run relay as a future primary signal

**Context.** Carbide Motion exposes no link to HA, so spindle state has to be sensed electrically. The earlier YoLink power-sense plan was replaced. The VFD's multifunction relay output ("running") was never evaluated at the time, and whether Rob's VFD has a free one is still unverified.

**Decision.** Shelly EM Gen3 with a CT on the spindle circuit feeds the template `binary_sensor.shop_cnc_spindle_running`, with a 2 s debounce in the CNC automation.

**Why (reconstructed, not recorded at the time).** The CT clamps around a wire with no other setup. Using the VFD relay means opening the VFD enclosure (mains and stored DC bus voltage inside), landing wires on its control terminals, and setting a drive parameter. Why Shelly beat YoLink (latency or resolution?) was not recorded.

**Consequences.** The spindle signal lives in HA only and isn't wired to the ESP, so gate opening depends on HA, the Shelly and Wi-Fi, plus a power threshold and debounce.

**Planned revision.** If the VFD's run relay is confirmed free, make it the primary spindle signal: sense it on the controller through a screw-terminal PC817 opto input (GPIO32, see the CNC air blast design). That signal is instant, needs no threshold, and works without HA. One relay input can then drive both the CNC gate and the air blast interlock. The Shelly stays as a cross-check and for power monitoring, and a mismatch between the two flags a wiring or VFD parameter fault. Blocked on: Rob's VFD model, its manual, and whether the relay output is free.
