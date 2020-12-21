# Simple Lane Detection
- By: Mehmet Yilmaz
- Date: 12-21-2020


## About:
- Simple lane detection done though classical Computer Vision methods. With a combination of AOI, Thresholding, Canny, HoughLinesP, & point clustering, the detection of the left and right lane of the driving car in the video (point of view) is achieved.
- This method is NOT PERFECT as it really only works best if the video data is clean, there are no objects/cars in the AOI, and the road is not so broken down.
- Dispite it's short commings, this method does remove most of the noise in a frame and has the protentional of being a more efficient lane detection system.


## Stretch Goals:
- Implement more advance methods using Convolutional Neural Networks (CNN).
- Find other, better, methods for isolating lanes. Such as HSV thresholding.
- Apply object detection for detecting cars and none road-like objects.


## Preview:
![SLD-preview](https://user-images.githubusercontent.com/15916367/102777441-d335e700-434d-11eb-8f0b-a4ec1089d4dd.gif)


## Papers Read:
- [Advanced lane detection technique for structural highway based on computer vision algorithm](https://www.sciencedirect.com/science/article/pii/S2214785320373302?casa_token=M4ZoLzeJwx4AAAAA:ukSK4iSWKjdMNAMMDgsUf315ZNYUahOzGfoExKCEooWribsMTM6Jo-9V-C4EwBglgmOa69tYquA)

- [Real-time Lane detection and Motion Planning in Raspberry Pi and Arduino for an Autonomous Vehicle Prototype](https://arxiv.org/pdf/2009.09391.pdf)

- [Real-Time Lane Departure Detection Based on Extended Edge-Linking Algorithm](https://ieeexplore.ieee.org/document/5489518)


## Driving Clips:
- (YouTube) Self Driving Car Complete Dataset: [[link](https://www.youtube.com/playlist?list=PLUop7b1Q1uZkv5__d2yPZG1cAXcelata8)]

- Clips Used For This Project:
	- cal_freeway: [[link](https://www.youtube.com/watch?v=eoXguTDnnHM)]
	- delihi_drive: [[link](https://www.youtube.com/watch?v=UjCFTNhZGeo&list=PLUop7b1Q1uZkv5__d2yPZG1cAXcelata8&index=89)]
	- mout_drive: [[link](https://www.youtube.com/watch?v=pvUj2M-wRHQ)]
	- missi_drive: [[link](https://www.youtube.com/watch?v=isJlndP8V9g&list=PLUop7b1Q1uZkv5__d2yPZG1cAXcelata8&index=18)]
	- toronto_way: [[link](https://www.youtube.com/watch?v=uHusTBlqlZI)]
	- toronto_longer: [[link](https://www.youtube.com/watch?v=uHusTBlqlZI)]

