#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import String




def GetpixelDist(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def GetRealDist(pixeld,defaultd):
    return float(pixeld)/defaultd*1

def GetAngle(p1,p2):
    return math.degrees(math.atan(math.fabs(float((p1[0]-p2[0])))/math.fabs((p1[1]-p2[1]))))

def callback(msg):
    global pubStr,pubPose,detection
    arrPt = eval(msg.data)[:2]
    if 1023 not in arrPt:
        pixelDist = GetpixelDist(arrPt[0], arrPt[1])
        realDist = GetRealDist(pixelDist, 500)
        angle = GetAngle(arrPt[0], arrPt[1])

    # print detection.transformationString
    pubStr.publish(realDist,angle)


def main(argv=None):
    global pubStr,pubPose
    rospy.init_node('ircam_2pointsdetect', anonymous=True)
    pubStr = rospy.Publisher("/ircam_2pointsdetect", String, queue_size=10)
    rospy.Subscriber("/ircam_4points", String, callback)

    rospy.spin()



if __name__ == '__main__':
    pubStr = None

    # define the marker size.
    main()
