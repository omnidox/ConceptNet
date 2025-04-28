
import fiftyone as fo
import fiftyone.zoo as foz

import torch, detectron2

print("PyTorch version: ", torch.__version__)
print("CUDA version: ", torch.version.cuda)


# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, cv2

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog, DatasetCatalog

from detectron2 import model_zoo
from detectron2.engine import DefaultTrainer, DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2.modeling import build_model, build_roi_heads
from detectron2.config import get_cfg

# Continuation Training of fast_rcnn but with a scheduler for optimization

from detectron2.engine import DefaultTrainer

cfg = get_cfg()
cfg.MODEL.DEVICE = "cpu"
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("fiftyone_train",)
cfg.DATASETS.TEST = ()
cfg.DATALOADER.NUM_WORKERS = 2

# Point to the saved checkpoint from the previous training session
cfg.MODEL.WEIGHTS = "models/model_final_2.pth"

cfg.SOLVER.IMS_PER_BATCH = 4
cfg.SOLVER.BASE_LR = 0.01
cfg.SOLVER.MAX_ITER = 60000
cfg.SOLVER.STEPS = []
cfg.SOLVER.GAMMA = 0.1
cfg.SOLVER.WARMUP_ITERS = 800
cfg.SOLVER.LR_SCHEDULER_NAME = "WarmupCosineLR"
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 512
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 80
# cfg.OUTPUT_DIR = "/content/drive/MyDrive/faster_rcnn/Weights_2"

cfg.SOLVER.CHECKPOINT_PERIOD = 20000

import torch

# Load the model checkpoint
checkpoint = torch.load(os.path.join(cfg.OUTPUT_DIR, "models/model_final_2.pth"), map_location=torch.device('cpu'))

# Extract the number of iterations
iterations = checkpoint['iteration']

print(f"The model was trained for {iterations} iterations.")

cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5


cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "models/model_final_2.pth")  # path to the model we just trained
predictor = DefaultPredictor(cfg)


# import fiftyone as fo


# export_dir = "/content/drive/MyDrive/Alpha_dataset_02"
export_dir = "alpha_dataset_02/Alpha_dataset_02"

# Import the dataset
imported_dataset = fo.Dataset.from_dir(
    dataset_dir=export_dir,
    dataset_type=fo.types.FiftyOneDataset,
    name="imported_dataset_name",
    overwrite=True  # Overwrite existing dataset
)

# Get the list of classes for the "ground_truth" field
GT_Classes = imported_dataset.distinct("ground_truth.detections.label")

# Print the classes
print(GT_Classes)

classes = ['adhesive_tape', 'apple', 'artichoke', 'ball', 'balloon', 
           'banana', 'beer', 'bell_pepper', 'belt', 'book', 'boot', 
           'bottle', 'bowl', 'box', 'broccoli', 'cake', 'calculator', 
           'camera', 'candle', 'carrot', 'cheese', 'chopsticks', 'clock', 
           'clothing', 'coin', 'computer_mouse', 'cookie', 'cucumber', 'dice', 
           'doughnut', 'drinking_straw', 'flower', 'flying_disc', 
           'garden_asparagus', 'glove', 'grape', 'handbag', 'hat', 
           'high_heels', 'juice', 'knife', 'lemon', 'mobile_phone', 'muffin', 
           'mug', 'mushroom', 'orange', 'oyster', 'pastry', 'peach', 'pear', 
           'pen', 'pencil_case', 'plastic_bag', 'platter', 'popcorn', 'potato', 
           'pretzel', 'radish', 'remote_control', 'roller_skates', 'ruler', 
           'saucer', 'scarf', 'scissors', 'shirt', 'shorts', 'skirt', 'sock', 
           'spoon', 'stapler', 'strawberry', 'swimwear', 'tablet_computer', 
           'teddy_bear', 'tie', 'towel', 'watch', 'wine', 'zucchini']

num_classes = len(classes)
print("Number of classes: ", num_classes)

# Empty Polygon Error correction for fiftyone.
from detectron2.structures import BoxMode


for d in ["train", "val"]:
    MetadataCatalog.get("fiftyone_" + d).set(thing_classes=classes)

metadata = MetadataCatalog.get("fiftyone_train")

from IPython.display import display, Javascript, Image
from base64 import b64decode, b64encode
import numpy as np
import PIL
import io
import html
import time
import os
import random
import matplotlib.pyplot as plt

from detectron2.structures import BoxMode
from detectron2.data import DatasetCatalog, MetadataCatalog
import matplotlib.image as mpimg
from matplotlib.pyplot import imshow
import cv2
import json
import requests
import gzip
import base64



