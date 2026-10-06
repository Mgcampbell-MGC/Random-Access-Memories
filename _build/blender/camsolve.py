"""Solve a camera so the glass lands on exact pixels (platform §E.1: "distance solved for 883 px").

    from camsolve import solve
    cam = solve(lens=85, height_mm=160, tilt_deg=-5, glass_h_mm=88, top_px=610, glass_px=883, res=(1080, 1920),
                yaw_deg=0, x_px=540, target=(0, 0, 0))

The glass's FRONT silhouette edge (y = -R) at z = 0 and z = glass_h is projected; the camera keeps its height and
tilt, its distance is solved for the pixel height, then shift_y (and shift_x) put the top edge at top_px and the axis
at x_px. Returns the camera object. Works with any object at `target` (its base centre).
"""
import math
import bpy
from mathutils import Vector, Euler
from bpy_extras.object_utils import world_to_camera_view


def _px(cam, p, res):
    sc = bpy.context.scene
    co = world_to_camera_view(sc, cam, Vector(p))
    return co.x * res[0], (1 - co.y) * res[1]


def solve(lens, height_mm, tilt_deg, glass_h_mm, top_px, glass_px, res, yaw_deg=0.0, x_px=None, target=(0, 0, 0),
          r_mm=38.0, sensor_mm=36.0):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = res
    cam = sc.camera
    if cam is None:
        bpy.ops.object.camera_add()
        cam = bpy.context.object
        sc.camera = cam
    cam.data.lens = lens
    cam.data.sensor_fit = 'AUTO'
    cam.data.sensor_width = sensor_mm
    cam.data.clip_start = 0.005
    tx, ty, tz = target
    yaw = math.radians(yaw_deg)
    top = (tx - r_mm * 1e-3 * math.sin(yaw) * 0, ty - r_mm * 1e-3, tz + glass_h_mm * 1e-3)
    bot = (tx, ty - r_mm * 1e-3, tz)
    lo, hi = 0.05, 20.0
    for _ in range(60):
        d = (lo + hi) / 2
        cam.location = (tx + d * math.sin(yaw), ty - d * math.cos(yaw), tz + height_mm * 1e-3)
        cam.rotation_euler = Euler((math.radians(90 + tilt_deg), 0, yaw), 'XYZ')
        cam.data.shift_x = cam.data.shift_y = 0
        bpy.context.view_layer.update()
        h = _px(cam, bot, res)[1] - _px(cam, top, res)[1]
        if h > glass_px:
            lo = d
        else:
            hi = d
    # shift so the top lands on top_px and the axis on x_px (shift is in units of the larger sensor dimension)
    big = max(res)
    for _ in range(4):
        bpy.context.view_layer.update()
        y = _px(cam, top, res)[1]
        cam.data.shift_y -= (y - top_px) / big     # +shift_y raises the frustum: content moves down
        if x_px is not None:
            x = _px(cam, (tx, ty, tz + glass_h_mm * 0.5e-3), res)[0]
            cam.data.shift_x += (x - x_px) / big
    bpy.context.view_layer.update()
    return cam


def report(cam, res, glass_h_mm=88, target=(0, 0, 0), r_mm=38.0):
    tx, ty, tz = target
    t = _px(cam, (tx, ty - r_mm * 1e-3, tz + glass_h_mm * 1e-3), res)
    b = _px(cam, (tx, ty - r_mm * 1e-3, tz), res)
    return dict(top_y=round(t[1], 1), base_y=round(b[1], 1), glass_px=round(b[1] - t[1], 1), axis_x=round(t[0], 1),
                distance_m=round((cam.location - Vector(target)).length, 4), shift=(round(cam.data.shift_x, 4),
                                                                                     round(cam.data.shift_y, 4)))
