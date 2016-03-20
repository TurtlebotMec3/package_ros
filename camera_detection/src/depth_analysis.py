#!/usr/bin/env python

import roslib
import rospy
import cv2
import numpy as np

import dynamic_reconfigure.client

from std_msgs.msg import Bool

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from camera_detection.msg import ObstacleDetection

image=CvBridge()
pub = rospy.Publisher("/camera/obstacle_detection/position", ObstacleDetection, queue_size = 0)
activation_flag = False

def callback_enable(flag):
	global activation_flag
	activation_flag = flag.data

def callback(data):
	global image
	global pub
	global activation_flag

	if (activation_flag == True):
		position = ObstacleDetection()

		# dimension of the image received
		H = data.height
		W = data.width
	
		# conversion of the image to the right type
		# ie 16bit grayscale 
		image_temp = image.imgmsg_to_cv2(data, "16UC1")
		imageCV=np.array(image_temp, dtype=np.float32)
	
		# Normalisation of the image
		cv2.normalize(imageCV, imageCV, 0, 1, cv2.NORM_MINMAX)
	
		# On decoupe l'image en 3 zones
        	# On garde tout ce qui est a heuteur du robot
       		# on coupe les bords noirs et on enleve le sol  
    		# puis on decoupe une zone a gauche, une zone a droite et une zone au centre
		# On fait ensuite un masque pour connaitre les points < 30 cm du robot
        	mask_left=imageCV[H/2-10:H-25,10:10+W/4,0]<0.1
       		mask_center=imageCV[H/2-10:H-25,W/3:2*W/3,0]<0.1
      		mask_right=imageCV[H/2-10:H-25,3*W/4-20:W-20,0]<0.1

		# Then we calculate the average of the masks to know the percentage of the 
		# the zone  < 30 cm
		average_left = np.average(mask_left)
		average_center = np.average(mask_center)
		average_right = np.average(mask_right)

	#	print(average_left, average_center, average_right)

		# if 25 % of the zone is located at less than 30 cm of the robot
	
			# No possibility -> turn back
		if average_left > 0.25 and average_right > 0.25:
			position.position = position.FRONT
	
			# Priority to the CENTER detection
		elif average_center > 0.25:
			position.position = position.CENTER

		elif average_left > 0.25: 
			position.position = position.LEFT
		elif average_right > 0.25:
			position.position = position.RIGHT
		else:
			position.position = position.NONE

		#We publish the data
		pub.publish(position)


def main():
	# change depth resolution to QVGA
	client =  dynamic_reconfigure.client.Client("/camera/driver")
	client.update_configuration({"depth_mode":8, "data_skip":0})

	rospy.Subscriber("/camera/depth/image_rect", Image, callback)
	rospy.Subscriber("/camera/obstacle_detection/enable", Bool, callback_enable) 
	rospy.spin()


if __name__ == '__main__':
	rospy.init_node('obstacle_detection_analysis')
	main()

