"""
Title:  User Input With Validation
Description: Methods used for getting a user's input and validating it. 
"""

import math
import sys
import cv2
import os


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

    # common video file extensions
    video_file_extensions = [
        ".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv",
        ".ogg", "m4p", "m4v", ".avi", ".wmv", ".mov",
        ".qt", ".flv", ".swf", ".avchd", ".mp4"
    ]

    # make sure location contains "/" before continuing
    if "/" not in str(location):
        print("Inputed location value: " + str(location) + ", does not contain a /. Please input something else!")
        return

    # make sure location/directory exists before continuing
    try:
        all_files = os.listdir(str(location))
    except:
        print("Inputed directory does not exist: " + str(location))
        return

    # grab only files that are video files
    video_files = []
    for file in all_files:
        for vext in video_file_extensions:
            if str(vext) in str(file):
                video_files.append(file)
                break
    
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


