#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from scipy.spatial import distance as dist
import numpy as np
import cv2
import transformation as t



# 3D model points.
MODEL_POINTS = np.array([
	(0.0, 0.0, 0.0),
	(1.0, 0.0, 0.0),
	(1.0, 1.0, 0.0),
	(0.0, 1.0, 0.0),
])

# order np points. don't have to understand...
# input is np.array()
def order_points(pts):
	xSorted = pts[np.argsort(pts[:, 0]), :]
	leftMost = xSorted[:2, :]
	rightMost = xSorted[2:, :]
	leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
	(tl, bl) = leftMost
	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
	(br, tr) = rightMost[np.argsort(D)[::-1], :]
	return np.array([tl, tr, br, bl], dtype="float32")
# eof

def parseDatatoImagePoints(data):
	data = eval(data)
	image_points = np.array([
		(data[0], data[1]),
		(data[0], data[1]),
		(data[0], data[1]),
		(data[0], data[1]),
	], dtype="double")
	return image_points

def callback(msg):
	global pub

	# 2D image points
	image_Points = parseDatatoImagePoints(msg.data)
	image_Points = order_points(image_Points)

	test_image_points = parseDatatoImagePoints("0 , 0 , 0 , 1 , 1 , 1 , 1 , 0")
	#test_image_points = parseDatatoImagePoints("303 , 188 , 759 , 109 , 819 , 557 , 381 , 624")
	# 3D model points
	model_Points = MODEL_POINTS

	# alternative: cameraMatrix = np.eye(3)
	camera_Matrix = np.array([[1024, 0, 512],[0, 1024, 512],[0, 0, 1]], dtype="double")
	# Assuming no lens distortion
	dist_Coeffs = np.zeros((4, 1))

	(success, rotation_vector, translation_vector) = cv2.solvePnP(model_Points, test_image_points, camera_Matrix,
																  dist_Coeffs)

	rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

	print "Rotation Matrix:\n {0}".format(rotation_matrix)
	print "Translation Vector:\n {0}".format(translation_vector)

	pub.publish(str(translation_vector))


def main():
	global pub
	rospy.init_node('ircam_transformation', anonymous=True)

	rospy.Subscriber("/ircam_4points", String, callback)
	pub = rospy.Publisher("/ircam_transformation", String, queue_size=10)

	rospy.spin()


# eof


if __name__ == '__main__':
	pub = None
	main()