def classify_objects(objects_list, frame, color_image):
    for object_info in objects_list:
        class_name = object_info["class_name"]
        object_id = object_info["object_id"]
        box = object_info["box"]

        corners = []

        centerx = (box[0] + box[2])/2
        centery = (box[1] + box[3])/ 2
        corners.append(centerx)
        corners.append(centery)

        depth_meters = frame.get_distance(int(corners[0]), int(corners[1]))
        point = rs.rs2_deproject_pixel_to_point(depth_intrinsics, [int(corners[0]), int(corners[1])], depth_meters)
        if (point[0] == 0 and point[1] == 0 and point[2] == 0):
            print("points are zero")
        else:
            point_stamped.point.x = point[0]
            point_stamped.point.y = point[1]
            point_stamped.point.z = point[2]

            marker = Marker()
            marker.header.frame_id = "image"
            marker.type = Marker.TEXT_VIEW_FACING
            marker.action = Marker.ADD
            marker.pose.position.x = point_stamped.point.x 
            marker.pose.position.y = point_stamped.point.y 
            marker.pose.position.z = point_stamped.point.z 
            marker.text = class_name


            image_new = Image()
            image_new = bridge.cv2_to_imgmsg(color_image, "bgr8")
            image_new.header.frame_id = "image"
            publisher.publish(image_new)
            publisher2.publish(camera_info)
            publisher3.publish(marker)


        scores = {
            category: score_dict[category].get(class_name, 0) * 100
            for category in score_dict
        }

        if all(score == 0 for score in scores.values()):
            scores["Misc"] = 100

        print(f"Class Name: {class_name}")
        print(f"Object ID: {object_id}")
        print(f"Box: {box}")
        for category, score in scores.items():
            if score != 0:
                print(f"{category}: {score}%")
        print("\n")

    print("---------------------------------------------------")

# def classify_objects(objects_list, frame, color_image):
#     for object_info in objects_list:
#         class_name = object_info["class_name"]
#         object_id = object_info["object_id"]
#         segmentation = object_info["segmentation"]
#         box = object_info["box"]

#         corners = []

#         centerx = (box[0] + box[2])/2
#         centery = (box[1] + box[3])/ 2
#         corners.append(centerx)
#         corners.append(centery)

#         depth_meters = frame.get_distance(int(corners[0]), int(corners[1]))
#         point = rs.rs2_deproject_pixel_to_point(depth_intrinsics, [int(corners[0]), int(corners[1])], depth_meters)
#         if (point[0] == 0 and point[1] == 0 and point[2] == 0):
#             print("points are zero")
#         else:
#             point_stamped.point.x = point[0]
#             point_stamped.point.y = point[1]
#             point_stamped.point.z = point[2]

#         marker = Marker()
#         marker.header.frame_id = "image"
#         marker.type = Marker.TEXT_VIEW_FACING
#         marker.action = Marker.ADD
#         marker.pose.position.x = point_stamped.point.x 
#         marker.pose.position.y = point_stamped.point.y 
#         marker.pose.position.z = point_stamped.point.z 
#         marker.text = class_name


#         image_new = Image()
#         image_new = bridge.cv2_to_imgmsg(color_image, "bgr8")
#         image_new.header.frame_id = "image"
#         publisher.publish(image_new)
#         publisher2.publish(camera_info)
#         publisher3.publish(marker)

#         scores = {
#             category: score_dict[category].get(class_name, 0) * 100
#             for category in score_dict
#         }

#         if all(score == 0 for score in scores.values()):
#             scores["Misc"] = 100

#         print(f"Class Name: {class_name}")
#         print(f"Object ID: {object_id}")
#         print(f"Box: {box}")
#         print(f"center corners", corners)
#         print("this is the depth", depth_meters)
#         print(f"Segmentation: {segmentation}")
#         for category, score in scores.items():
#             if score != 0:
#                 print(f"{category}: {score}%")
#         print("\n")
#     print("---------------------------------------------------")




def generate_objects_list(outputs, cfg):
    instances = outputs["instances"]

    metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
    class_catalog = metadata.thing_classes
    return [{
        "class_name": class_catalog[instances.pred_classes[idx]],
        "object_id": idx,
        "box": coordinates.tolist()
    } for idx, coordinates in enumerate(instances.pred_boxes.tensor)]


