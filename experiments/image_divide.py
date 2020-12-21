# About: Split image in half then divides left and right side x amount of time(s), then clusters points to,
#        average the points. Then draws line point to point, so highlight a lane.
#
# Author: Mehmet Yilmaz
#
# Update: From what we have, this method proves to be the best method. So this method was implmented.

import cv2

# (x,y) points used for testing
def points(choice):
    if(choice == 1):
        return [(190, 697), (306, 690), (390, 537), (256, 520), (1110, 697), (940, 702), (755, 455), (942, 500), (734, 117), (696, 153), (850, 150), (780, 134), (900, 140)]
    elif(choice == 2):
        return [(190, 697), (306, 690), (390, 537), (256, 520)]
    elif(choice == 3):
        return [(190, 697), (306, 690), (390, 537), (256, 520), (1110, 697), (940, 702), (755, 455), (942, 500)]

# print a list, line by line
def print_list(values):
    c = 1
    for i in values:
        print(c, ":", i)
        c = c + 1

# divide image in half then divide each side x amount of times, these points are saved to really divide the points
def half_divide(image, splits_per_half):
    x = image.shape[1]  # height
    y = image.shape[0]  # width

    P_left = []
    P_right = []

    mid = int(x/2)
    point = int(y/splits_per_half)

    pos = 0
    for i in range(splits_per_half):

        left_p1_x = 0
        left_p1_y = point*pos
        left_p2_x = mid
        left_p2_y = point*(pos+1)
        cv2.rectangle(image, (left_p1_x, left_p1_y), (left_p2_x, left_p2_y), (255, 0, 0), 4)
        P_left.append([left_p1_x, left_p1_y, left_p2_x, left_p2_y])

        right_p1_x = mid
        right_p1_y = point*pos
        right_p2_x = mid*2
        right_p2_y = point*(pos+1)
        cv2.rectangle(image, (right_p1_x, right_p1_y), (right_p2_x, right_p2_y), (255, 255, 255), 4)
        P_right.append([right_p1_x, right_p1_y, right_p2_x, right_p2_y])

        pos = pos + 1
    
    return P_left, P_right, mid

# plot all points in a list onto an OpenCV image
def draw_points(image, P, color):
    for p in P:
        cv2.circle(image, p, 8, color, -1)

# cluster each point depending on how the image is divided
def group_points(splits_per_half, mid, P, P_left, P_right):
    left_group = [[] for i in range(splits_per_half)]
    right_group = [[] for i in range(splits_per_half)]

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

# average each point in a cluster.
def average_points(left_group, right_group):
    avg_points_left = []
    avg_points_right = []
    #avg_color = (255, 255, 0)
    for grouping in left_group:
        if(len(grouping) > 0):
            temp = [sum(x)/len(x) for x in zip(*grouping)]
            temp = (int(temp[0]), int(temp[1]))
            avg_points_left.append(temp)
            #cv2.circle(image, temp, 8, avg_color, -1)

    for grouping in right_group:
        if(len(grouping) > 0):
            temp = [sum(x)/len(x) for x in zip(*grouping)]
            temp = (int(temp[0]), int(temp[1]))
            avg_points_right.append(temp)
            #cv2.circle(image, temp, 8, avg_color, -1)
    
    return avg_points_left, avg_points_right

# draw lines, point to point, given a list of points
def draw_lines(image, color, thickness, points):
    for i in range(len(points)-1):
        cv2.line(image, points[i], points[i+1], color, thickness)

# main function
def main(image, P):
    splits_per_half = 3 # number of divides for both left and right sides

    # divide and divide the image
    P_left, P_right, mid= half_divide(image, splits_per_half)

    # plot testing points onto the image, it should kind of look like a lane
    draw_points(image, P, (255, 0, 255))

    # cluster and group all the points on the right and left side of the image
    left_group, right_group = group_points(splits_per_half, mid, P, P_left, P_right)
    
    # average the points in each cluster into a one point for each cluster
    avg_points_left, avg_points_right = average_points(left_group, right_group)

    # draw average points as a line on the image
    draw_lines(image, (255, 255, 255), 4, avg_points_left)
    draw_lines(image, (255, 255, 255), 4, avg_points_right)

    # draw average points on the image
    draw_points(image, avg_points_left, (255, 255, 0))
    draw_points(image, avg_points_right, (255, 255, 0))

    # show everything
    cv2.imshow("demo", image)

if __name__ == "__main__":
    P = points(3)   # pick test set of points
    image = cv2.imread("split_it.jpeg") # pick test image (baby yoda!)
    main(image, P)  # run everything
    cv2.waitKey(0)  # wait for space to close the program


