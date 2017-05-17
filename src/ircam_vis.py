#!/usr/bin/env python

# -----ROS-related Modules:
from time import sleep, time
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray
from visualization_msgs.msg import MarkerArray
from visualization_msgs.msg import Marker


def ircam_vis():
    global pub,pub_marker
    # initilize the magnet
    rospy.init_node('ircam_vis', anonymous=True)

    pub = rospy.Publisher('ircam_vis_poses', PoseArray, queue_size=10)
    pub_marker = rospy.Publisher('ircam_vis_markers', MarkerArray, queue_size=100)
    # subscribe to the change_magnet
    rospy.Subscriber('ircam_4points', String, callback)

    rospy.spin()
# eof

def makeMarkers(pose):
    marker = Marker()

    marker.type = Marker.SPHERE
    marker.pose = pose
    if pose.position.x == 1023 and pose.position.y == 1023:
        marker.color.r = 0
        marker.color.g = 0
        marker.color.b = 255
        marker.scale.x = 10
        marker.scale.y = 10
        marker.scale.z = 10
    else:
        marker.color.r = 255
        marker.color.g = 0
        marker.color.b = 0
        marker.scale.x = 20
        marker.scale.y = 20
        marker.scale.z = 20
    marker.color.a = 1.0

    marker.header.frame_id = 'ircam'
    return marker

def parseDatatoPose(data):
    data = eval(data)
    Poses = PoseArray()
    Markers = MarkerArray()
    Poses.header.frame_id = 'ircam'
    for i in range(0,7,2):
        p = Pose()
        p.position.x = data[i]
        p.position.y = data[i+1]
        p.position.z = 0
        Poses.poses.append(p)
        m = makeMarkers(p)
        m.ns = 'point:'+str(i/2+1)
        Markers.markers.append(m)

    return Poses,Markers


def callback(data):
    if data.data != "1023 , 1023 , 1023 , 1023 , 1023 , 1023 , 1023 , 1023":
        #rospy.loginfo("points detected")
        msg = parseDatatoPose(data.data)
        pub.publish(msg[0])
        pub_marker.publish(msg[1])

    #else:
    #rospy.loginfo("no points detected")
    return
# eof

if __name__ == '__main__':

    try:
        ircam_vis()
    except rospy.ROSInterruptException:
        com.close()
        rospy.loginfo("ROS Shutdown Request")
