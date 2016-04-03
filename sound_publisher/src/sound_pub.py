#!/usr/bin/env python
# -*- coding: utf-8 -*-

import roslib
import rospy
import time

from serial import Serial
from std_msgs.msg import String
from std_msgs.msg import Bool
from sound_publisher.msg import Tones 
from sound_publisher.msg import TonesArray

#dynamic_reconfigure :
from dynamic_reconfigure.server import Server
from sound_publisher.cfg import sound_publisherConfig

robot = Serial('/dev/kobuki', 115200)
waiting_time = 100.
a = 0.00000275


def reconfigure_callback(config, level):
	global waiting_time
	waiting_time = config.waiting_time
	print("Time between to tones is now : ", waiting_time)
	return config

# Function sending the sound command via uart
def send_command_robot(note, duration):
	global robot
	note_lsb = 0xff & note
	note_msb = 0xff & (note>>8)

	header = [0xAA, 0x55]
	payload = [0x05, 0x03, 0x03, note_lsb, note_msb, duration]
	
	# Checksum 
	checksum = 0
	for i in payload:
		checksum ^=i

	packet = header + payload + [checksum]
	robot.write(''.join(map(chr, packet)))
	

# conversion of the note to be understand by the robot
def note(f, t=500):
        global robot
        global a
	global waiting_time
        for i in range (0, t/100):
        	#robot.send([kobuki_serial.BuildRequestData.sound(int(1./(f*a)), 120)])
		send_command_robot(int(1./(f*a)), 120)
                time.sleep(0.1)
        rospy.sleep(waiting_time/500)


def callback_note_reception(data):
	for i in data.score:
		note(i.frequency, i.time)

def main():
	rospy.Subscriber("sound/tones", TonesArray , callback_note_reception)
	
	srv = Server(sound_publisherConfig, reconfigure_callback)
	rospy.spin()

#Main function
if __name__ == '__main__':
	#Initiate the node
	rospy.init_node('sound_pub', anonymous=True)
	main()
