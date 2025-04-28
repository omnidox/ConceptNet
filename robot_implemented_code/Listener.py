import rospy
from geometry_msgs.msg import Point, PointStamped
import tf
from visualization_msgs.msg import Marker

#position = rospy.Publisher('/object_position', PointStamped, queue_size=10)

def callback(msg):
    # Define the callback function to handle the incoming messages


    parent_frame = msg.header.frame_id
    child_frame = msg.text

    broadcaster = tf.TransformBroadcaster()

    rate = rospy.Rate(1)


    point = PointStamped()
    point.header.stamp = rospy.Time.now()
    point.header.frame_id = parent_frame
    point.point.x = msg.pose.position.x
    point.point.y = msg.pose.position.y
    point.point.z = msg.pose.position.z

    broadcaster.sendTransform((point.point.x, point.point.y, point.point.z),
                               (0.0, 0.0, 0.0, 1.0),
                               rospy.Time.now(),
                               child_frame,
                               parent_frame)






rospy.init_node('Rafael_node', anonymous=True)

# Create a subscriber object for the topic '/chatter'
rospy.Subscriber('/object', Marker, callback)


# Spin the node to receive the incoming messages
rospy.spin()