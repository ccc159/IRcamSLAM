#!/usr/bin/env python

# -----ROS-related Modules:
from time import sleep,time
import rospy
from std_msgs.msg import String
from gpiozero import Buzzer

def buzzerNode():
    # initilize the magnet
    rospy.init_node('ircam_buzzer', anonymous = True)

    # subscribe to the change_magnet
    rospy.Subscriber('ircam_4points', String, callback)
    

    rospy.spin()
# eof
		
def callback(data):

    if data.data != "1023 , 1023 , 1023 , 1023 , 1023 , 1023 , 1023 , 1023":
        buzzer.beep()

        #rospy.loginfo("points detected: buzzer on")
    else:
        buzzer.beep()
        buzzer.beep()
        #rospy.loginfo("no points detected: buzzer off")

    return ""
# eof

if __name__ == '__main__':
    buzzer = Buzzer(17)
    try:
        buzzerNode()
    except rospy.ROSInterruptException:
        com.close()
        rospy.loginfo("ROS Shutdown Request")
