#!/bin/bash
# Runs the 3D jobs listed in fila.txt one at a time, each through the kit's render lock (blender.sh), so the
# director and the other teams interleave between jobs. Edit fila.txt while it runs: the next line is read each time.
cd "$(dirname "$0")"
mkdir -p _render/logs
while true; do
  job=$(head -n1 fila.txt 2>/dev/null)
  [ -z "$job" ] && break
  sed -i '1d' fila.txt
  tag=$(echo "$job" | tr ' ,' '__')
  echo "$(date +%H:%M:%S) START $job" >> _render/logs/fila.log
  ../shots/blender.sh f15_3d.py -- $job > "_render/logs/$tag.log" 2>&1
  echo "$(date +%H:%M:%S) END $? $job" >> _render/logs/fila.log
done
echo "$(date +%H:%M:%S) FILA VAZIA" >> _render/logs/fila.log
