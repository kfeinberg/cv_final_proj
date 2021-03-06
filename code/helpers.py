from cmath import pi, sin, cos
import math
import cv2
import numpy as np
from skimage import img_as_float32
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import random
from os import uname
from re import U
import random
from PIL import Image, ImageDraw as D
import PIL.ImageFont as ImageFont

dt = .05

def get_matches(image1, image2):
    """
    # Wraps OpenCV's ORB function and feature matcher
    # returns two N x 2 numpy arrays, 2d points in image1 and image2
    # that are proposed matches
    """
    # TODO: do this using the data that model gets on frisbee!!!!


def show_matches(image1, image2, points1, points2):
    """
    Shows matches from image1 to image2, represented by Nx2 arrays
    points1 and points2
    """
    image1 = img_as_float32(image1)
    image2 = img_as_float32(image2)

    fig = plt.figure()
    plt.axis('off')

    matches_image = np.hstack([image1, image2])
    plt.imshow(matches_image)

    shift = image1.shape[1]
    for i in range(0, points1.shape[0]):

        random_color = lambda: random.randint(0, 255)
        cur_color = ('#%02X%02X%02X' % (random_color(), random_color(), random_color()))

        x1 = points1[i, 1]
        y1 = points1[i, 0]
        x2 = points2[i, 1]
        y2 = points2[i, 0]

        x = np.array([x1, x2])
        y = np.array([y1, y2 + shift])
        plt.plot(y, x, c=cur_color, linewidth=0.5)

    plt.show()

# TODO: this is so approximate!
# TODO: should hardcode values be parameters to function??
def calculate_projection_matrix(focal_length, origin):
    """
    Calculates projection matrix based on intrinsic data
    """
    theta = 0
    tx = 0
    ty = 0
    tz = 0

    # calculating for the phone that is not the origin
    if not origin:
        theta = 30 * pi / 180 # 40 degrees in radians
        tx = 6.5 # in meters
        ty = 0 # no up and down movement
        tz = -4.66 # in meters

    K = [[focal_length, 0, 0],[0, focal_length, 0],[0, 0, 1]]
    Rt = [[cos(theta), 0, sin(theta), tx], [0, 1, 0, ty], [-sin(theta), 0, cos(theta), tz]]
    return np.matmul(K, Rt)

def matches_to_3d(points1, points2, M1, M2):
    """
    Given two sets of points and two projection matrices, you will need to solve
    for the ground-truth 3D points using np.linalg.lstsq(). For a brief reminder
    of how to do this, please refer to Question 5 from the written questions for
    this project.


    :param points1: [N x 2] points from image1
    :param points2: [N x 2] points from image2
    :param M1: [3 x 4] projection matrix of image2
    :param M2: [3 x 4] projection matrix of image2
    :return: [N x 3] list of solved ground truth 3D points for each pair of 2D
    points from points1 and points2
    """
    n= np.shape(points1)[0]
    
    Q = np.zeros((4, 3))
    a = np.zeros((4, 1))
    points3d = []

    for i in range(0, n):
        point1 = points1[i]
        point2 = points2[i]

        for k in range(0, 3):
            Q[0, k] = M1[2, k] * point1[0] - M1[0][k]

        for k in range(0, 3):
            Q[1, k] = M1[2, k] * point1[1] - M1[1][k]

        for k in range(0, 3):
            Q[2, k] = M2[2, k] * point2[0] - M2[0][k]

        for k in range(0, 3):
            Q[3, k] = M2[2, k] * point2[1] - M2[1][k]

        a[0,0] = M1[0, 3] - M1[2,3] * point1[0]
        a[1,0] = M1[1, 3] - M1[2,3] * point1[1]
        a[2,0] = M2[0, 3] - M2[2,3] * point2[0]
        a[3,0] = M2[1, 3] - M2[2,3] * point2[1]

        point3d = np.linalg.lstsq(Q, a, rcond=None)[0]
        point3d = np.reshape(point3d, (1, 3))
        points3d.append(point3d)

    points3d = np.array(points3d)
    points3d = np.reshape(points3d, (n, 3))
    points3d = points3d.tolist()

    return points3d

# takes centroids of frisbees in two frames and finds speed between them
def get_speed(point1, point2):
    return math.sqrt( ((point1[0]-point2[0])**2)+((point1[1]-point2[1])**2)) / dt


def draw_on_image(xmin, ymin, xmax, ymax, physics_speed, camera_speed, input_image_path, output_image_path, avg_phys_speed="", avg_proj_speed="", centroids=[]):
    img = Image.open(input_image_path)
    
    font_fname = 'arial.ttf'
    font_size = 40
    font = ImageFont.truetype(font_fname, font_size)

    draw = D.Draw(img, "RGBA")
    draw.rectangle([(xmin,ymin),(xmax,ymax)], width=8, outline="black")
    draw.text((10, 10),"Physics calculated speed: " + str(round(physics_speed, 2)) + "m/s", (0,0,0), font=font)
    draw.text((10, 60),"Camera calculated speed: " + str(round(camera_speed, 2)) + "m/s", (0,0,0), font=font)
    if (avg_phys_speed != ""):
        draw.text((10, 110),"Average physics speed: " + str(round(avg_phys_speed, 2)) + "m/s", (0,0,0), font=font)
    if (avg_proj_speed != ""):
        draw.text((10, 160),"Average camera projection speed: " + str(round(avg_proj_speed, 2)) + "m/s", (0,0,0), font=font)
    if (centroids != []):
        for i in range(len(centroids)-1):
            draw.line([(centroids[i][0],centroids[i][1]), (centroids[i+1][0],centroids[i+1][1])], fill="red", width = 5)

    img.save(output_image_path)
