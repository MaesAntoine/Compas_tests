from compas.artists import Artist
from compas.geometry import NurbsCurve, Point, Plane, Polyline, intersection_polyline_plane

from BW_000_utils import frange

import random
import math



# =============================================================================
# Brick and wall dimensions
# =============================================================================

brick_width = 0.24
brick_height = 0.12
brick_depth = 0.18
cement_thickness = 0.01

curve_count = 3
wall_height = 2
wall_length = 5
CP_count = 4 # can't be less than 3
y_offset = 1


# =============================================================================
# Curve's control points
# =============================================================================

control_points = []

# create a 3 step range
heights = [wall_height * i / (curve_count - 1) for i in range(curve_count)]

# create a list of x_coordinates that are equally spaced from 0 to wall_length with CP_count steps
x_coord = [wall_length * i / (CP_count - 1) for i in range(CP_count)]


for i in range(curve_count):
    heights[i] = round(heights[i], 2)

    # create a list of y coordinates
    y = [random.uniform(-y_offset, y_offset) for i in range(CP_count - 2)]
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

# example of points evaluated at every distance
single_curve = curves[0]
curve_length = single_curve.length()

# floor value of curve length / brick width
divide_value = math.floor(curve_length / brick_width) - 1 # hardcoded value for margin
precise_value = curve_length / brick_width

# compute margins
margin = (precise_value - divide_value) / divide_value

parameters, new_points = single_curve.divide_by_count(divide_value, return_points=True)

# parameters = [i / (n - 1) for i in range(n)]
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
# Points for brick positions
# =============================================================================

step = brick_height + cement_thickness
number_of_horizontal_curves = math.floor(wall_height / (step))
z_values = list(frange(0, step * number_of_horizontal_curves, step, decimals=2))


# create planes for each z value
planes = [Plane(Point(0, 0, z), [0, 0, 1]) for z in z_values]

# intersect each vertical curve with each plane
brick_points = [[] for _ in range(len(vertical_curves))]
vertical_polylines = [curve.to_polyline() for curve in vertical_curves]


for poly_idx, poly in enumerate(vertical_polylines):
    for plane in planes:
        points = intersection_polyline_plane(poly, plane)
        brick_points[poly_idx].append(Point(*points[0]))



# =============================================================================
# Orient planes on each brick point
# =============================================================================

brick_planes = []

# =============================================================================
# Construct bricks on each plane
# =============================================================================

bricks = []

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

    for points in brick_points:
        for point in points:
            viewer.add(point)
    viewer.show()