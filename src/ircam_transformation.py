#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from detector import Detection
from geometry_msgs.msg import PoseStamped


def callback(msg):
    global pubStr,pubPose,detection
    arrPt = eval(msg.data)
    detection.updateImgPts(arrPt).orderPoints().getTransformation().getPoseStamped()

    print detection.transformationString
    pubStr.publish(detection.transformationString)
    pubPose.publish(detection.poseStamped)

def main(argv=None):
    global pubStr,pubPose
    rospy.init_node('ircam_transformation', anonymous=True)
    rospy.Subscriber("/ircam_4points", String, callback)
    pubStr = rospy.Publisher("/ircam_transformation", String, queue_size=10)
    pubPose = rospy.Publisher("/ircam_PoseStamped",PoseStamped,queue_size=10)

    rospy.spin()



if __name__ == '__main__':
    pubStr,pubPose = None,None

    # define the marker size.
    detection = Detection(10)
    main()
