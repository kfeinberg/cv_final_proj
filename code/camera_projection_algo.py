import argparse
import os
from skimage import io
import numpy as np
import helpers

# TODO: Fact check this! this was confusing info to locate
focal_length_thirteen_mini = 23 #focal length in mm
focal_length_xs = 26 #focal length in mm

M1 = helpers.calculate_projection_matrix(focal_length_thirteen_mini, True)
M2 = helpers.calculate_projection_matrix(focal_length_xs, False)

#parameters: 2 consecutive centroids from camera 1, 2 consecutive centroids from camera2
def get_camera_projection_speed(camera1_centroids, camera2_centroid):
    points3d = helpers.matches_to_3d(camera1_centroids, camera2_centroid, M1, M2)
    return helpers.get_speed(points3d)