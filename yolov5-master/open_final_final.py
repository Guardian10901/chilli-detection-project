
import cv2
import math
import numpy as np
import pyrealsense2 as rs
from realsense_depth import *

dc = DepthCamera()
intr = dc.get_intrinsics()
print(intr)

cap = cv2.VideoCapture(0)
net = cv2.dnn.readNetFromONNX("best.onnx")
file = open("yolov5-master/yolov5-master/class.txt","r")
classes = file.read().split('\n')
print(classes)

while True:
    ret, depth_frame, color_frame = dc.get_frame()
    

    color_image = np.asanyarray(color_frame)
    depth_image = np.asanyarray(depth_frame)
    img = color_image
       
    if img is None:
        break
       
    img = cv2.resize(img, (1000,600))
    blob = cv2.dnn.blobFromImage(img,scalefactor= 1/255,size=(640,640),mean=[0,0,0],swapRB= True, crop= False)
    net.setInput(blob)
    detections = net.forward()[0]
  

    # cx,cy , w,h, confidence, 80 class_scores
    # class_ids, confidences, boxes

    classes_ids = []
    confidences = []
    boxes = []
    rows = detections.shape[0]

    img_width, img_height = img.shape[1], img.shape[0]
    x_scale = img_width/640
    y_scale = img_height/480
    

    for i in range(rows):
        row = detections[i]
        confidence = row[4]
        if confidence > 0.5:
            classes_score = row[5:]
            ind = np.argmax(classes_score)
            if classes_score[ind] > 0.5:
                classes_ids.append(ind)
                confidences.append(confidence)
                cx, cy, w, h = row[:4]
                x1 = int((cx- w/2)*x_scale)
                y1 = int((cy-h/2)*y_scale)
                width = int(w * x_scale)
                height = int(h * y_scale)
                box = np.array([x1,y1,width,height])
                boxes.append(box)

    indices = cv2.dnn.NMSBoxes(boxes,confidences,0.5,0.5)

    for i in indices:
        x1,y1,w,h = boxes[i]
        label = classes[classes_ids[i]]
        conf = confidences[i]
        text = label + "{:.2f}".format(conf)
        y2=y1-h/2
        point = (x1,y1)
        
        depth_value = dc.get_depth(x1, y1)*1000
        Xtemp = depth_value*(x1 -intr.ppx)/intr.fx
        Ytemp = depth_value*(y1 -intr.ppy)/intr.fy
        Ztemp = depth_value

        Xtarget = Xtemp - 35 #35 is RGB camera module offset from the center of the realsense
        Ytarget = -(Ztemp*math.sin(0) + Ytemp*math.cos(0))
        Ztarget = Ztemp*math.cos(0) + Ytemp*math.sin(0)

       
              # cv2.circle(color_frame, point, 4, (0, 0, 255)) # type: ignore
        #distance = depth_frame[point[1], point[0]]
        print(int(Xtarget),int(Ytarget),int(depth_value))
        #
        #text = label + "{:.2f}".format(conf) + point
        #
        cv2.rectangle(img,(x1,y1),(x1+w,y1+h),(255,0,0),2)
        cv2.putText(img, text, (x1,y1-2),cv2.FONT_HERSHEY_COMPLEX, 0.7,(255,0,255),2)
        break

    cv2.imshow("VIDEO",img)
    k = cv2.waitKey(5)
    if k == ord('q'):
        break

