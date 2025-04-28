
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

# Copyright (c) Facebook, Inc. and its affiliates.
import argparse
import glob
import multiprocessing as mp
import numpy as np
import os
import tempfile
import time
import warnings
import cv2
import tqdm
import sys
import mss

from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger

sys.path.insert(0, 'third_party/CenterNet2/')
from centernet.config import add_centernet_config
from detic.config import add_detic_config
from detectron2.data import MetadataCatalog


from detic.predictor import VisualizationDemo
from detectron2.structures import BoxMode

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
from detectron2.layers import nms

# constants
WINDOW_NAME = "Detic"

def setup_cfg(args):
    cfg = get_cfg()
    if args.cpu:
        cfg.MODEL.DEVICE="cpu"
    add_centernet_config(cfg)
    add_detic_config(cfg)
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set score_threshold for builtin models
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    cfg.MODEL.ROI_BOX_HEAD.ZEROSHOT_WEIGHT_PATH = 'rand' # load later
    if not args.pred_all_class:
        cfg.MODEL.ROI_HEADS.ONE_CLASS_PER_PROPOSAL = True
    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 demo for builtin configs")
    parser.add_argument(
        "--config-file",
        default="configs/quick_schedules/mask_rcnn_R_50_FPN_inference_acc_test.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument("--webcam", help="Take inputs from webcam.")
    parser.add_argument("--cpu", action='store_true', help="Use CPU only.")
    parser.add_argument("--video-input", help="Path to video file.")
    parser.add_argument(
        "--input",
        nargs="+",
        help="A list of space separated input images; "
        "or a single glob pattern such as 'directory/*.jpg'",
    )
    parser.add_argument(
        "--output",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )
    parser.add_argument(
        "--vocabulary",
        default="lvis",
        choices=['lvis', 'openimages', 'objects365', 'coco', 'custom'],
        help="",
    )
    parser.add_argument(
        "--custom_vocabulary",
        default="",
        help="",
    )
    parser.add_argument("--pred_all_class", action='store_true')
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=[],
        nargs=argparse.REMAINDER,
    )
    return parser


def test_opencv_video_format(codec, file_ext):
    with tempfile.TemporaryDirectory(prefix="video_format_test") as dir:
        filename = os.path.join(dir, "test_file" + file_ext)
        writer = cv2.VideoWriter(
            filename=filename,
            fourcc=cv2.VideoWriter_fourcc(*codec),
            fps=float(30),
            frameSize=(10, 10),
            isColor=True,
        )
        [writer.write(np.zeros((10, 10, 3), np.uint8)) for _ in range(30)]
        writer.release()
        if os.path.isfile(filename):
            return True
        return False

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


        print(f"Class Name: {class_name}")
        print(f"Object ID: {object_id}")
        print(f"Box: {box}")
        print("\n")

    print("---------------------------------------------------")



def generate_objects_list(outputs, metadata):
    instances = outputs
    class_catalog = metadata.thing_classes
    return [{
        "class_name": class_catalog[instances.pred_classes[idx]],
        "object_id": idx,
        "box": coordinates.tolist()
    } for idx, coordinates in enumerate(instances.pred_boxes.tensor)]


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

mp.set_start_method("spawn", force=True)
args = get_parser().parse_args()
setup_logger(name="fvcore")
logger = setup_logger()
logger.info("Arguments: " + str(args))

cfg = setup_cfg(args)
demo = VisualizationDemo(cfg, args)

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


        
    # Make predictions on the frame
        predictions, vis_output = demo.run_on_image2(frame)

        # Apply class-agnostic NMS to the predictions
        if predictions.has("pred_boxes"):
            boxes = predictions.pred_boxes.tensor
            scores = predictions.scores

            keep = nms(boxes, scores.max(dim=1)[0] if len(scores.shape) == 2 else scores, iou_threshold=0.01)
            predictions = predictions[keep]

            if len(scores.shape) == 2:
                max_scores, max_classes = scores[keep].max(dim=1)
            else:
                max_scores = scores[keep]
                max_classes = predictions.pred_classes

            predictions.scores = max_scores
            predictions.pred_classes = max_classes


        # Display the visualized frame
        vis = vis_output.get_image()[:, :, ::-1]
        cv2.imshow(WINDOW_NAME, vis)

        # Extract bounding boxes and other information from predictions
        if predictions.has("pred_boxes"):
            metadata = demo.metadata  # Use the metadata from the VisualizationDemo class
            detected_objects = generate_objects_list(predictions, metadata)
            classify_objects(detected_objects, aligned_depth_frame, frame)

        # Resize the window based on the frame's dimensions
        height, width, _ = frame.shape
        cv2.resizeWindow(WINDOW_NAME, width, height)

        if cv2.waitKey(1) == 27:
            break  # esc to quit
except Exception as e:
        print(e)
finally:
    cv2.destroyAllWindows()
#############################################################################################################


    # When everything is done, release the capture and destroy windows
#     pipeline.stop()
#     cv2.destroyAllWindows()


#         # Make the predictions
#         outputs = predictor(frame)

#         from detectron2.layers import nms

#         # Extract bounding boxes and scores
#         boxes = outputs["instances"].pred_boxes.tensor
#         scores = outputs["instances"].scores

#         # Apply class-agnostic NMS
#         from detectron2.layers import nms
#         keep = nms(boxes, scores.max(dim=1)[0] if len(scores.shape) == 2 else scores, iou_threshold=0.01)

#         # Retain only the bounding boxes and class predictions that pass NMS
#         outputs["instances"] = outputs["instances"][keep]

#         # If scores tensor is two-dimensional, find max score and its class for each box
#         if len(scores.shape) == 2:
#             max_scores, max_classes = scores[keep].max(dim=1)
#         else:
#             max_scores = scores[keep]
#             max_classes = outputs["instances"].pred_classes

#         # Update the outputs with the highest confidence class predictions
#         outputs["instances"].scores = max_scores
#         outputs["instances"].pred_classes = max_classes



#         objects_list = generate_objects_list(outputs, cfg)
#         classify_objects(objects_list, aligned_depth_frame, frame)

#         v = Visualizer(frame[:, :, ::-1],
#                     metadata=metadata,
#                     scale=1.0)
#         out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

#         # Display the resulting frame
#         cv2.imshow('Webcam', out.get_image()[:, :, ::-1])

#         # Break the loop on 'q' key press
#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('q'):

#             break

#     # When everything is done, release the capture
#     cv2.destroyAllWindows()
# except Exception as e:
#         print(e)

