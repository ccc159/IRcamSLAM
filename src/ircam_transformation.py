#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from detector import Detection


def callback(msg):
    global pub,detection
    arrPt = eval(msg.data)
    detection.updateImgPts(arrPt).orderPoints().getTransformation()

    print detection.transformationString
    pub.publish(detection.transformationString)


def main(argv=None):
    global pub
    rospy.init_node('ircam_transformation', anonymous=True)
    rospy.Subscriber("/ircam_4points", String, callback)
    pub = rospy.Publisher("/ircam_transformation", String, queue_size=10)

    rospy.spin()



if __name__ == '__main__':
    pub = None
    detection = Detection(10)
    main()
