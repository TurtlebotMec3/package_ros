#!/usr/bin/env python

# Programm controlling the blue tube full of LED in the robot

import roslib
import rospy

from kobuki_msgs.msg import DigitalOutput

# Message to change the alimention mode of the Led
# mode = { ON, OFF, BLINK_SLOW, BLINK_FAST}
from turtlebot_scenario.msg import LedControl 



def change_mode(request):
	pub = rospy.Publisher('mobile_base/commands/digital_output', DigitalOutput, queue_size = 1)
	
	output = DigitalOutput()
	output.mask = [False, True, True, False]
	
	if (request.mode == request.OFF):
		output.values[1] = False
		output.values[2] = False
	elif (request.mode == request.BLINK_SLOW):
		output.values[1] = False
		output.values[2] = True
	elif (request.mode == request.BLINK_FAST):
		output.values[1] = True
		output.values[2] = False
	elif (request.mode == request.ALIVE):
		output.values[1] = True
		output.values[2] = True

	pub.publish(output)


def main():
	rospy.Subscriber('led/control_mode', LedControl, change_mode)
	rospy.spin()



# Main Function
if __name__ == '__main__':
	rospy.init_node('led_control', anonymous=True)
	main()
