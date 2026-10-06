#!/bin/bash
# queue: look-dev tests first, then the finals that need no flame, no X and no posters (holds of 6 Oct)
cd "$(dirname "$0")"
./blender.sh campanha.py -- L03 C02 C04 C08 --teste > logs/teste5.log 2>&1
./blender.sh campanha.py -- C10 L00 L01 L02 L04 L06 L07 C05_1x1 C05_9x16 > logs/finais2.log 2>&1
