#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from detector import Detection
from geometry_msgs.msg import PoseStamped


def callback(msg):
    global pubStr,pubPose,detection
    arrPt = eval(msg.data)
    if 1023 not in arrPt:
        detection.updateImgPts(arrPt).orderPoints().getTransformation().getPoseStamped()

    # print detection.transformationString
    pubStr.publish(detection.transformationString)
    pubPose.publish(detection.poseStamped)

def main(argv=None):
    global pubStr,pubPose
    rospy.init_node('ircam_transformation', anonymous=True)
    pubStr = rospy.Publisher("/ircam_transformation", String, queue_size=10)
    pubPose = rospy.Publisher("/ircam_poseStamped",PoseStamped,queue_size=10)
    rospy.Subscriber("/ircam_4points", String, callback)

    rospy.spin()



if __name__ == '__main__':
    pubStr,pubPose = None,None

    # define the marker size.
    detection = Detection(10)
    main()
