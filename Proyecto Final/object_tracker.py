"""
Healthy distance analyzer. Team 4.

José Francisco Pacheco A01373488
Uriel Fuentes A00820592
Eloy Hernández A01066325
Yasuo Ignacio Maidana A01328427

This programs analyze a video feed and outputs a video with 
people that do not have a healthy distance between them bounded
by a red box. A red line conects the pairs of persons that do not have
healthy distance. The time the persons have spent with no healthy distance 
is also shown. 
"""

import time, random
import numpy as np
from absl import app, flags, logging
from absl.flags import FLAGS
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny
)
from yolov3_tf2.dataset import transform_images
from yolov3_tf2.utils import draw_outputs, convert_boxes

from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
from PIL import Image

flags.DEFINE_string('classes', './data/labels/coco.names', 'path to classes file')
flags.DEFINE_string('weights', './weights/yolov3.tf',
                    'path to weights file')
flags.DEFINE_boolean('tiny', False, 'yolov3 or yolov3-tiny')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_string('video', './data/video/test.mp4',
                    'path to video file or number for webcam)')
flags.DEFINE_string('output', None, 'path to output video')
flags.DEFINE_string('output_format', 'XVID', 'codec used in VideoWriter when saving video to file')
flags.DEFINE_integer('num_classes', 80, 'number of classes in the model')

angle_factor = 0.8

#Method to determine healthy distance presence

def isclose(p1,p2):

    #Select width and height for analysis
    if(p1[1]<p2[1]):
        a_w = p1[0]
        a_h = p1[1]
    else:
        a_w = p2[0]
        a_h = p2[1]
    
    #Get horizontal and vertical separation
    d_hor = abs(p2[2][0]-p1[2][0])
    d_ver = abs(p2[2][1]-p1[2][1])
    
    #Calculate threshold values  
    vc_calib_hor = a_w*1.3
    vc_calib_ver = a_h*0.4*angle_factor
    
    #Determine healthy distance presence
    if (0<d_hor<vc_calib_hor and 0 < d_ver < vc_calib_ver):
        return 1
    else:
        return 0
        
def main(_argv):
    # Definition of the parameters
    max_cosine_distance = 0.5
    nn_budget = None
    nms_max_overlap = 1.0
    
    #initialize deep sort
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)

    yolo = YoloV3(classes=FLAGS.num_classes)

    yolo.load_weights(FLAGS.weights)
    logging.info('weights loaded')

    class_names = [c.strip() for c in open(FLAGS.classes).readlines()]
    logging.info('classes loaded')

    try:
        vid = cv2.VideoCapture(int(FLAGS.video))
    except:
        vid = cv2.VideoCapture(FLAGS.video)

    out = None

    if FLAGS.output:
        # by default VideoCapture returns float instead of int
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fpsT = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
        out = cv2.VideoWriter(FLAGS.output, codec, fpsT/2, (width, height))
        frame_index = -1 
    
    timeFrame = 1 / fpsT
    fps = 0.0
    count = 0 
    
    timeClose = {}
    
    while True:
        _, img = vid.read()

        if img is None:
            logging.warning("Empty Frame")
            time.sleep(0.1)
            count+=1
            if count < 3:
                continue
            else: 
                break
        
        #Format image to feed YOLO
        img_in = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        img_in = tf.expand_dims(img_in, 0)
        img_in = transform_images(img_in, FLAGS.size)
        
        boxes, scores, classes, nums = yolo.predict(img_in)
        classes = classes[0]
        names = []
        for i in range(len(classes)):
            names.append(class_names[int(classes[i])])
        names = np.array(names)
        converted_boxes = convert_boxes(img, boxes[0])
        features = encoder(img, converted_boxes)    
        detections = [Detection(bbox, score, class_name, feature) for bbox, score, class_name, feature in zip(converted_boxes, scores[0], names, features)]
        
        # run non-maxima suppresion
        boxs = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        classes = np.array([d.class_name for d in detections])
        indices = preprocessing.non_max_suppression(boxs, classes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]        

        # Call the tracker
        tracker.predict()
        tracker.update(detections)

        personsBoxes = []
        personsID = []

        #Get data of the bounding boxes of people in the image and their IDs. 
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            if track.get_class() == "person":
                box = track.to_tlbr()
                personsBoxes.append([int(box[0]),int(box[1]),int(box[2]),int(box[3])])
                personsID.append(track.track_id)


        status = []
        close_pair = []
        center = []
        obj_info = []
            
        for person in range(len(personsID)):

            #Get dada needed for the close distance analysis
            (x, y) = (personsBoxes[person][0], personsBoxes[person][1])
            (w, h) = (personsBoxes[person][2] - x, personsBoxes[person][3] - y)
            cen = [int(x + w / 2), int(y + h / 2)]
            center.append(cen)
            obj_info.append([w, h, cen])
            status.append(0)

        #Analyze each pair of people in the image to determine if they have a healthy distance
        for i in range(len(obj_info)):
            for j in range(i+1, len(obj_info)):
              g = isclose(obj_info[i],obj_info[j])
              #If pair of people do not have healthy distance record it. 
              if g == 1:
                status[i] = 1
                status[j] = 1
                
                #Update the time each person has not have healthy distance
                if str(personsID[i]) in timeClose:
                    timeClose[str(personsID[i])] = timeClose[str(personsID[i])] + timeFrame
                else: 
                    timeClose[str(personsID[i])] = timeFrame
                if str(personsID[j]) in timeClose:
                    timeClose[str(personsID[j])] = timeClose[str(personsID[j])] + timeFrame
                else: 
                    timeClose[str(personsID[j])] = timeFrame
                
                #Draw the line between the persons. 
                cv2.line(img, tuple(obj_info[i][2]), tuple(obj_info[j][2]), (0, 0, 255), 2)
        
        #For each person in the image that do not has healthy distance draw red bounding box and show ID and time. 
        for i in range(len(status)):
            if status[i] == 1:
                cv2.rectangle(img, (personsBoxes[i][0], personsBoxes[i][1]), (personsBoxes[i][2], personsBoxes[i][3]), (0, 0, 255), 2)
                cv2.rectangle(img, (personsBoxes[i][0], personsBoxes[i][1] - 30), (personsBoxes[i][0]+(len("person")+len(str(personsID[i])))*17 + 7 * 17, personsBoxes[i][1]), (0, 0, 255), -1)
                cv2.putText(img, "person-" + str(personsID[i]) + " t= {:.2f}".format(timeClose[str(personsID[i])]),(personsBoxes[i][0], personsBoxes[i][1]-10),0, 0.75, (255,255,255),2)
        
        #Make filter for box of the title
        sub_img = img[20:150, 40:1120]
        black_rect = np.ones(sub_img.shape, dtype=np.uint8) * 0
        res = cv2.addWeighted(sub_img, 0.50, black_rect, 0.50, 1.0)
        img[20:150, 40:1120] = res
        
        #Write title
        cv2.putText(img, "Analizador de Sana Distancia. Equipo 4. Uriel, Eloy, Yasuo y Jose. ", (50, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, "Los rectangulos rojos senalan personas sin sana distancia.", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2) 
        cv2.putText(img, "Las lineas rojas unen pares de personas sin sana distancia.", (50, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2) 
        cv2.imshow('output', img)

        if FLAGS.output:
            out.write(img)
            
        # press q to quit
        if cv2.waitKey(1) == ord('q'):
            break
            
    vid.release()
    
    if FLAGS.ouput:
        out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
