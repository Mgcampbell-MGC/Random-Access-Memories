#!/bin/bash
# Approved by the coordinator (6 Oct 2026): the flame jobs run OUTSIDE the render lock, pinned to cores 2-3, one at a time.
cd "$(dirname "$0")"
export HF_THREADS=2
for job in "chama palco 0-23 --samples 128" "blecaute --pct 200 --samples 64" "chama blecaute 210-223,228,229 --samples 96"; do
  tag=$(echo "$job" | tr ' ,' '__')
  echo "$(date +%H:%M:%S) START (fora do lock, cpu 2-3) $job" >> _render/logs/fila.log
  taskset -c 2,3 nice -n 3 /home/user/venvs/blender/bin/python f15_3d.py -- $job > "_render/logs/$tag.log" 2>&1
  echo "$(date +%H:%M:%S) END $? (fora do lock) $job" >> _render/logs/fila.log
done
