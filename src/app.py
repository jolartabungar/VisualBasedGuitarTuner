#!/usr/bin/env python

'''
This sample demonstrates Canny edge detection.

Usage:
  edge.py [<video source>]

  Trackbars control edge thresholds.

'''

# Python 2/3 compatibility
from __future__ import print_function

import cv2 as cv
import numpy as np

winControls = 'Controls'
winResults1 = 'Edge Detection Results'
winResults2 = 'Harris Corner Detection Results'
winResults3 = 'Fast Feature Detection Results'
winResults4 = 'Hough Line Transform'


def main():
    def apply_non_maxima_suppression(original_image, binary_image):
        # Initialize output image
        output_img = np.zeros(original_image.shape)

        # Determine gradients of original image
        gy, gx = np.gradient(original_image)

        g_magnitude = np.sqrt(np.square(gx) + np.square(gy))
        g_direction = np.arctan(gy * gx)

        # Retrieve image dimensions
        height = original_image.shape[1]
        width = original_image.shape[0]

        for x in range(1, width - 1):
            for y in range(1, height - 1):
                direction = g_direction[x, y]

                # Only check pixels that passed threshold (drawn in white)
                if binary_image[x, y] == 255:

                    # Determine neighbouring pixels based on gradient direction
                    if (0 <= direction < np.pi / 8) or (15 * np.pi / 8 <= direction <= 2 * np.pi):
                        neighbour_p1 = g_magnitude[x, y - 1]
                        neighbour_p2 = g_magnitude[x, y + 1]
                    elif (np.pi / 8 <= direction < 3 * np.pi / 8) or (9 * np.pi / 8 <= direction < 11 * np.pi / 8):
                        neighbour_p1 = g_magnitude[x + 1, y - 1]
                        neighbour_p2 = g_magnitude[x - 1, y + 1]
                    elif (3 * np.pi / 8 <= direction < 5 * np.pi / 8) or (11 * np.pi / 8 <= direction < 13 * np.pi / 8):
                        neighbour_p1 = g_magnitude[x - 1, y]
                        neighbour_p2 = g_magnitude[x + 1, y]
                    else:
                        neighbour_p1 = g_magnitude[x - 1, y - 1]
                        neighbour_p2 = g_magnitude[x + 1, y + 1]

                    # Add pixel to output if it is local maxima
                    if g_magnitude[x, y] >= neighbour_p1 and g_magnitude[x, y] >= neighbour_p2:
                        output_img[x, y] = binary_image[x, y]

        return output_img

    def add_markers(original_image, binary_image):
        height = original_image.shape[1]
        width = original_image.shape[0]

        # Convert original image to colored image to allow markers to be drawn in color
        output_img = cv.cvtColor(original_image, cv.COLOR_GRAY2RGB)
        for x in range(1, width - 1):
            for y in range(1, height - 1):
                # If pixel passed NMS, draw marker
                if binary_image[x, y] == 255:
                    cv.drawMarker(output_img, (y, x), color=(255, 0, 0),
                                  markerType=cv.MARKER_TILTED_CROSS, markerSize=1)

        return output_img

    def harris_corner_detect(original_image):
        # Compute minimum eigen value
        min_eigen_val = cv.cornerMinEigenVal(original_image, 3)
        # Determine eigenvalue threshold based on trackbar value
        min_egv_threshold = cv.getTrackbarPos('thrs3', winControls) / 1000

        # Create binary image based off current value of threshold
        _, binary_img = cv.threshold(min_eigen_val, min_egv_threshold, 255, 0)
        # Apply NMS algorithm
        after_nms_img = apply_non_maxima_suppression(original_image, binary_img)
        # Add markers
        orig_with_corners = add_markers(original_image, after_nms_img)
        result = orig_with_corners

        cv.imshow(winResults2, result)

    def canny_edge_detect(original_image, gray_image):
        thrs1 = cv.getTrackbarPos('thrs1', winControls)
        thrs2 = cv.getTrackbarPos('thrs2', winControls)

        edge = cv.Canny(gray_image, thrs1, thrs2, apertureSize=5)

        vis = original_image.copy()
        vis = np.uint8(vis / 2.)
        vis[edge != 0] = (0, 255, 0)
        result = vis

        cv.imshow(winResults1, result)

    def fast_feature_detect(original_image, gray_image):
        fast = cv.FastFeatureDetector_create()
        fast.setNonmaxSuppression(False)

        img_copy = original_image.copy()
        key_points = fast.detect(gray_image, None)
        # img_copy[key_points != 0] = (255, 0, 0)
        result = cv.drawKeypoints(img_copy, key_points, None, color=(255, 0, 0))

        cv.imshow(winResults3, result)

    def hough(img, gray):

        thrs3 = cv.getTrackbarPos('thrs3', winControls)
        img_copy = img.copy()

        edges = cv.Canny(gray, 50, 150, apertureSize=3)
        cv.imshow("canny",edges)

        linesP = cv.HoughLinesP(edges, 1, np.pi / 180, thrs3, None, 50, 10)
        print(linesP)
        if linesP is not None:
            for i in range(0, len(linesP)):
                l = linesP[i][0]
                cv.line(img_copy, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv.LINE_AA)
        cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", img_copy)

    def on_change(*arg):
        frame_pos = cv.getTrackbarPos('VideoFrame', winControls)
        cap.set(1, frame_pos)
        _flag, img = cap.read()
        img = cv.resize(img[600:1920, 0:1080], (1056, 594))

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # canny_edge_detect(img, gray)
        fast_feature_detect(img, gray)
        # harris_corner_detect(gray)
        hough(img, gray)

    cap = cv.VideoCapture("../data/vid1.mp4")
    frames_total = int(cap.get(7) - 1)

    cv.namedWindow(winControls)

    # Edge Detection
    # cv.createTrackbar('thrs1', winControls, 2000, 5000, on_change)
    # cv.createTrackbar('thrs2', winControls, 4000, 5000, on_change)

    # Harris Corner Detection
    # cv.createTrackbar('thrs3', winControls, 0, 20, on_change)

    cv.createTrackbar('thrs3', winControls, 0, 500, on_change)


    # Scroll through frames
    cv.createTrackbar('VideoFrame', winControls, 0, frames_total, on_change)

    cv.imshow(winControls, np.zeros([1, 1500]))

    cv.waitKey(0)
    cv.destroyAllWindows()
    print('Done')


main()
