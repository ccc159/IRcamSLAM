from scipy.spatial import distance as dist
import numpy as np
import cv2
import transformation as tf
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Point

class Detection:
	def __init__(self,size):
		s = size/2
		self.objPts = np.array([([-s],[s],[0]),([s],[s],[0]),([s],[-s],[0]),([-s],[-s],[0])], dtype="double")
		self.distCoeffs = np.zeros((4, 1))  # no lens distortion
		self.cameraMatrix = np.array([[1369.41, 0, 512],[0, 1369.41, 384],[0, 0, 1]], dtype="double") # IR cam Camera Matrix, DO NOT CHANGE!
		self.rotationMatrix = np.array([(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)], dtype="double")
		self.translationVec = None
		self.transformationMatrix = np.zeros([4,4], dtype="double")
		self.transformationString = None
		self.poseStamped = PoseStamped()

	# order np points. don't have to understand...
	def orderPoints(self):
		xSorted = self.imgPts[np.argsort(self.imgPts[:, 0]), :]
		leftMost = xSorted[:2, :]
		rightMost = xSorted[2:, :]
		leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
		(tl, bl) = leftMost
		D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
		(br, tr) = rightMost[np.argsort(D)[::-1], :]
		self.imgPts = np.array([tl, tr, br, bl])
		return self

	# update the image points once receive new points
	def updateImgPts(self,arrPt):
		self.imgPts = np.array([(arrPt[0],arrPt[1]),
								(arrPt[2],arrPt[3]),
								(arrPt[4],arrPt[5]),
								(arrPt[6],arrPt[7])], dtype="double")
		return self

	def getTransformation(self):
		#perform solvePnP
		(success, rotVec, transVec) = cv2.solvePnP(self.objPts, self.imgPts, self.cameraMatrix,self.distCoeffs)

		#change rotation vector to rotation 3x3 matrix
		rotMatrix,jacobian = cv2.Rodrigues(rotVec)

		#pass rotation matrix and translation vec to detector
		self.rotationMatrix[:3, :3] = rotMatrix
		self.translationVec = transVec

		#combine 3x3 rotation matrix to 4x4 transformation matrix
		self.transformationMatrix[:3, :3] = rotMatrix

		#combine translation vector to 4x4 transformation matrix
		self.transformationMatrix[0,3],self.transformationMatrix[1,3],self.transformationMatrix[2,3] = transVec
		self.transformationMatrix[3, 3] = 1

		#convert matrix to string
		self.transformationString = ''
		for i in range(4):
			for j in range(4):
				self.transformationString += str(round(self.transformationMatrix[i,j],5)) + ','
		self.transformationString = self.transformationString[:-1]

		return self

	def getPoseStamped(self):
		# convert matrix to quaternion
		quaternion = tf.quaternion_from_matrix(self.rotationMatrix,True)
		self.poseStamped.header.frame_id = 'world'
		self.poseStamped.pose.position = Point(*self.translationVec)
		self.poseStamped.pose.orientation = Quaternion(*quaternion)

		return self



# detection = Detection(10)
# arrPt = [188,562,464,479,506,596,227,680]
# detection.updateImgPts(arrPt).orderPoints().getTransformation().getPoseStamped()
