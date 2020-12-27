"""
Title:  Simple Lane Detection
Description: This code uses a combination of AOI, Thresholding, Canny, HoughLinesP, & point clustering, 
             to detect the left and right lane of a driving car using classical computer vision methods. 
"""


import math
import sys
import cv2
import os


def half_divide(image, splits_per_half, show_clusters=False):
    """
    Divides image in half and divide those 2 halfs of the image by splits_per_half amount of times

    Parameters:
    :param image: array, frame/image, ideally the AOI
    :param splits_per_half: int, number of divides per each half (right & left) of the image
    :param show_clusters: boolean, visualization of each divide/cluster, drawn with open sqaures

    Returns:
    :returns: P_left, array
        An array of top left points (x1,y1) and bottom right points (x2,y2) for each clustering,
        of the image. This array is for the left side of the divided image.

    :returns: P_right, array
        An array of top left points (x1,y1) and bottom right points (x2,y2) for each clustering,
        of the image. This array is for the right side of the divided image.
    """

    x = image.shape[1]  # width of image
    y = image.shape[0]  # height of image

    P_left = []
    P_right = []

    mid = int(x/2)  # mid location of the image
    point = int(y/splits_per_half)  # divided height of the image by splits_per_half

    # loop though each splits_per_half*2 clusters in the image and store those cluster's,
    # top-left and bottom-right cooridantes.
    pos = 0
    for i in range(splits_per_half):

        left_p1_x = 0
        left_p1_y = point*pos
        left_p2_x = mid
        left_p2_y = point*(pos+1)
        P_left.append([left_p1_x, left_p1_y, left_p2_x, left_p2_y])

        right_p1_x = mid
        right_p1_y = point*pos
        right_p2_x = mid*2
        right_p2_y = point*(pos+1)
        P_right.append([right_p1_x, right_p1_y, right_p2_x, right_p2_y])

        if(show_clusters):
            cv2.rectangle(image, (left_p1_x, left_p1_y), (left_p2_x, left_p2_y), (255, 0, 0), 4)
            cv2.rectangle(image, (right_p1_x, right_p1_y), (right_p2_x, right_p2_y), (255, 255, 255), 4)

        pos = pos + 1
    
    return P_left, P_right, mid


def draw_points(image, P, color, thickness):
    """
    Plot each a list of given points on a selected image

    Parameters:
    :param image: array, frame/image.
    :param P: array, set of (x,y) points.
    :param color: array, RGB value for points.
    :param thickness: double, thickness of each point.

    Returns:
    :returns: Draws inputed points on inputed image.
    """

    for p in P:
        cv2.circle(image, p, thickness, color, -1)


def group_points(splits_per_half, mid, P, P_left, P_right):
    """
    Groups/clusters points based on how the image is divided

    Parameters:
    :param splits_per_half: int, number of divides per each half (right & left) of the image
    :param mid: int, middile width location of the image.
    :param P: list, a set of (x,y) points.
    :P_left: list, a set of (x,y) points used for "grouping" the left side of the image. 
             This is an output of half_divide().
    :P_right: list, a set of (x,y) points used for "grouping" the right side of the image. 
              This is an output of half_divide().

    Returns:
    :returns left_group: list of lists of turples, [[(x,y)], [], ...] 
        A list of lists of turples, where each index presentations each left side divide and,
        each turple is a (x,y) coordinate on the image.
    
    :returns right_group: list of lists of turples, [[(x,y)], [], ...] 
        A list of lists of turples, where each index presentations each right side divide and,
        each turple is a (x,y) coordinate on the image.
    """

    # list of empty lists, used for clustering points
    left_group = [[] for i in range(splits_per_half)]
    right_group = [[] for i in range(splits_per_half)]

    # cluster each points based on what sides its on,
    # as well as what divide a point is on.
    for points in P:
        if(points[0] <= mid):
            c = 0
            for sections in P_left:
                x1, y1, x2, y2 = sections
                if(y1 <= points[1] and y2 >= points[1]):
                    left_group[c].append(points)
                c = c + 1
        else:
            c = 0
            for sections in P_right:
                x1, y1, x2, y2 = sections
                if(y1 <= points[1] and y2 >= points[1]):
                    right_group[c].append(points)
                c = c + 1
    
    return left_group, right_group


