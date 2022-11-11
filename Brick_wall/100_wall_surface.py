from compas.artists import Artist
from compas.geometry import NurbsCurve, Point

import random


# =============================================================================
# Heights
# =============================================================================



# =============================================================================
# Curve's control points
# =============================================================================

curve_count = 3
max_height = 5
CP_count = 4 # can't be less than 3
y_offset = 1
control_points = []

# create a 3 step range
heights = [max_height * i / (curve_count - 1) for i in range(curve_count)]

x = [random.random() for i in range(CP_count - 2)]
x_coord = [0, *sorted(x), 1]

for i in range(curve_count):
    heights[i] = round(heights[i], 2)

    # create a list of y coordinates
    y = [random.uniform(-y_offset, y_offset) for i in range(CP_count - 2)]
    y_coord = [0, *y, 0]

    # create a list of z coordinates
    z_coord = [heights[i] for _ in range(CP_count)]

    # create a list of control points
    control_points.append([Point(x_coord[i], y_coord[i], z_coord[i]) for i in range(CP_count)])

print("control_points: ", control_points)

for points in control_points:
    print(points)



# =============================================================================
# Curve
# =============================================================================

points = [
    Point(0, 0, 0),
    Point(2, 2, 0),
    Point(4, -4, 0),
    Point(6, 0, 0),
]

curve = NurbsCurve.from_points(points)

# =============================================================================
# Viz
# =============================================================================

from_rhino = False

if from_rhino:
    Artist.clear()

else:
    from compas_view2.app import App

    viewer = App()
    viewer.show()