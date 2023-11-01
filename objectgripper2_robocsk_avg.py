import rospy
import tf
import moveit_commander
import geometry_msgs.msg
from geometry_msgs.msg import Pose, Point, Quaternion, PoseArray
from std_msgs.msg import String, Float64MultiArray
from visualization_msgs.msg import Marker
import numpy as np
from sensor_msgs.msg import JointState
import sys
import threading
import pandas as pd
import json
import time




child_frame = []
fifth_joint = 0
list_filled_event = threading.Event()
unprompted = True


# New function to set robot focus
def set_robot_focus(path_info, focus_contexts, degree_reduction=0, weight_multiplier=1.5):
    path, average_weight, degree_of_separation = path_info
    for edge in path:
        if edge[0] in focus_contexts:
            # print(f"Adjusting for focus context: {edge[0]}") 

            # degree_of_separation = max(1, degree_of_separation - degree_reduction)  # Ensure it doesn't go below 1

            degree_of_separation -= degree_reduction
            average_weight *= weight_multiplier
            break
    return (path, average_weight, degree_of_separation)



def get_object_context(data, object_name, desired_contexts=None, focus_contexts=[]):

    # Start timing for the first implementation
    start_time_1 = time.time()
    """
    Given the data, an object name, and an optional list of desired contexts,
    return its most relevant context along with the path, weight, and degree of separation.
    """
    # If no specific contexts are provided, consider all available contexts
    if desired_contexts is None:
        desired_contexts = ["kitchen", "office", "child's_bedroom", "living_room", "bedroom", 
                            "dining_room", "pantry", "garden", "laundry_room"]
    
    # If the object isn't present in the data, return a message indicating that
    if object_name not in [key.split(':')[1] for key in data]:
        return f"No paths found for {object_name}"
    
    # Gather paths relevant to the object
    relevant_paths = []
    for key, paths_list in data.items():
        loc, obj = key.split(':')

        # Remove the '/c/en/' prefix from the object name
        obj = obj.split('/')[0]

        # Only consider paths that have the desired context
        if obj == object_name and loc in desired_contexts:
            relevant_paths.extend(paths_list)

    # Exclude paths that have any edge labeled 'Synonym'
    relevant_paths = [path for path in relevant_paths if not any(edge[1] == 'Synonym' for edge in path[0])]

    # # Exclude paths that have any edge labeled 'RelatedTo' with a weight less than 2
    # relevant_paths = [path for path in relevant_paths if not any(edge[1] == 'RelatedTo' and edge[2] < 2 for edge in path[0])]


    # Calculate the average weight for each path based on the robot's focus
    for i, (path, _) in enumerate(relevant_paths):
        # Calculate the average weight for the path
        total_weight = sum(edge[2] for edge in path)
        average_weight = total_weight / len(path)
        degree_of_separation = len(path)

        # Adjust the average weight and degree of separation based on the robot's focus
        if focus_contexts:
            path_info = set_robot_focus((path, average_weight, degree_of_separation), focus_contexts)
        else:
            path_info = (path, average_weight, degree_of_separation)
        
        relevant_paths[i] = path_info


    # Sort the paths by average weight
    sorted_paths = sorted(relevant_paths, key=lambda x: -x[1])[:20]


    # The most relevant location and details will be from the first path in the sorted list
    if sorted_paths:
        most_relevant_path, weight, degree_of_separation = sorted_paths[0]
        context = most_relevant_path[0][0]
        
        # Create a readable path for display
        path_elements = []
        for edge in most_relevant_path:
            if edge[1] in ['IsA', 'AtLocation']:
                arrow = " <- "
            else:
                arrow = " -> "
            path_elements.append(f"{edge[0]} ({edge[1]}){arrow}")
        readable_path = ''.join(path_elements) + object_name

           
        # End timing for the first implementation
        end_time_1 = time.time()

        execution_time_1 = end_time_1 - start_time_1
        print(f"Execution time for the robo-csk implementation: {execution_time_1:.4f} seconds")

        
        return context, readable_path, weight, degree_of_separation
    else:

           
        # End timing for the first implementation
        end_time_1 = time.time()

        execution_time_1 = end_time_1 - start_time_1
        print(f"Execution time for the first implementation: {execution_time_1:.4f} seconds")

        return f"No paths found for {object_name}", None, None, None
 

def callback(msg):
    # Define the callback function to handle the incoming messages
    counter = 0
    while counter < 4:
        if msg.text not in child_frame:
            child_frame.append(msg.text)
        counter += 1
    list_filled_event.set()
    #print(child_frame)

