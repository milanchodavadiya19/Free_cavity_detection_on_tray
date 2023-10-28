import argparse
import zmq
import cv2
import numpy as np
import string
import random
import glob

# initializing size of string
N = 7

dest_folder = "/app/result"


# numpy setup
# Load Yolo
net = cv2.dnn.readNet("/app/yolov3_custom_final.weights", "/app/yolov3_custom.cfg")

# Name custom object
classes = ["FreeCavity"]

def detectCavity(imagePath, image_id):
    # _, img = cap.read()
    img = cv2.imread(imagePath)
    img = cv2.resize(img, (720, 720))

    hight, width, _ = img.shape
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

    net.setInput(blob)

    output_layers_name = net.getUnconnectedOutLayersNames()

    layerOutputs = net.forward(output_layers_name)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence = score[class_id]
            if confidence > 0.7:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * hight)
                w = int(detection[2] * width)
                h = int(detection[3] * hight)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, .5, .4)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence = score[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * hight)
                w = int(detection[2] * width)
                h = int(detection[3] * hight)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, .8, .4)
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(boxes), 3))
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label + " " + confidence, (x, y + 400), font, 2, color, 2)

    cv2.imwrite("/app/detected_result/{}-detected-boxes.jpg".format(image_id), img)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)

        # if cv2.waitKey(1) == ord('q'):
        #     break

    #cap.release()
    # cv2.destroyAllWindows()





def subscriber(ip="0.0.0.0", port=5551):
    # ZMQ connection
    url = "tcp://{}:{}".format(ip, port) 
    print("Going to bind to: {}".format(url))
    ctx = zmq.Context()
    socket = ctx.socket(zmq.SUB)
    socket.bind(url)  # subscriber creates ZeroMQ socket
    socket.setsockopt(zmq.SUBSCRIBE, ''.encode('ascii'))  # any topic
    # socket.setsockopt(zmq.SUBSCRIBE, b"")

    print("Sub bound to: {}\nWaiting for data...".format(url))

    while True:
        # using random.choices()
        # generating random strings
        print("image in process")
        import time 
        time.sleep(5)
        random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        file_path_to_save = "{}/{}.tif".format(dest_folder, random_id)
        # # wait for publisher data
        # # topic, msg = socket.recv_multipart()
        try:
            msg = socket.recv()
            print("reached msg", msg[0:50])
        except Exception as e:
            print(e.__str__)
        # print("On topic {}, received data: {}".format("kajsffg", msg[0:50]))
        if msg:
            f = open(file_path_to_save, 'wb')
            f.write(msg)
            print("wrote file at path {}", file_path_to_save)
            detectCavity(file_path_to_save, random_id)
            f.close()



if __name__ == "__main__":
    # command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=argparse.SUPPRESS,
                        help="IP of (Docker) machine")
    parser.add_argument("--port", default=argparse.SUPPRESS,
                        help="Port of (Docker) machine")

    args, leftovers = parser.parse_known_args()
    print("The following arguments are used: {}".format(args))
    print("The following arguments are ignored: {}\n".format(leftovers))

    # call function and pass on command line arguments
    subscriber(**vars(args))