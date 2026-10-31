#!/bin/sh
set -e
esphome compile /config/esphome/smart-blast-gate-display.yaml > /config/esphome/.tough-compile.log 2>&1
echo EXIT:$? >> /config/esphome/.tough-compile.log