def joint_callback(msg):
    global fifth_joint
    fifth_joint = msg.position[4]
    #print(fifth_joint)
def move_forward(rot, trans, z):

    move_group.set_start_state_to_current_state()
    start_pose = move_group.get_current_pose().pose
    obj_pose = geometry_msgs.msg.Pose()
    obj_pose.position.x = (trans[0])
    obj_pose.position.y = (trans[1])
    obj_pose.position.z = z
    obj_pose.orientation.x = rot[0]
    obj_pose.orientation.y = rot[1]
    obj_pose.orientation.z = rot[2]
    obj_pose.orientation.w = rot[3]

    print(obj_pose.position.x)

    waypoints = [start_pose, obj_pose]
    end_effector_point = waypoints[-1]
    prev_point = waypoints[-2]
    end_effector_pose = Pose()
    end_effector_pose.position.x = (end_effector_point.position.x*.75)
    end_effector_pose.position.y = end_effector_point.position.y
    end_effector_pose.position.z = z
    prev_point_orientation = prev_point.orientation
    end_effector_pose.orientation.x = prev_point_orientation.x
    end_effector_pose.orientation.y = prev_point_orientation.y
    end_effector_pose.orientation.z = prev_point_orientation.z
    end_effector_pose.orientation.w = prev_point_orientation.w
    waypoints[-1] = end_effector_pose

    move_group.set_pose_target(waypoints[-1])
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()
    rospy.sleep(6)

def move_up(rot, trans):
    move_group.set_start_state_to_current_state()
    start_pose = move_group.get_current_pose().pose
    obj_pose = geometry_msgs.msg.Pose()
    obj_pose.position.x = (trans[0])
    obj_pose.position.y = (trans[1])
    obj_pose.position.z = (trans[2] + .45)
    obj_pose.orientation.x = rot[0]
    obj_pose.orientation.y = rot[1]
    obj_pose.orientation.z = rot[2]
    obj_pose.orientation.w = rot[3]

    print(obj_pose.position.x)

    waypoints = [start_pose, obj_pose]
    end_effector_point = waypoints[-1]
    prev_point = waypoints[-2]
    end_effector_pose = Pose()
    end_effector_pose.position.x = (end_effector_point.position.x * .70)
    end_effector_pose.position.y = end_effector_point.position.y
    end_effector_pose.position.z = (end_effector_point.position.z)
    prev_point_orientation = prev_point.orientation
    end_effector_pose.orientation.x = prev_point_orientation.x
    end_effector_pose.orientation.y = prev_point_orientation.y
    end_effector_pose.orientation.z = prev_point_orientation.z
    end_effector_pose.orientation.w = prev_point_orientation.w
    waypoints[-1] = end_effector_pose

    move_group.set_pose_target(waypoints[-1])
    plan = move_group.plan()
    plan_traj = plan[1]
    move_group.execute(plan_traj, wait=True)
    move_group.stop()
    move_group.clear_pose_targets()
    rospy.sleep(10)

