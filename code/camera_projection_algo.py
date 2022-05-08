import argparse
import os
from skimage import io
import numpy as np
import helpers

focal_length_thirteen_mini = 23 #focal length in mm

def parse_args():
    """ Perform command-line argument parsing. """

    parser = argparse.ArgumentParser(
        description="Project 5 camera calibration!")
    parser.add_argument(
        '--image1',
        required=True,
        default='mgvid1',
        help='Which image 1 sequence to use')
    parser.add_argument(
        '--image2',
        required=True,
        choices='mgvid2',
        help='Which image 2 sequence to use')
    parser.add_argument(
        '--data',
        default=os.getcwd() + '/../data/images',
        help='Location where your data is stored')
    parser.add_argument(
        '--ransac-iters',
        type=int,
        default=100,
        help='Number of samples to try in RANSAC')
    parser.add_argument(
        '--num-keypoints',
        type=int,
        default=5000,
        help='Number of keypoints to detect with ORB')
    parser.add_argument(
        '--no-intermediate-vis',
        action='store_true',
        help='Disables intermediate visualizations'
    )

    return parser.parse_args()


def main():
    args = parse_args()

    image1_dir = os.path.join(args.data, args.image1)
    image2_dir = os.path.join(args.data, args.image2)
    
    image1_dir_len = os.listdir(image1_dir).length
    image2_dir_len = os.listdir(image2_dir).length

    # gets all images from first angle
    throw1 = []
    for i in range(1, image1_dir_len):
        throw1.append(io.imread(os.path.join(image1_dir, i)))
    
    # gets all images from second angle
    throw2 = []
    for i in range(1, image2_dir_len):
        throw2.append(io.imread(os.path.join(image2_dir, i)))

    # calling student's calculate_projection_matrix function on each image
    print('Calculating projection matrix')
    Ms = helpers.calculate_projection_matrix(focal_length_thirteen_mini)
    # TODO: calculate second projection matrix with Mars phone

    points3d = []
    points3d_color = []

    # Loop through pairs of consecutive images
    for i in range(len(throw1) - 1):
        image1 = throw1[i]
        M1 = Ms
        image2 = throw2[i]
        M2 = Ms 

        # Uses OpenCV's ORB function and feature matcher to obtain proposed matching points between a pair of images
        print(f'Getting matches for images')
        points1, points2 = helpers.get_matches(image1, image2, args.num_keypoints)
        if not args.no_intermediate_vis:
            helpers.show_matches(image1, image2, points1, points2)

        # Obtain an estimated fundamental matrix (F) and inlier point pairs using student's ransac_fundamental_matrix
        # by passing in proposed matching points calculated previously.
        print(f'Filtering with RANSAC...')
        F, inliers1, inliers2 = helpers.ransac_fundamental_matrix(
            points1, points2, args.ransac_iters)

        # Visualize student's matched inlier point pairs on the original images
        if not args.no_intermediate_vis:
            helpers.show_matches(image1, image2, inliers1, inliers2)

        # Uses student's matches_to_3d to infer the 3D points that inlier pairs correspond to
        print('Calculating 3D points for accepted matches...')
        points3d += helpers.matches_to_3d(inliers1, inliers2, M1, M2)
        points3d_color += [tuple(image1[int(point[1]), int(point[0]), :] / 255.0) for point in inliers1]

    points3d = np.array(points3d)


if __name__ == '__main__':
    main()
