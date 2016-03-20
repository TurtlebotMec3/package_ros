#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import random
import math
import time
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

# orientation camera
from turtlebot_scenario.msg import OrientationRequest

# bumper
from kobuki_msgs.msg import BumperEvent
from kobuki_msgs.msg import ButtonEvent

# face recognition
from facedetector.msg import Detection

# detection obstcale with depth camera
from camera_detection.msg import ObstacleDetection

from turtlebot_scenario.msg import LedControl


# Global Variables
pub_motor = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=0)
pub_melody = rospy.Publisher('/mobile_base_commands/sound', Sound, queue_size = 0)
pub_Tones = rospy.Publisher('/sound/tones', TonesArray, queue_size = 1)
pub_MTones = rospy.Publisher('/sound/musical_note', MusicalTonesArray, queue_size =0)
pub_song = rospy.Publisher('/sound/play_song', SongTitle, queue_size = 0)
pub_servo = rospy.Publisher('/camera/orientation/request', OrientationRequest, queue_size = 0)
pub_enable_depth = rospy.Publisher('/camera/obstacle_detection/enable', Bool, queue_size=0, latch=True)
pub_enable_facedetection = rospy.Publisher('/facedetector/toggle', Bool, queue_size=0, latch=True)
pub_light_mode = rospy.Publisher('/led/control_mode', LedControl, queue_size = 0, latch=True)


melody = Sound()
command = Twist()
song = SongTitle()
bumper = BumperEvent()
dir3D = ObstacleDetection()
light = LedControl()

flag_detection = False
activation_scenario = True


# hint action
actual_time = 0
past_time = 0
nb_hit = 0
flag_hint_action = False

#define de directions
STRAIGHT=4
FRONT=3

# easily send command to the motor
def send_command_motor(linear = 0., angular = 0.):
	global pub_motor, command
	global pub_sound_mutex

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

# Reaction to bumper hit
def callback_bumper(data):
	global bumper, FRONT, STRAIGHT
	global actual_time, past_time, nb_hit, flag_hint_action

	# We store the bumper to use it in the scenario
	if data.state == data.PRESSED:
		bumper = data

	# hint action : 
	actual_time = rospy.get_time()
	if data.bumper == bumper.CENTER and data.state == data.RELEASED:
		if actual_time - past_time > 5:
			past_time = actual_time
			nb_hit = 1
		else:
			nb_hit = nb_hit + 1

	if (nb_hit == 3):
		bumper.bumper =  STRAIGHT
		flag_hint_action = True
		nb_hit = 0
	 	

def callback_button(data):
	global activation_scenario
	global light, pub_light_mode
	global pub_enable_depth, pub_enable_facedetection

	# Button 1 change the actual light mode
	if data.button == data.Button0 and data.state == data.RELEASED:
		if light.mode == light.BLINK_SLOW:
			light.mode = light.OFF
		elif light.mode == light.OFF:
			light.mode = light.ALIVE
		elif light.mode == light.ALIVE:
			light.mode = light.BLINK_FAST
		elif light.mode == light.BLINK_FAST:
			light.mode = light.BLINK_SLOW
		pub_light_mode.publish(light)

	# button 2 enable and disable the scenario
	elif data.button == data.Button2 and data.state == data.RELEASED:
		if activation_scenario == True:
			activation_scenario = False
			light.mode = light.OFF
			pub_light_mode.publish(light)
			pub_enable_depth.publish(False)
		else: 
			activation_scenario = True 
			light.mode = light.BLINK_SLOW
			pub_light_mode.publish(light)
			pub_enable_depth.publish(True)


# Reaction to depth_analysis
def callback_depth_analysis(data):
	global dir3D
	dir3D=data


# Reaction to a face recognition
def callback_face(face):
	global flag_detection

	flag_detection = True

