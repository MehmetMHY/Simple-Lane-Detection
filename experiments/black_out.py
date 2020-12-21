# About:
# This function simply "crops" the image by coverting everything in the image black but,
# the area that is being cropped. This was developed in the hopes of being acting as a tool,
# to get an AOI without the need to offset the points, but sadly this really effects Canny(),
# and the output of HoughLinesP.
#
# Author: Mehmet Yilmaz

import sys
import cv2
import numpy as np

# mouse callback function
def get_xy(event, x, y, flags, param):
    list_limit = 2
    if event == cv2.EVENT_LBUTTONUP:
        window_name, image, point_list = param  # Unpack parameters
        cv2.rectangle(image, pt1=(x-15, y-15), pt2=(x+15, y+15), color=(0,0,255),thickness=3)
        cv2.imshow(window_name, image)
        if(len(point_list) < list_limit):
            point_list.append((x, y))
            print((x, y))

# utility function to create an image window.
def create_named_window(window_name, image):
    # WINDOW_NORMAL allows resize; use WINDOW_AUTOSIZE for no resize.
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    h = image.shape[0]  # image height
    w = image.shape[1]  # image width

    # Shrink the window if it is too big (exceeds some maximum size).
    WIN_MAX_SIZE = 1000
    if max(w, h) > WIN_MAX_SIZE:
        scale = WIN_MAX_SIZE / max(w, h)
    else:
        scale = 1
    cv2.resizeWindow(winname=window_name, width=int(w * scale), height=int(h * scale))

def crop_edges(points_list):
    x1 = points_list[0][0]
    y1 = points_list[0][1]
    x2 = points_list[1][0]
    y2 = points_list[1][1]
    return x1, y1, x2, y2

def black_out_crop(image, x, y, x1, y1, x2, y2):
    image = cv2.rectangle(image, (0, 0), (x, y1), (0, 0, 0), -1)
    image = cv2.rectangle(image, (0, 0), (x1, y), (0, 0, 0), -1)
    image = cv2.rectangle(image, (x2, 0), (x, y), (0, 0, 0), -1)
    image = cv2.rectangle(image, (x1, y2), (x2, y), (0, 0, 0), -1)
    return image


def main(image):
    crop_points = []

    x = image.shape[1]  # height
    y = image.shape[0]  # width

    window_name = "Set AOI - [ Enter SPACE To Start ]"

    mouse_display = image.copy()
    create_named_window(window_name, mouse_display)
    cv2.imshow(window_name, mouse_display)

    cv2.setMouseCallback(window_name, on_mouse=get_xy, param=(window_name, mouse_display, crop_points))
    cv2.waitKey(0)

    x1, y1, x2, y2 = crop_edges(crop_points)

    black_out_crop(image, x, y, x1, y1, x2, y2)

    cv2.imshow("demo", image)
        
if __name__ == "__main__":
    image = cv2.imread("split_it.jpeg")
    main(image)
    print("[ Enter SPACE To Exit ]")
    cv2.waitKey(0)