def move_down2(rot, trans):
    move_group.set_start_state_to_current_state()
    start_pose = move_group.get_current_pose().pose
    obj_pose = geometry_msgs.msg.Pose()
    obj_pose.position.x = (trans[0])
    obj_pose.position.y = (trans[1])
    obj_pose.position.z = (trans[2]+ .038) #might need to be adjusted for certain items
    obj_pose.orientation.x = rot[0]
    obj_pose.orientation.y = rot[1]
    obj_pose.orientation.z = rot[2]
    obj_pose.orientation.w = rot[3]
    print("before the ifs, fifth joint: ", fifth_joint)
    print(obj_pose.position.z)
    if fifth_joint > .03:
        print("fifth joint right: ", fifth_joint)
        waypoints = [start_pose, obj_pose]
        end_effector_point = waypoints[-1]
        prev_point = waypoints[-2]
        end_effector_pose = Pose()
        end_effector_pose.position.x = (end_effector_point.position.x - .05)#.05
        end_effector_pose.position.y = (end_effector_point.position.y + .016)#.012
        end_effector_pose.position.z = (end_effector_point.position.z)
        prev_point_orientation = prev_point.orientation
        end_effector_pose.orientation.x = prev_point_orientation.x
        end_effector_pose.orientation.y = prev_point_orientation.y
        end_effector_pose.orientation.z = prev_point_orientation.z
        end_effector_pose.orientation.w = prev_point_orientation.w
        waypoints[-1] = end_effector_pose

        move_group.set_pose_target(waypoints[-1])
        plan = move_group.plan()
        plan_traj = plan[1]
        move_group.execute(plan_traj, wait=True)
        move_group.stop()
        move_group.clear_pose_targets()
        rospy.sleep(5)
    elif fifth_joint < -.03:
        print("fifth joint left: ", fifth_joint)
        waypoints = [start_pose, obj_pose]
        end_effector_point = waypoints[-1]
        prev_point = waypoints[-2]
        end_effector_pose = Pose()
        end_effector_pose.position.x = (end_effector_point.position.x - .05)
        end_effector_pose.position.y = (end_effector_point.position.y + .05)
        end_effector_pose.position.z = (end_effector_point.position.z)
        prev_point_orientation = prev_point.orientation
        end_effector_pose.orientation.x = prev_point_orientation.x
        end_effector_pose.orientation.y = prev_point_orientation.y
        end_effector_pose.orientation.z = prev_point_orientation.z
        end_effector_pose.orientation.w = prev_point_orientation.w
        waypoints[-1] = end_effector_pose

        move_group.set_pose_target(waypoints[-1])
        plan = move_group.plan()
        plan_traj = plan[1]
        move_group.execute(plan_traj, wait=True)
        move_group.stop()
        move_group.clear_pose_targets()
        rospy.sleep(5)
    else:
        waypoints = [start_pose, obj_pose]
        end_effector_point = waypoints[-1]
        prev_point = waypoints[-2]
        end_effector_pose = Pose()
        end_effector_pose.position.x = (end_effector_point.position.x - .05)
        end_effector_pose.position.y = (end_effector_point.position.y + .027)
        end_effector_pose.position.z = (end_effector_point.position.z)
        prev_point_orientation = prev_point.orientation
        end_effector_pose.orientation.x = prev_point_orientation.x
        end_effector_pose.orientation.y = prev_point_orientation.y
        end_effector_pose.orientation.z = prev_point_orientation.z
        end_effector_pose.orientation.w = prev_point_orientation.w
        waypoints[-1] = end_effector_pose

        move_group.set_pose_target(waypoints[-1])
        plan = move_group.plan()
        plan_traj = plan[1]
        move_group.execute(plan_traj, wait=True)
        move_group.stop()
        move_group.clear_pose_targets()
        rospy.sleep(5)

