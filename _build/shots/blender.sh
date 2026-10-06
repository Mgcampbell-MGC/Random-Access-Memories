#!/bin/bash
# Run Blender (bpy) under the kit's render lock, so only one render uses the 4 cores at a time.
# Usage: _build/shots/blender.sh script.py -- args...
exec flock /tmp/holofote_render.lock /home/user/venvs/blender/bin/python "$@"
