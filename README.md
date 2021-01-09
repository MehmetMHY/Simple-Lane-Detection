# Simple Lane Detection
- By: Mehmet Yilmaz
- Date: 1-9-2021


## About:
- Simple lane detection done though classical Computer Vision methods. With a combination of AOI, Thresholding, Canny line detection, HoughLinesP, & point clustering; the detection of the left and right lane of the driving car in the video (point of view) is achieved.
- This method is NOT PERFECT as it really only works best if the video data is clean, there are no objects/cars in the AOI, and the road is not so broken down. To learn more about this method's imperfections, please check out the "Key Bugs & Limitations" section of this README.
- Dispite it's shortcomings, this method does remove most of the noise in a frame and has the protentional of being a more efficient lane detection system.

## Future/Stretch Goals:
- Implement more advance methods using Convolutional Neural Networks (CNN).
- Find other, better, methods for isolating lanes. Such as HSV thresholding.
- Apply object detection for detecting cars and none road-like objects. In doing so, those objects can be blurred or removed which would remove more noise from a frame.

## Simple Preview:
![SLD-preview](https://user-images.githubusercontent.com/15916367/102777441-d335e700-434d-11eb-8f0b-a4ec1089d4dd.gif)

## Key Bugs & Limitations:
- A big limitation with this method is that the left and right lanes, two lanes total, of the driving vehicle can potentially be detected, limiting what the code can provide to the car overall.

- Big bugs found with this current method can be seen and explained though Figure 1:
<img width="887" alt="figure_1" src="https://user-images.githubusercontent.com/15916367/103167390-07932280-47e8-11eb-830c-9c66a1dc8ada.png">

## Credits:

### - Papers Read:
- [Advanced lane detection technique for structural highway based on computer vision algorithm](https://www.sciencedirect.com/science/article/pii/S2214785320373302?casa_token=M4ZoLzeJwx4AAAAA:ukSK4iSWKjdMNAMMDgsUf315ZNYUahOzGfoExKCEooWribsMTM6Jo-9V-C4EwBglgmOa69tYquA)

- [Real-time Lane detection and Motion Planning in Raspberry Pi and Arduino for an Autonomous Vehicle Prototype](https://arxiv.org/pdf/2009.09391.pdf)

- [Real-Time Lane Departure Detection Based on Extended Edge-Linking Algorithm](https://ieeexplore.ieee.org/document/5489518)

### - Driving Clips:
- Due to many driving car footages being too long and/or having too high of a resolution, I had to trim/clip them into a smaller length as well as a lower resolution. The driving footage included in this repo is a clip/segment from toronto_way.

- (YouTube) Self Driving Car Complete Dataset: [[link](https://www.youtube.com/playlist?list=PLUop7b1Q1uZkv5__d2yPZG1cAXcelata8)]

- Clips Used For This Project:
	- cal_freeway: [[link](https://www.youtube.com/watch?v=eoXguTDnnHM)]
	- delihi_drive: [[link](https://www.youtube.com/watch?v=UjCFTNhZGeo&list=PLUop7b1Q1uZkv5__d2yPZG1cAXcelata8&index=89)]
	- mout_drive: [[link](https://www.youtube.com/watch?v=pvUj2M-wRHQ)]
	- missi_drive: [[link](https://www.youtube.com/watch?v=isJlndP8V9g&list=PLUop7b1Q1uZkv5__d2yPZG1cAXcelata8&index=18)]
	- toronto_way: [[link](https://www.youtube.com/watch?v=uHusTBlqlZI)], # clip included!
	- toronto_longer: [[link](https://www.youtube.com/watch?v=uHusTBlqlZI)]

### - Other Sources:
- [OpenCV Canny Edge Detection Doc](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html)
- [OpenCV Hough Line Transform Doc](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html)
- [OpenCV Smoothing Images Doc](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html)
- [StackOverflow Detect Mouse Position Click - Discussion](https://stackoverflow.com/questions/28327020/opencv-detect-mouse-position-clicking-over-a-picture)
-   *The following functions where provided to me from the class CSCI437 (Colorado School of Mines) during the Fall 2020 semester:*

        get_xy()
		create_named_window()

	- *These functions were modified for this project. Some of these functions are no longer in use but they can be found in this repo's git history so I wanted to include this credit.*