if __name__ == "__main__":
    rospy.init_node('Rafael_panda_move')
    rospy.Subscriber('/object', Marker, callback)
    rospy.Subscriber('/joint_states', JointState, joint_callback)
    moveit_commander.roscpp_initialize(sys.argv)
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group_name = "panda_arm"
    move_group = moveit_commander.MoveGroupCommander(group_name)


    move_group.set_planning_time(10)
    move_group.set_end_effector_link("panda_hand")
    # Get the initial pose of the end effector
    start_pose = move_group.get_current_pose().pose

    # Initialize the transform listener
    listener = tf.TransformListener()

    # Initialize the gripper commander
    group_hand_name = "hand"
    gripper = moveit_commander.MoveGroupCommander(group_hand_name)

    # Initialize the gripper commander

    # Define the joint state to close the gripper
    gripper_joint_goal = [0.35, 0.35] 
    joint_home = [-0.0002249274015897828, -0.7846473935524318, 4.74312715691906e-06, -2.3559378868236878, -0.0007421279900396864, 1.571840799410771, 0.78462253368357]
    joints = []
    list_filled_event.wait()


    while not rospy.is_shutdown():
        for object in child_frame[:]:
            
            print("object", object)
            print("child frames", child_frame)
            i = 0
            move_group.set_start_state_to_current_state()
            start_pose = move_group.get_current_pose().pose

            listener.waitForTransform('panda_link0', 'panda_hand', rospy.Time(), rospy.Duration(3.0))

            (trans2, rot2) = listener.lookupTransform('panda_link0', 'panda_hand', rospy.Time(0))

            arm_pose = geometry_msgs.msg.Pose()
            arm_pose.position.x = trans2[0]
            arm_pose.position.y = trans2[1]
            arm_pose.position.z = (trans2[2])
            
            listener.clear()


            move_group.set_start_state_to_current_state()
            start_pose = move_group.get_current_pose().pose

            listener.waitForTransform('panda_link0', object,rospy.Time(), rospy.Duration(5.0))

            (trans, rot) = listener.lookupTransform('panda_link0', object, rospy.Time(0))
            print(f"rotation: {rot}, translation: {trans}, object: {object}")
            

            move_forward(rot, trans, arm_pose.position.z)

            listener.clear()

            move_group.set_start_state_to_current_state()
            start_pose = move_group.get_current_pose().pose
            

            listener.waitForTransform('panda_link0', object,rospy.Time(), rospy.Duration(5.0))

            (trans, rot) = listener.lookupTransform('panda_link0', object, rospy.Time(0))
            print(f"rotation: {rot}, translation: {trans}, object: {object}")


            move_up(rot, trans)

            listener.clear()
            move_group.set_start_state_to_current_state()
            start_pose = move_group.get_current_pose().pose


            listener.waitForTransform('panda_link0', object,rospy.Time(), rospy.Duration(5.0))

            (trans, rot) = listener.lookupTransform('panda_link0', object, rospy.Time(0))
            print(f"rotation: {rot}, translation: {trans}, object: {object}")


            move_down2(rot, trans)
            
            hand_close = [0.02, 0.02]
            gripper.set_joint_value_target([0.02, 0.02])
            plan = gripper.plan()
            plan_traj = plan[1]
            gripper.execute(plan_traj, wait=True)
            gripper.stop()
            rospy.sleep(1)
            


            # Load the data
            with open('paths_modified_4.json', 'r') as file:
                data = json.load(file)

            contexts_csv = '/home/parronj1/Rafael/local_detectron/contexts.csv'
            df = pd.read_csv(contexts_csv)
            desired_contexts = []
            desired_contexts.extend(df["Context"])

            # Prompt the user for tasks
            available_contexts = ["kitchen", "office", "child's_bedroom", "living_room", "bedroom", 
                                "dining_room", "pantry", "garden", "laundry_room"]

            prompt_message = ("Please input what contexts or multiple contexts separated by commas for the robot to focus on. "
                            f"These are the possible contexts: {', '.join(available_contexts)} "
                            "(or press Enter to continue without specifying tasks): ")

            while unprompted:
                user_input = input(prompt_message).strip()

                # Split the input by commas and strip whitespace
                robot_focus = [task.strip() for task in user_input.split(",")] if user_input else []

                # Check if all tasks are in available_contexts
                if all(task in available_contexts for task in robot_focus) or not robot_focus:

                    if robot_focus:
                        print(f"You have set the robot's focus on: {', '.join(robot_focus)}")
                    else:
                        print("There will be no focus.")
                    
                    unprompted = False
                    break
                else:
                    print("One or more of the contexts you entered are not valid. Please try again.")





            context, path, weight, degree_of_separation = get_object_context(data, object, desired_contexts, robot_focus)
            print(f"The most relevant context for {object} is {context}.")
            if context and not context.startswith("No paths found"):
                print(f"Path: {path}")
                # print(f"Weight: {weight:.2f}")
                # print(f"Degree of Separation: {degree_of_separation}")
            else:
                print("No relevant paths found.")

            
            context = context.strip().lower()
            filtered_rows = df[df["Context"] == context]
            

            if not filtered_rows.empty:
                matching_row = filtered_rows.iloc[0]
                row_values = matching_row.values[1:]
                print(row_values)
                joints.extend(row_values)

            

            print(joints)
            move_group.set_joint_value_target(joint_home)
            plan = move_group.plan()
            plan_traj = plan[1]
            move_group.execute(plan_traj, wait=True)
            move_group.stop()
            move_group.clear_pose_targets()


            move_group.set_joint_value_target(joints)
            plan = move_group.plan()
            plan_traj = plan[1]
            move_group.execute(plan_traj, wait=True)
            move_group.stop()
            move_group.clear_pose_targets()
            rospy.sleep(2)

            joints.clear()

            

            hand_open = [0.036, 0.036]
            gripper.set_joint_value_target([0.036, 0.036])
            plan = gripper.plan()
            plan_traj = plan[1]
            gripper.execute(plan_traj, wait=True)
            gripper.stop()
            rospy.sleep(2)

            move_group.set_joint_value_target(joint_home)
            plan = move_group.plan()
            plan_traj = plan[1]
            move_group.execute(plan_traj, wait=True)
            move_group.stop()
            move_group.clear_pose_targets()
            rospy.sleep(8)

            print("before pop", child_frame)

            child_frame.remove(object)
            listener.clear()
            print("after pop", child_frame)
            print("object after pop", object)
        if len(child_frame) == 0:
            print("nothing in child frame")
            exit()
            
    rospy.spin()

      
