# Archived ESPHome display designs

Archived 2026-10-31 (America/Denver) before bringing up the M5Stack Tough as the new **Smart Blast Gate Display**.

| File | Hardware | Role when live | Notes |
|---|---|---|---|
| `smart-blast-gate-display-round-CO5300.yaml` | ESP32-S3 16MB octal PSRAM; Waveshare-style round AMOLED **CO5300 466×466** quad SPI; CST9220 touch; LVGL split CNC/HOSE tap UI | Device name `smart-blast-gate-display` (Shop HA live file was `circle-try-3.yaml`) | Superseded in daily use by Shop CNC Display; offline leftovers may remain in HA |
| `shop-bambu-display.yaml` | PanelLan ZX2D80CE02S / AITRIP 2.8" ESP32-S3; **ST7789V 240×320** octal `mipi_spi`; LEDC backlight; LVGL; **no touch** | Bambu Lab P1S print status / progress / temps / AMS trays via HA sensors | Lived only on Shop HA (copied here for the archive); offline |

Secrets in these YAMLs stay as `!secret` refs — never commit secret values.

Shop CNC Display (`../shop-cnc-display.yaml`) was **not** archived; it stays active until the Tough is online and Rob retires it.

See also Shop HA `/config/esphome/archive/` for dated copies of the same files.
