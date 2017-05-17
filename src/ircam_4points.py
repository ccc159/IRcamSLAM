#!/usr/bin/env python

# -----Python Modules:
import serial
from time import sleep,time
import smbus


# -----ROS-related Modules:
import rospy
from std_msgs.msg import String


class pyIRcam:
	def __init__(self):
		self.sensorAddress = 0x58 
		self.device = smbus.SMBus(1)
		self.positions = {'found':False,'1':[0,0],'2':[0,0],'3':[0,0],'4':[0,0]}
		# Initialization of the IR sensor
		self.initCMDs = [0x30, 0x01, 0x30, 0x08, 0x06, 0x90, 0x08, 0xC0, 0x1A, 0x40, 0x33, 0x33]
		for i,j in zip(self.initCMDs[0::2], self.initCMDs[1::2]):
			self.device.write_byte_data(self.sensorAddress, i, j)
			sleep(0.01)

	def getPositions(self):
		self.device.write_byte(self.sensorAddress, 0x36)
		data = self.device.read_i2c_block_data(self.sensorAddress, 0x36, 16) # Read the data from the I2C bus
		x = [0x00]*4
		y = [0x00]*4
		i=0
		for j in xrange(1,11,3): # Decode the data coming from the I2C bus
			x[i]=data[j]+((data[j+2] & 0x30) << 4)
			y[i]=data[j+1]+((data[j+2] & 0xC0) << 2)
			i+=1
		i=0
		for j in ('1','2','3','4'): # Put the x and y positions into the dictionary
			self.positions[j][0]=x[i]
			self.positions[j][1]=y[i]
			i+=1
		if ( all(i == 1023 for i in x) and all(i == 1023 for i in y) ): # If all objects are 1023, then there is no IR object in front of the sensor
			self.positions['found'] = False
		else:
			self.positions['found'] = True

def runIrCamNode():
    # initilize the camera
    rospy.init_node('ircam_4points', anonymous = True)

    # publish the topic
    pub = rospy.Publisher('ircam_4points', String, queue_size = 10)
	
    rate = rospy.Rate(100)
    
    # Sensor initialization
    camera = pyIRcam()
    
    while not rospy.is_shutdown():
		# Update found IR objects
		camera.getPositions() 
		# If an IR object is found, print the information
		if camera.positions['found']: 
			s = ("%d, %d , %d, %d , %d, %d , %d, %d" % (camera.positions['1'][0],camera.positions['1'][1],camera.positions['2'][0],camera.positions['2'][1],camera.positions['3'][0],camera.positions['3'][1],camera.positions['4'][0],camera.positions['4'][1]) )
			rospy.loginfo (s)
			pub.publish(s)

			
		else:
			rospy.logwarn ("no points detected...")
			pub.publish("1023 , 1023 , 1023 , 1023 , 1023 , 1023 , 1023 , 1023")
    rate.sleep()
	
	
# eof

if __name__ == '__main__':
    try:
        runIrCamNode()
    except rospy.ROSInterruptException:
        com.close()
        rospy.loginfo("ROS Shutdown Request")
