#!/usr/bin/env python
import roslib
#load in all the paths to the packages listed in 'manifest.xml'
roslib.load_manifest('simple_controller')

#basic ros python commands:
import rospy

#import message types:
from pr2_controllers_msgs.msg import JointTrajectoryControllerState
from geometry_msgs.msg import Twist

from math import  *



#[sensor_msgs/LaserScan]:
#Header header
#  uint32 seq
#  time stamp
#  string frame_id
#float32 angle_min
#float32 angle_max
#float32 angle_increment
#float32 time_increment
#float32 scan_time
#float32 range_min
#float32 range_max
#float32[] ranges
#float32[] intensities

def myStateCallback(state):
    
    
    cmd = Twist()
    cmd.linear.x=-2.0*state.error.positions[2]
    cmd.linear.y=-2.0*state.error.positions[3]
    if(abs(cmd.linear.x) < .05):
	cmd.linear.x=0.0
    if(abs(cmd.linear.y) < .05):
        cmd.linear.y=0.0
    cmd.angular.z=4.0*state.error.positions[4]
    if(abs(cmd.angular.z) < .05):
        cmd.angular.z=0.0

    print cmd
    #regardless of whether we set things, publish the command:
    pub.publish(cmd)   




#this command registers this process with the ros master
rospy.init_node('my_controller')

#register a publisher, to topic '/base_controller/command', of type Twist
pub = rospy.Publisher('/base_controller/command', Twist)

#register a callback for messages of type LaserScan, on the topic "/base_scan"
sub = rospy.Subscriber("/r_arm_controller/state", JointTrajectoryControllerState, myStateCallback)

#this line is equivalent to: 
# while(everything is ok)
#   check for messages, call callbacks
#   sleep
rospy.spin()

#in this example, we are controlling the robot at ~40Hz, 
#which is the rate at which we are receiving laser data


