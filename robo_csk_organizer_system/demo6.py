# -*- coding: utf-8 -*-
"""demo2.py

This file is a conversion of the original demo.ipynb file located at
https://colab.research.google.com/github/salesforce/BLIP/blob/main/demo.ipynb

# BLIP: Inference Demo
 - [Image Captioning](#Image-Captioning)
 - [VQA](#VQA)
 - [Feature Extraction](#Feature-Extraction)
 - [Image Text Matching](#Image-Text-Matching)
"""

# install requirements
import sys
import cv2
import numpy as np

from PIL import Image
import requests
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
import pyrealsense2 as rs
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import CameraInfo


import rospy
import tf
import moveit_commander
#import geometry_msgs.msg
#import moveit_msgs.msg
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Pose, Point, Quaternion, PoseArray
from moveit_msgs.msg import Constraints, OrientationConstraint, RobotTrajectory
from control_msgs.msg import JointControllerState
import csv
import time

inner_left = [-0.17286183697553179, 0.3498518714782533, 0.08938334395356042, -1.6924855889772112, -0.08166645785180486, 2.037432755000581, 2.2392614062171843]
inner_right = [-0.08998131547440179, 0.3681223102275564, 0.35176773803709016, -1.6939787181424293, -0.20793655107087525, 2.0565959983682545, 2.632105155107952]
far_right = [0.23236656827884808, 0.6350597265063891, 0.3774248047711556, -1.29531910726892, -0.24970737549625796, 1.8775164473333112, 2.89170068895258]
far_left = [-0.2828344379146142, 0.5337419479938974, -0.12191653278457937, -1.3271019937130857, 0.051913634488979975, 1.8602580542932865, 1.8537054844336307]
home = [0.00026527582188645086, -0.7843304152182199, -0.00045309998436554713, -2.356442127729717, -0.0010922843198188476, 1.5716981815761988, 0.7857652555986918]

rospy.init_node('panda_arm_rafael')

moveit_commander.roscpp_initialize(sys.argv)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
move_group = MoveGroupCommander("panda_arm")
hand_group = MoveGroupCommander("hand")
end_effector_link = move_group.get_end_effector_link()
listener = tf.TransformListener()


bridge = CvBridge()
align_to = rs.stream.color
align = rs.align(align_to)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_demo_image(frame, image_size, device):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    raw_image = Image.fromarray(frame)
    transform = transforms.Compose([
        transforms.Resize((image_size,image_size),interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        ])
    image = transform(raw_image).unsqueeze(0).to(device)
    return image
# Image Captioning
# Perform image captioning using finetuned BLIP model

# from models.blip import blip_decoder
from models.blip_itm import blip_itm

image_size = 384

model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_capfilt_large.pth'

model = blip_itm(pretrained=model_url, image_size=image_size, vit='base')
model.eval()
model = model.to(device)

contexts = [
    'kitchen',
    'office',
    "playroom",
    'living room',
    'bedroom',
    'dining room',
    'pantry',
    'garden',
    'laundry room',
    'bathroom'
]

def move_left_far():
    move_group.set_joint_value_target(far_left)
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

def move_right_far():
    move_group.set_joint_value_target(far_right)
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

def move_left_inner():
    move_group.set_joint_value_target(inner_left)
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

def move_right_inner():
    move_group.set_joint_value_target(inner_right)
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

def move_home():
    move_group.set_joint_value_target(home)
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()



def record_context(frame, counter):
    if counter <= 3:
        move_left_far()
        direction = "left_outer"
    if counter > 3 and counter <= 7:
        move_left_inner()
        direction = "left_inner"
    if counter > 7 and counter <= 10:
        move_right_inner()
        direction = "right_inner"
    if counter > 10 and counter <= 13:
        move_right_far()
        direction = "right_outer"
    image = load_demo_image(frame, image_size=image_size, device=device)
    with torch.no_grad():
        image = load_demo_image(frame, image_size=image_size, device=device)
        max_score = 0
        best_context = ''
        for context in contexts:
            itm_output = model(image, context, match_head='itm')
            itm_score = torch.nn.functional.softmax(itm_output, dim=1)[:,1]
            if itm_score > max_score:
                max_score = itm_score
                best_context = context.replace(" ", "_")
        print('\nThe best matched context is "%s" with a probability of %.4f' % (best_context, max_score))
        if direction == "left_outer" and counter == 3:
            with open('contexts.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                data = [best_context, far_left[0], far_left[1], far_left[2], far_left[3], far_left[4],far_left[5],far_left[6]]
                writer.writerow(data)
        if direction == "left_inner" and counter == 7:
            with open('contexts.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                data = [best_context, inner_left[0], inner_left[1], inner_left[2], inner_left[3], inner_left[4],inner_left[5],inner_left[6]]
                writer.writerow(data)
        if direction == "right_inner" and counter == 10:
            with open('contexts.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                data = [best_context, inner_right[0], inner_right[1], inner_right[2], inner_right[3], inner_right[4],inner_right[5],inner_right[6]]
                writer.writerow(data)
        if direction == "right_outer" and counter == 13:
            with open('contexts.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                data = [best_context, far_right[0], far_right[1], far_right[2], far_right[3], far_right[4],far_right[5],far_right[6]]
                writer.writerow(data)
try:
    pipeline = rs.pipeline()

    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    profile = pipeline.start(config)

    start_time = time.time()
    move_home()
    counter = 0 
    while True:
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
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame() #gets a array of bits of a colored video stream
        frame= np.asanyarray(color_frame.get_data())  #This is the image frame
        cv2.imshow("new_frame", frame)
        record_context(frame, counter)
        counter += 1

        if counter == 14:
            move_home()
            exit()
        
            
        
        key = cv2.waitKey(1)
        
        if key == ord('q'):  # Press 'q' to quit
            break

    cv2.destroyAllWindows()
                
        
except Exception as e:
        print(e)