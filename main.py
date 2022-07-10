"""
Title:  Main Function For Simple Lane Detection
Description: Main function that shows Simple Lane Detection.
"""

from modules import simple_method as sm
from modules import user_input as ui
import cv2


if __name__ == "__main__":
    try:
        # get user to input their desired whole number of the splits_per_half value
        user_input = ui.validating_user_input("Please Enter splits_per_half To Continue!",
                                        "Input desired splits_per_half value (ex: 6): ",
                                        "Invalid Input, Please Enter Only Whole Numbers!")

        # set number of divides per each half (right & left) of the image    
        splits_per_half = user_input

        # selected video name/path
        video = ui.select_video("./assets/")   # videos.toronto_way

        if video is not None:
            # apply clasic lane detection:
            sm.classic_lane_detection(video, splits_per_half)
            
            # closing message
            print("\n" + "[ Enter SPACE To Exit ]")
            cv2.waitKey(0)
            
        else:
            print("Failed to load, check inputed splits_per_half value or inputed video!")

    except KeyboardInterrupt:
        print("\n" + "Closed program due to interrupt caused by the pressing of CTRL-C")
        pass



