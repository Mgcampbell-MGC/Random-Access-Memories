#!/usr/bin/env bash
# HOLOFOTE · construir.sh — rebuild the whole sound package with one command:
#   bash _build/sound/construir.sh
# 1 fetch + verify the licensed sources (SHA-256) · 2 own TTS voices for the crowd (Kokoro, local)
# 3 SFX library + sonic identity · 4 music · 5 film beds · 6 verification PNGs
set -euo pipefail
cd "$(dirname "$0")"
PY=/home/user/venvs/web/bin/python
KPY=/home/user/venvs/kokoro/bin/python
$PY -I fetch_sources.py
$KPY -I walla_tts.py
$PY -I musica.py
$PY -I sfx.py
$PY -I filmes.py
$PY -I verificacao.py
echo "pronto: 04_FILMES/som/"