def average_points(left_group, right_group):
    """
    Averages every clustering of points for both the left and right sides of the image, into
    one points per cluster.

    Parameters:
    :param left_group: list of lists of turples, [[(x,y)], [], ...], 
        contains all the clustering of the points on the left side of the image.
    :param right_group: list of lists of turples, [[(x,y)], [], ...], 
        contains all the clustering of the points on the right side of the image.

    Returns:
    :returns avg_points_left: list of turples (x,y),
        A list of turples, where each turple is the averaging of every point in a cluster.
        For the left side of the image.
    
    :returns avg_points_right: list of turples (x,y),
        A list of turples, where each turple is the averaging of every point in a cluster.
        For the right side of the image.
    """

    avg_points_left = []
    avg_points_right = []

    # average the turple of each cluster for the left side.
    for grouping in left_group:
        if(len(grouping) > 0):
            averaged_point = [sum(point)/len(point) for point in zip(*grouping)]
            averaged_point = (int(averaged_point[0]), int(averaged_point[1]))
            avg_points_left.append(averaged_point)

    # average the turple of each cluster for the right side.
    for grouping in right_group:
        if(len(grouping) > 0):
            averaged_point = [sum(point)/len(point) for point in zip(*grouping)]
            averaged_point = (int(averaged_point[0]), int(averaged_point[1]))
            avg_points_right.append(averaged_point)
    
    return avg_points_left, avg_points_right


def draw_lines(image, color, thickness, points):
    """
    Draw a line from point to point on the inputed image.

    Parameters:
    :param image: array, frame/image.
    :param color: array, RGB value for points.
    :param thickness: double, thickness of each point.
    :param points: list of turples,
        A set of points used for drawing the line.

    Returns:
    :returns: Draws inputed points as a line.
    """
    for i in range(len(points)-1):
        cv2.line(image, points[i], points[i+1], color, thickness)


def get_xy(event, x, y, flags, param):
    """
    Mouse callback function for detecting mouse clicks,
    this function is used for detereming area of interest,
    (AOI) as it determines the (x,y) of where the user,
    clicked on an image.

    Parameters:
    :param event: OpenCV's mouse click event variable.
    :param x: int, x value of click coordinate
    :param y: int, y value of click coordinate
    :param param: list, A list of parameters: window_name, image, point_list
        window_name: string, Name of OpenCV window for the mouse clicking.
        image: array, frame/image.


    Returns:
    :returns: Opens new windows that detects mouse clicks and draws red open,
              sqaures at where the mouse was clicked.

    :returns: Two (x,y) turples
    """

    list_limit = 2  # number of points need to cropping

    # listen for mouse clicks on new window
    if event == cv2.EVENT_LBUTTONUP:
        window_name, image, point_list = param  # Unpack parameters

        # draw red open sqaure at were a mouse click was placed in an image
        cv2.rectangle(image, pt1=(x-15, y-15), pt2=(x+15, y+15), color=(0,0,255),thickness=3)
        cv2.imshow(window_name, image)

        # only collect two mouse click coordinates, print message after 
        # two coordinates have been collected
        if(len(point_list) < list_limit):
            point_list.append((x, y))
        else:
            print("Maxed out number of clicks, please hit ENTER or CTRL-C")


def create_named_window(window_name, image):
    """
    Utility function to create an image window.

    Parameters:
    :param window_name: string, name of OpenCV window.
    :param image: array, frame/image. 

    Returns:
    :returns: New, resized, OpenCV window
    """

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
    """
    Get list of two points and returns it in a x1, y1, x2, y2 formate.
    This is used after the two points are gathered from the get_xy().

    Parameters:
    :param points_list: list, A list of two turples (x,y)

    Returns:
    :returns: Four int values: x1, y1, x2, y2
    """

    x1 = points_list[0][0]
    y1 = points_list[0][1]
    x2 = points_list[1][0]
    y2 = points_list[1][1]

    return x1, y1, x2, y2


def offset_to_original(P, cx1, cy1):
    """
    Offset points from cropped image to the original image.

    Parameters:
    :param P: list, a list of (x,y) turples.
    :param cx1: x value offset.
    :param cy1: y value offset.

    Returns:
    :returns: list, list of new points with offset appled.
    """

    new_P = []
    for i in range(len(P)):
        temp = (P[i][0]+cx1, P[i][1]+cy1)
        new_P.append(temp)
    return new_P


