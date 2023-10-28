# object_detection_on_tray
identify the free cavity on the tray 


## Getting Started

System contains 4 python files, 1 trained model file and 2 folders. 
I have used LeNet Convolutional Neural Networks and Keras.

### Prerequisites
```
Keras
Scikit
cv2
matplotlib
imutils

```

### Installing
I have already trained the model so you can direcly use it.
```
mymodel.h5
```
You can also train you own network by running "train_network.py"
to train you own network you have to add images to images/notes and images/not_notes (There were many of my personal images so I did not upload it)
```
run: train_network.py
```
Testing the network. Add testing images to "examples/" and to run test.py give command line argument like below:
```
python test_network.py --image examples/image_name.jpg
```
To Delete the image from the desired folder change the path from delete_images.py and directly run the file
```
python delete_images.py
```

## Built With

* [Keras](https://keras.io/) - Deep Leanring framework
* [LeNet](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf/) - Research Paper

## Examples
<img src="[https://github.com/milanchodavadiya19/Exam_Notes_Detection/blob/main/test1.JPG](https://github.com/milanchodavadiya19/object_detection_on_tray-main/blob/main/freecavity/detected_result/8RKATQZ-detected-boxes.jpg)https://github.com/milanchodavadiya19/object_detection_on_tray-main/blob/main/freecavity/detected_result/8RKATQZ-detected-boxes.jpg">
<!-- <img src="https://github.com/milanchodavadiya19/Exam_Notes_Detection/blob/main/test2.JPG"> -->


