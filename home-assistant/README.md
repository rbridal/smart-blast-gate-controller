# Home Assistant side

HA owns **intent**; the ESP owns **making the valves match it** (see `docs/decisions/0006`).

| Entity | Kind | Role |
|---|---|---|
| `sensor.shop_cnc_spindle_monitor_*` | Shelly EM Gen3 (CT on spindle circuit, `em1:0`) | Raw spindle power/current |
| `binary_sensor.shop_cnc_spindle_running` | Template helper (UI) | Spindle running, derived from the Shelly EM |
| `input_boolean.dust_collection_cnc_override` | Helper | Manual override (e.g. warm-up / pencil-in-collet); only valid while spindle runs |
| `binary_sensor.dust_collection_cnc_desired` | Template helper (UI) | Spindle running AND NOT override (per design notes; template body not exported) |
| `binary_sensor.dust_collection_shop_vac_requested` | Template helper (UI) | Any gate requesting suction (template body not exported) |
| `button.dust_collection_hose_on/off/toggle`, `button.dust_collection_cnc_on/off` | Template buttons | Used by the round display and physical buttons |
| `switch.smart_blast_gate_cnc_blast_gate` / `..._hose_blast_gate` | ESPHome | **Desired** gate state only |
| `text_sensor` CNC/Hose actual, `binary_sensor` aligned / align fault | ESPHome | Physical truth — use these for "is it really open" |
| `switch.shop_vacuum_switch` | YoLink Outlet | Shop vac power |

`automations.yaml` is the live export (2026-10-14). The template-helper bodies for
`dust_collection_cnc_desired`, `dust_collection_shop_vac_requested` and
`shop_cnc_spindle_running` (threshold) were not exported — **TODO**.