def highlight_lanes(draw_image, avg_points_left, avg_points_right):
    """
    Draws lines and points given a list of points on the left divide and,
    A list of points on the right divide of the AOI.

    Parameters:
    :param draw_image: array, frame/image.
    :param avg_points_left: 
        list, list of (x,y) turples of averaged points on the left divide of the AOI.
    :param avg_points_right:
        list, list of (x,y) turples of averaged points on the right divide of the AOI.

    Returns:
    :returns: Draw lines and points on inputed OpenCV image.
    """

    # default RGB color and thinkness of lines
    draw_line_color = (255, 255, 0)
    draw_line_thickness = 25
    
    # draw lines on image
    draw_lines(draw_image, draw_line_color, draw_line_thickness, avg_points_left)
    draw_lines(draw_image, draw_line_color, draw_line_thickness, avg_points_right)

    # default RGB color and thinkness of points
    draw_points_color = (255, 0, 255)
    draw_points_thickness = 4

    # draw points on image
    draw_points(draw_image, avg_points_left, draw_points_color, draw_points_thickness)
    draw_points(draw_image, avg_points_right, draw_points_color, draw_points_thickness)


def classic_lane_detection(video_file, splits_per_half):
    """
    Serves as the main function of classic_lane_detection, given a video file location and
    a splits_per_half value, the following processed occur to detect and highlight the 1-2,
    lanes the driving vechile is in:
        1) AOI/cropping is selected
        2) Gaussian Blur & Grayscale is applied
        3) Canny and HoughLinesP is applied
        4) The AOI is divided in half then into groups/cluster for each half
        5) Points are clustered based on the divided from step 4
        6) Each clusters' points are averaged into one point
        7) The averaged points and divides are used to detect the lanes
        9) The results are displayed though OpenCV windows

    Parameters:
    :param video_file: string, video file location/name.
    :param splits_per_half: int, number of divides per each half (right & left) of the image.

    Returns:
    :returns: Window 1, AOI selection OpenCV window.
    :returns: Window 2, AOI processing and point of view.
    :returns: Window 3, original video with lane detection applied.
    """

    # load inputed video
    video = cv2.VideoCapture(video_file)
    got_image, img = video.read()

    # make sure the video file exists
    if not got_image:
        print("Cannot read video source")
        sys.exit()

    crop_points = []    # list that will hold 2 turple points, (x,y), which will be used from AOI/cropping

    frame = 0 # count number of frames

    # loop though each frame in video
    while True:

        # break loop when there are no more frames in video
        got_image, img = video.read()
        if not got_image:
            break

        # copy frame, serves as AOI image (Window 2)
        image = img

        # copy frame, serves as final image (Window 3)
        og = image.copy()

        # wait for user to selected AOI (Windows 1)
        if(frame == 0):
            window_name = "[Set AOI]-[Pick Top-Left & Bottom-Right Crop Corners]-[SPACE->Start]"

            # rather mouse clicks on image, to determine the two points needed to apply AOI
            mouse_display = image.copy()
            create_named_window(window_name, mouse_display)
            cv2.imshow(window_name, mouse_display)
            cv2.setMouseCallback(window_name, on_mouse=get_xy, param=(window_name, mouse_display, crop_points))
            cv2.waitKey(0)

        # load variables from determined AOI points
        cx1, cy1, cx2, cy2 = crop_edges(crop_points)

        # apply AOI; crop image
        img = img[cy1:cy2, cx1:cx2]

        image = img

        frame = frame + 1 # add to frame counter

        # display current frame number on main image
        cv2.putText(og, text=str(frame), org=(20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0, 0, 0), thickness=3)

        # apply filters, thresholdings, and Canny
        image = cv2.GaussianBlur(image,(7,7),0)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.Canny(image,100,200)

        # apply HoughLinesP to determine lines/points of possible lanes
        points = cv2.HoughLinesP(image, rho=1.0, theta=math.pi/180, threshold=20, minLineLength=10, maxLineGap=10)

        # store all the points from HoughLinesP
        P = []
        if points is not None:
            for point in points:
                x1, y1, x2, y2 = point[0]

                # draw points found from HoughLinesP 
                cv2.circle(img, (x1, y1), 5, [0, 0, 0], -1)
                cv2.circle(img, (x2, y2), 5, [0, 0, 0], -1)

                P.append((x1, y1))
                P.append((x2, y2))

        draw_image = img

        # divide the AOI image in half, then divide those halfs splits_per_half amount of times
        P_left, P_right, mid= half_divide(draw_image, splits_per_half, True)

        # cluster points on left and right side
        left_group, right_group = group_points(splits_per_half, mid, P, P_left, P_right)

        # average clusters' points into one point per clustering
        avg_points_left, avg_points_right = average_points(left_group, right_group)

        # draw clustering process to AOI image (Window 2)
        #highlight_lanes(img, avg_points_left, avg_points_right)

        # offset averaged points to original image
        avg_points_left = offset_to_original(avg_points_left, cx1, cy1)
        avg_points_right = offset_to_original(avg_points_right, cx1, cy1)

        # display message of rather or not the left and/or the right lane has been detected or not
        left_message = "Left Lane NOT Detected"
        right_message = "Right Lane NOT Detected"
        if(len(avg_points_left) > 0):
            left_message = "Left Lane DETECTED"
        if(len(avg_points_right) > 0):
            right_message = "Right Lane DETECTED"
        
        # left lane detection status image message
        cv2.putText(og, text=left_message, org=(20, 110), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.65, color=(0, 0, 0), thickness=2)
        
        # right lane detection status image message
        cv2.putText(og, text=right_message, org=(20, 180), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.65, color=(0, 0, 0), thickness=2)

        # draw highlight lanes on the original image (Window 3)
        highlight_lanes(og, avg_points_left, avg_points_right)

        # display the windows
        cv2.imshow("Original Frame/Video", og)
        cv2.imshow("Selected AOI Point Of View", img)

        cv2.waitKey(30)


