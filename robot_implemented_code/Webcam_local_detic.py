
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
from detectron2.data.datasets.lvis import get_lvis_instances_meta, register_lvis_instances
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


import torch
from detectron2.structures import BoxMode
from IPython.display import display, Javascript, Image
from base64 import b64decode, b64encode
import cv2
import numpy as np
import PIL
import io
import html
import time

import os
import numpy as np
import json
import random
import matplotlib.pyplot as plt

from detectron2.structures import BoxMode
from detectron2.data import DatasetCatalog, MetadataCatalog

import matplotlib.image as mpimg
from matplotlib.pyplot import imshow

import cv2
import requests
import json


import requests
import json
import gzip
import base64

from detectron2.engine import DefaultTrainer
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
    


def classify_objects(objects_list):
    for object_info in objects_list:
        class_name = object_info["class_name"]
        object_id = object_info["object_id"]
        box = object_info["box"]


        print(f"Class Name: {class_name}")
        print(f"Object ID: {object_id}")
        print(f"Box: {box}")
        print("\n")

def generate_objects_list(outputs, metadata):
    instances = outputs
    class_catalog = metadata.thing_classes
    return [{
        "class_name": class_catalog[instances.pred_classes[idx]],
        "object_id": idx,
        "box": coordinates.tolist()
    } for idx, coordinates in enumerate(instances.pred_boxes.tensor)]



import cv2

# if __name__ == "__main__":
mp.set_start_method("spawn", force=True)
args = get_parser().parse_args()
setup_logger(name="fvcore")
logger = setup_logger()
logger.info("Arguments: " + str(args))

cfg = setup_cfg(args)

demo = VisualizationDemo(cfg, args)

# Initialize the webcam
cap = cv2.VideoCapture(0)

try:
    while True:
        # Capture frame-by-frame
        ret, img = cap.read()

        if not ret:
            break

    # Make predictions on the frame
        predictions, vis_output = demo.run_on_image2(img)

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
            classify_objects(detected_objects)

        # Resize the window based on the frame's dimensions
        height, width, _ = img.shape
        cv2.resizeWindow(WINDOW_NAME, width, height)

        if cv2.waitKey(1) == 27:
            break  # esc to quit
except Exception as e:
        print(e)
finally:
    cv2.destroyAllWindows()