def scenario():
	global melody, pub_melody
	global pub_Tones, pub_song, song
	global pub_servo
	global bumper
	global flag_detection, activation_scenario
	global dir3D
	global pub_enable_depth, pub_enable_facedetection
	global pub_light_mode, light
	global flag_hint_action

	flag_detected=False
	signe=1

	if activation_scenario:
	
		if bumper.bumper == bumper.LEFT:
			print("bumper Gauche")
			send_command_motor(angular = -2.)
			rospy.sleep(0.5)
			bumper.bumper = STRAIGHT
		elif dir3D.position == dir3D.LEFT:
			print("Camera Gauche")
			send_command_motor(angular = -1.5)
			rospy.sleep(0.5)
			dir3D.position = dir3D.NONE
		elif bumper.bumper == bumper.CENTER:
			print("bumper Centre")
			
			# Recule + levage camera
			flag_detection = False
				
			pub_enable_depth.publish(False)
			pub_enable_facedetection.publish(True)
			pub_servo.publish(True)
			send_command_motor(linear = -0.2)
			
			# Wait 5 seconds to capture a face or until center buttons is pushed 3 times in 5 seconds
			delay = 0. 
			while (delay < 50 and flag_detection == False):
				rospy.sleep(0.1)
				delay = delay + 1

			# People still standing and we didn't push 3 times in 5 seconds the center button
			while(flag_detection == True and flag_hint_action == False):
				light.mode = light.BLINK_FAST
				pub_light_mode.publish(light)
				flag_detection = False
				rospy.sleep(2.5)
				flag_detected = True
			
			light.mode = light.BLINK_SLOW
			pub_light_mode.publish(light)
			pub_servo.publish(False)
			pub_enable_facedetection.publish(False)
			pub_enable_depth.publish(True)
	

			# If we didn't puch the center button 3 times in 5 seconds
			if (flag_hint_action == False):
				signe=sign()
				if(flag_detected == True):
					send_command_motor(angular = signe*3.8)
					send_command_motor(angular = signe*3.8)
					send_command_motor(angular = signe*3.8)
					send_command_motor(angular = signe*3.8)
				else :
					send_command_motor(angular = signe*3)
					rospy.sleep(0.5)
					send_command_motor(angular = -signe*2)
					rospy.sleep(0.1)
					send_command_motor(angular = - signe*2)
					#send_command_motor(angular = -signe*3.8)
					rospy.sleep(0.5)
					send_command_motor(angular = signe*2.)
		
				rospy.sleep(1)
		
				# robot going away
				signe=sign()
				send_command_motor(linear = -0.2, angular = signe *  3)
       	         		send_command_motor(angular = signe*3)
				
				rospy.sleep(0.5)
				bumper.bumper = STRAIGHT
	
		elif dir3D.position == dir3D.CENTER:
			print("Camera centre")
			send_command_motor(linear = -0.2, angular = sign() * 2.)
			rospy.sleep(0.5)
			dir3D.position = dir3D.NONE

		elif bumper.bumper == bumper.RIGHT :
			print("Bumper Droit")
			send_command_motor(angular = 2.)
			rospy.sleep(0.5)
			bumper.bumper = STRAIGHT

		elif dir3D.position == dir3D.RIGHT:
       	         	print("Camera Droite")
                	send_command_motor(angular = 1.5)
			rospy.sleep(0.5)
                	dir3D.position = dir3D.NONE

		elif dir3D.position == dir3D.FRONT:
			print("Camera Gauche et Droite")
			light.mode = light.BLINK_FAST
			pub_light_mode.publish(light)
			signe=sign()
			send_command_motor(angular = 2*signe)
			send_command_motor(angular = 2*signe)
			send_command_motor(angular = 2*signe)
			send_command_motor(angular = 2*signe)
			#send_command_motor(angular = 1.7*signe)
			dir3D.position = dir3D.NONE
			rospy.sleep(0.5)
			light.mode = light.BLINK_SLOW
			pub_light_mode.publish(light)
		else:
			send_command_motor(linear = 0.2)

def hint_action():
	global light, pub_light_mode
	global pub_song, song
	global flag_hint_action

	if flag_hint_action == True:
		light.mode = light.BLINK_FAST
		song.song = song.Indiana_Jones
	#	pub_song.publish(song)
		pub_light_mode.publish(light)
		time.sleep(15)
		light.mode = light.BLINK_SLOW
		pub_light_mode.publish(light)

		flag_hint_action = False


def main():
	global bumper, dir3D
	global pub_song, song
	global pub_enable_depth, pub_enable_facedetection
	global pub_light_mode, light

	
	# topic subscribed
	rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, callback_bumper)
	rospy.Subscriber('/facedetector/faces', Detection, callback_face)
	rospy.Subscriber('/camera/obstacle_detection/position', ObstacleDetection, callback_depth_analysis)	
	rospy.Subscriber('/mobile_base/events/button', ButtonEvent, callback_button)

	# post traitment enable

	rospy.sleep(5)
	pub_enable_facedetection.publish(False)
	pub_enable_depth.publish(True)

	song.song = song.Star_Wars
	pub_song.publish(song)
	light.mode = light.BLINK_FAST
	pub_light_mode.publish(light)


	rospy.sleep(10)
	print("let's go !")
	bumper.bumper = 4
	dir3D.position = dir3D.NONE
	light.mode = light.BLINK_SLOW
	pub_light_mode.publish(light)

	
	while not rospy.is_shutdown():
		
		#randomm direction changing
		duree = 10 + random()*5
		time_end = rospy.get_time() + duree
		
		while(rospy.get_time() < time_end):
			scenario()
			hint_action()
	#	bumper.bumper = choice([bumper.LEFT, bumper.RIGHT, STRAIGHT,STRAIGHT,STRAIGHT,STRAIGHT,STRAIGHT])

		#event()
	rospy.spin() 




if __name__ == '__main__':
	rospy.init_node('scenario', anonymous=True)
	main()