def validating_user_input(initial_message, input_message, invalid_message):
    """
    Input validation for a user's inputted int value. The messages used in this function,
    can be configured. The messages and inputting will take place in a terminal console.

    :param initial_message: string,
        Initial message for the user to read. This message will be in RED.
    :param input_message: string,
        Input message that will be displayed to the user before the user inputs.
    :param invalid_message: string,
        Invalid message displayed if the user inputed a non-int value. This message,
        will be in RED.
       
    Returns:
    :returns: int, the user's inputed whole number with input validation to make sure of it.
    """

    # prints important message in RED
    print("\033[91m" + str(initial_message) + "\033[0m")

    # gets user's input
    user_input = str(input(str(input_message)))
    print()

    # input validation, for making sure the user's input is a whole number
    while(user_input.isdigit() == False):
        print("\033[91m" + invalid_message + "\033[0m")
        user_input = str(input(str(input_message)))
        print()
    
    return int(user_input)


def select_video(location):
    """
    Give a location/directory, this function will list all the files in that directory,
    then allow the user to select what video they wish to apply simple lane detection to.
    Input validation is applied and certain tests are applied to make sure nothing breaks.

    :param location: string, PATH to directory of files, ideally video files.
       
    Returns:
    :returns: string, PATH to user's selected video/file for simple lane detection to use.
        or
    :returns: none, a none value is returned if the inputed param fails a test.
    """

    # make sure location contains "/" before continuing
    if "/" not in str(location):
        print("Inputed location value: " + str(location) + ", does not contain a /. Please input something else!")
        return

    # make sure location/directory exists before continuing
    try:
        video_files = os.listdir(str(location))
    except:
        print("Inputed directory does not exist: " + str(location))
        return
    
    # make sure location contains more then 0 files before continuing
    if(len(video_files) == 0):
        print("No files in inputed directory: " + str(location))
        return
    
    # print all files in location
    print("\033[4m" + "Files in inputed directory: " + str(location) + "\033[0m")
    for i in range(len(video_files)):
        print(str(i) + ") " + str(video_files[i]))
    print()

    # key string values for validating_user_input() function
    main_mesg, input_mesg, invalid_mesg = ("Please Select Desired Video For Simple Lane Detection!",
                                           "Select Video (int): ",
                                           "Invalid Input, Please Enter Only Whole Numbers!")

    # input validation for user selecting a video in location
    user_input = validating_user_input(main_mesg, input_mesg, invalid_mesg)
    while(True):
        if(user_input >= 0 and user_input < len(video_files)):
            break
        else:
            print("Invalid Input, Try Again! \n")
            user_input = validating_user_input(main_mesg, input_mesg, invalid_mesg)

    return str(location) + str(video_files[user_input])


# main function
if __name__ == "__main__":

    # get user to input their desired whole number of the splits_per_half value
    user_input = validating_user_input("Please Enter splits_per_half To Continue!",
                                       "Input desired splits_per_half value (ex: 6): ",
                                       "Invalid Input, Please Enter Only Whole Numbers!")

    # set number of divides per each half (right & left) of the image    
    splits_per_half = user_input

    # selected video name/path
    video = select_video("./assets/")   # videos.toronto_way

    if video is not None:
        # apply clasic lane detection:
        classic_lane_detection(video, splits_per_half)
        
        # closing message
        print("\n" + "[ Enter SPACE To Exit ]")
        cv2.waitKey(0)
        
    else:
        print("Failed to load, check inputed splits_per_half value or inputed video!")




