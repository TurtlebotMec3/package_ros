#!/usr/bin/env python

import rospy
import random
import math
from random import *

#mobile base commands
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist

# sound module
from sound_publisher.msg import Tones
from sound_publisher.msg import TonesArray
from sound_publisher.msg import MusicalTones
from sound_publisher.msg import MusicalTonesArray
from sound_publisher.msg import SongTitle
from kobuki_msgs.msg import Sound

#orientation camera
from turtlebot_scenario.msg import OrientationRequest

#bumper
from kobuki_msgs.msg import BumperEvent

#face recognition
#from facedetector.msg import Detection

#detection 3D
from camera_detection.msg import ObstacleDetection

# Global Variables
pub_motor = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=0)
pub_melody = rospy.Publisher('/mobile_base_commands/sound', Sound, queue_size = 0)
pub_Tones = rospy.Publisher('/sound/tones', TonesArray, queue_size = 1)
pub_MTones = rospy.Publisher('/sound/musical_note', MusicalTonesArray, queue_size =0)
pub_song = rospy.Publisher('/sound/play_song', SongTitle, queue_size = 0)
pub_servo = rospy.Publisher('/camera/orientation/request', OrientationRequest, queue_size = 0)
pub_enable_depth = rospy.Publisher('/camera/obstacle_detection/enable', Bool, queue_size=1, latch=True)
pub_enable_facedetection = rospy.Publisher('/facedetector/toggle', Bool, queue_size=1, latch=True)

melody = Sound()
command = Twist()
song = SongTitle()
bumper = BumperEvent()
dir3D = ObstacleDetection()

flag_detection = False

#define de directions
STRAIGHT=4
FRONT=3

# easily send command to the motor
def send_command_motor(linear = 0., angular = 0.):
	global pub_motor, command

	command.linear.x = linear
	command.linear.y = 0
	command.linear.z = 0
	command.angular.x = 0
	command.angular.y = 0
	command.angular.z = angular
	pub_motor.publish(command)
	rospy.sleep(0.5)


# randomly choose a sign
def sign():
	return choice([-1, 1])

# reaction to bumper hit
def callback_bumper(data):
	global bumper
	bumper = data	

#reaction to 3Dsensor
def callback_depth_analysis(data):
	global dir3D
	#global bumper
	dir3D=data
	#if bumper >= STRAIGHT :
        #	bumper.bumper = dir3D.position


#reaction to a face recognition
#def callback_face(face):
#	global pub_Tones, flag_detection

#	flag_detection = True
	#pub_Tones.publish([Tones(2000, 500)])
#	rospy.sleep(0.1)

def scenario():
	global melody, pub_melody
	global pub_Tones, pub_song, song
	global pub_servo
	global bumper
	global flag_detection
	global dir3D
	global pub_enable_depth, pub_enable_facedetection

	flag_detected=False
	signe=1

	
	if bumper.bumper == bumper.LEFT:
		print("bumper Gauche")
		send_command_motor(angular = -2.)
		bumper.bumper = STRAIGHT
	elif dir3D.position == dir3D.LEFT:
		print("Camera Gauche")
		send_command_motor(angular = -2.)
		dir3D.position = dir3D.NONE
	elif bumper.bumper == bumper.CENTER:
		print("bumper Centre")
		
		# Recule + levage camera
		flag_detection = False
			
		pub_enable_depth.publish(False)
		pub_enable_facedetection.publish(True)
		pub_servo.publish(True)
		send_command_motor(linear = -0.2)
		rospy.sleep(5)

		# People still standing
		while(flag_detection == True):
			flag_detection = False
			rospy.sleep(2.5)
			flag_detected = True
		
		pub_enable_facedetection.publish(False)
		pub_enable_depth.publish(True)

		signe=sign()
		send_command_motor(angular = signe*4)
		if(flag_detected==True):
			send_command_motor(angular = signe*4)
			send_command_motor(angular = signe*4)
			send_command_motor(angular = signe*4)
		else:
			send_command_motor(angular = -signe*4)
                        send_command_motor(angular = signe*2)


		
		rospy.sleep(1)
		
		# robot going away
		pub_servo.publish(False)
		signe=sign()
		send_command_motor(linear = -0.2, angular = signe *  3)
                send_command_motor(angular = signe*3)

		bumper.bumper = STRAIGHT
		
	elif dir3D.position == dir3D.CENTER:
		print("Camera centre")
		send_command_motor(linear = -0.2, angular = sign() * 3)
		dir3D.position = dir3D.NONE

	elif bumper.bumper == bumper.RIGHT :
		print("Bumper Droit")
		send_command_motor(angular = 2.)
		bumper.bumper = STRAIGHT

	elif dir3D.position == dir3D.RIGHT:
                print("Camera Droite")
                send_command_motor(angular = 2.)
                dir3D.position = dir3D.NONE

	elif dir3D.position == dir3D.FRONT:
		print("Camera Gauche et Droite")
		signe=sign()
		send_command_motor(angular = 4*signe)
		send_command_motor(angular = 4*signe)
		dir3D.position = dir3D.NONE
	else:
		send_command_motor(linear = 0.2)

	

def main():
	global bumper
	global pub_song, song
	global pub_enable_depth, pub_enable_facedetection

	
	# topic subscribed
	rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, callback_bumper)
#	rospy.Subscriber('/facedetector/faces', Detection, callback_face)
	rospy.Subscriber('/camera/obstacle_detection/position', ObstacleDetection, callback_depth_analysis)	

	# post traitment enable
	pub_enable_facedetection.publish(False)
	pub_enable_depth.publish(True)	

	rospy.sleep(10)
	print("let's go !")
	bumper.bumper = 4
	
	while not rospy.is_shutdown():
		
		#randomm direction changing
		duree = 3 + random()*5
		time_end = rospy.get_time() + duree
		
		while(rospy.get_time() < time_end):
			scenario()
		#	bumper.bumper = choice([bumper.LEFT, bumper.RIGHT, STRAIGHT,STRAIGHT,STRAIGHT,STRAIGHT,STRAIGHT])
	rospy.spin() 				

if __name__ == '__main__':
	rospy.init_node('scenario', anonymous=True)
	main()