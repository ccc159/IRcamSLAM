#!/usr/bin/env python

# -----Python Modules:
import serial
import time

# -----ROS-related Modules:
import rospy
from std_msgs.msg import String

# -----Initialze Serial
com = serial.Serial('/dev/ttyACM0', baudrate = 9600)



def callback(msg):

    if msg.data == 'bs':
        com.write('bs')
        result = com.readline()
        print(result)
    	ir_cam_out = rospy.Publisher('ir_cam_out', String, queue_size=10)    
        ir_cam_out.publish(result)
    else:
        print("wrong command : " + msg.data)

    return ""
# eof

def runIrCamNode():
    # initilize the magnet
    rospy.init_node('ir_cam')

    # subscribe to the change_magnet
    rospy.Subscriber('ir_cam_in', String, callback)

    rospy.spin()
# eof

if __name__ == '__main__':
    try:
        runIrCamNode()
    except rospy.ROSInterruptException:
        com.close()
        rospy.loginfo("ROS Shutdown Request")
