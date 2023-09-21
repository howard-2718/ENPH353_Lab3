#! /usr/bin/env python3

"""
Constants.
"""
SCAN_ROW = 700
THRESHOLD = 200
CURVE = 5
FORWARD = 2.5

import rospy
from cv_bridge import CvBridge

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image

bridge = CvBridge()

rospy.init_node('track_following')
rospy.Subscriber('/robot/camera/image_raw', Image, process_image)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

"""
@brief Convert the image of the robot's sight to OpenCV format, then send a movement signal to follow the track.
@param data, which is a ROS image object.
@retval No return value, but sends a movement to the Publisher.
"""
def process_image(data):
    cv_image = bridge.imgmsg_to_cv2(data, desired_encoding='mono8')

    """
    Recycling last lab's code to detect where the track is.
    """
    analyze = cv_image[SCAN_ROW]

    on_road = False

    left_edge = 0
    right_edge = 0

    for i in range(len(analyze)):
        if analyze[i] < THRESHOLD and (on_road == False):
            left_edge = i
            on_road = True
        elif analyze[i] > THRESHOLD and (on_road == True):
            right_edge = i
            on_road = False

    center = round((left_edge + right_edge) / 2)

    move = Twist()

    """
    Very crude track following theory.
    """
    
    if center < 400:
        move.angular.z = CURVE
    elif center > 400:
        move.angular.z = -1 * CURVE
    else:
        move.angular.z = 0

    move.linear.x = FORWARD
    pub.publish(move)

rospy.spin()