score_dict = {
    "Fruit": {
        'Apple': 0.98, 'Orange': 0.46, 'Peach': 0.62, 'Strawberry': 0.92,
        'Grape': 0.96, 'Pear': 0.91, 'Banana': 0.95, 'Carrot': 0.88,
        'Pepper': 0.82, 'Cucumber': 0.91, 'Zucchini': 0.97,
        'Radish': 0.76, 'Artichoke': 0.7, 'Cheese': 0.75
    },
    "Drink": {
        'Bottle': 0.66, 'Beer': 0.82, 'Juice': 0.73, 'Wine': 0.84,
        'Mug': 0.96, 'Spoon': 0.46, 'Saucer': 0.46, 'Hat': 0.46,
    },
    "Vegetable": {
        'Strawberry': 0.7, 'Banana': 0.76, 'Carrot': 0.97, 'Pepper': 0.7,
        'Cucumber': 0.88, 'Broccoli': 0.82, 'Garden Asparagus': 0.91,
        'Zucchini': 0.89, 'Artichoke': 0.75, 'Mushroom': 0.76,
        'Potato': 0.91, 'Cheese': 0.7
    },
    "Snacks": {'Apple': 0.69, 'Banana': 0.78, 'Popcorn': 0.89, 'Muffin': 0.84},
    "Stationery": {
        'Pen': 0.87, 'Adhesive tape': 0.67, 'Stapler': 0.67,
        'Ruler': 0.81, 'Calculator': 0.58, 'Box': 0.96, 'Clock': 0.67
    },
    "Toys": {'Ball': 0.75, 'Flying disc': 0.46, 'Teddy bear': 0.87},
    "Tableware": {
        'Orange': 0.83, 'Plate': 0.64, 'Knife': 0.46, 'Spoon': 0.46, 'Saucer': 0.46, 'Chopsticks': 0.58
    }
}

import cv2
import pyrealsense2 as rs
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
import rospy
from geometry_msgs.msg import PointStamped, Point
from cv_bridge import CvBridge, CvBridgeError
#import tf2_geometry_msgs
import tf
from std_msgs.msg import String
from visualization_msgs.msg import Marker


bridge = CvBridge()

rospy.init_node('object_locations')
publisher = rospy.Publisher("/image_raw", Image,queue_size=10)
publisher2 = rospy.Publisher("/image_info", CameraInfo,queue_size=10)
publisher3 = rospy.Publisher('/object', Marker, queue_size=10)

# Initialize the webcam
#cap = cv2.VideoCapture(0)
try:
    pipeline = rs.pipeline()

    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  

    # config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    # config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)


    align_to = rs.stream.color
    align = rs.align(align_to)

    # Start streaming
    profile = pipeline.start(config)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    print("Depth Scale is: " , depth_scale)
    while True:
        # Capture frame-by-frame
        #ret, img = cap.read()

        #if not ret:
            #break
        point_stamped = PointStamped()
        point_stamped.header.frame_id = 'objects'
        point_stamped.header.stamp = rospy.Time.now()
        camera_info = CameraInfo()
        camera_info.header.frame_id = 'image_info'
        camera_info.height = 480
        camera_info.width = 640
        camera_info.distortion_model = 'Inverse Brown Conrady'
        camera_info.D = [0.0, 0.0, 0.0, 0.0, 0.0]
        camera_info.K = [383.243988037109, 0, 320.187683105469, 0, 383.243988037109, 237.547302246094, 0, 0, 1]
        camera_info.R = [.999994, 0.00351602, -0.000546174, 
                        -0.00351723, .999991, -0.00222811, 
                        0.000538335, 0.00223001, 0.999997]
        camera_info.P = [383.243988037109, 0, 320.187683105469, 0, 0, 383.243988037109, 237.547302246094, 0, 0, 0, 1, 0]
        frames = pipeline.wait_for_frames()

        profile = pipeline.get_active_profile()
        depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
        depth_intrinsics = depth_profile.get_intrinsics()

        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image



        color_frame = aligned_frames.get_color_frame() #gets a array of bits of a colored video stream

        frame= np.asanyarray(color_frame.get_data())  #This is the image frame

        #cv2.imshow("webcam", frame)



        # Make the predictions
        outputs = predictor(frame)

        from detectron2.layers import nms

        # Extract bounding boxes and scores
        boxes = outputs["instances"].pred_boxes.tensor
        scores = outputs["instances"].scores

        # Apply class-agnostic NMS
        from detectron2.layers import nms
        keep = nms(boxes, scores.max(dim=1)[0] if len(scores.shape) == 2 else scores, iou_threshold=0.01)

        # Retain only the bounding boxes and class predictions that pass NMS
        outputs["instances"] = outputs["instances"][keep]

        # If scores tensor is two-dimensional, find max score and its class for each box
        if len(scores.shape) == 2:
            max_scores, max_classes = scores[keep].max(dim=1)
        else:
            max_scores = scores[keep]
            max_classes = outputs["instances"].pred_classes

        # Update the outputs with the highest confidence class predictions
        outputs["instances"].scores = max_scores
        outputs["instances"].pred_classes = max_classes



        objects_list = generate_objects_list(outputs, cfg)
        classify_objects(objects_list, aligned_depth_frame, frame)

        v = Visualizer(frame[:, :, ::-1],
                    metadata=metadata,
                    scale=1.0)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

        # Display the resulting frame
        cv2.imshow('Webcam', out.get_image()[:, :, ::-1])

        # Break the loop on 'q' key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):

            break

    # When everything is done, release the capture
    cv2.destroyAllWindows()
except Exception as e:
        print(e)

