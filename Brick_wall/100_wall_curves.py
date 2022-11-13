from compas.artists import Artist
from compas.geometry import NurbsCurve, Point, NurbsSurface

import random




# =============================================================================
# Brick dimensions
# =============================================================================

brick_width = 0.24
brick_height = 0.12
brick_depth = 0.18
cement_thickness = 0.01


# =============================================================================
# Curve's control points
# =============================================================================

curve_count = 3
wall_height = 5
wall_length = 10
CP_count = 4 # can't be less than 3
y_offset = 2
control_points = []


# create a 3 step range
heights = [wall_height * i / (curve_count - 1) for i in range(curve_count)]

# create a list of x_coordinates that are equally spaced from 0 to wall_length with CP_count steps
x_coord = [wall_length * i / (CP_count - 1) for i in range(CP_count)]


for i in range(curve_count):
    heights[i] = round(heights[i], 2)

    # create a list of y coordinates
    y = [random.randrange(-y_offset, y_offset) for i in range(CP_count - 2)]
    y_coord = [0, *y, 0]

    # create a list of z coordinates
    z_coord = [heights[i] for _ in range(CP_count)]

    # create a list of control points
    control_points.append([Point(x_coord[i], y_coord[i], z_coord[i]) for i in range(CP_count)])



# =============================================================================
# Main curves
# =============================================================================

degree = 3
curves = []

for points in control_points:
    curve = NurbsCurve.from_points(points, degree=degree)
    curves.append(curve)


# =============================================================================
# Points for vertical curves
# =============================================================================

# evaluate the curves at n parameter values
n = 10

parameters = [i / (n - 1) for i in range(n)]
eval_points = [[] for _ in range(curve_count)]

for curve_idx, curve in enumerate(curves):
    for t in parameters:
        eval_points[curve_idx].append(curve.point_at(t))

transposed_points = [list(i) for i in zip(*eval_points)]


# =============================================================================
# Vertical curves
# =============================================================================

vertical_curves = []
vertical_degree = 1

for points in transposed_points:
    curve = NurbsCurve.from_points(points, degree=vertical_degree)
    vertical_curves.append(curve)

# =============================================================================
# Viz
# =============================================================================

from_rhino = False

if from_rhino:
    Artist.clear()

else:
    from compas_view2.app import App

    viewer = App()
    for curve in curves:
        viewer.add(curve.to_polyline())
    for curve in vertical_curves:
        viewer.add(curve.to_polyline())


    viewer.show()