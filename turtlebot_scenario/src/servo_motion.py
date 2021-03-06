#!/usr/bin/env python

# Program controlling the orientation of the camera
# publish the orientation and the command to the servo

import roslib
import rospy
from kobuki_msgs.msg import DigitalOutput
from turtlebot_scenario.msg import Orientation
from turtlebot_scenario.msg import OrientationRequest 

def callback(data):
	# topic 
	pub = rospy.Publisher('camera/orientation/value', Orientation, queue_size = 1, latch=True)
	command = rospy.Publisher('mobile_base/commands/digital_output', DigitalOutput, queue_size = 1, latch=True)
		
	# variable to publish
	digout = DigitalOutput()
	digout.mask = [True, False, False, False]
		
	angle = Orientation()

	if data.value == False:
		digout.values[0]=False
		angle.value = angle.low

	else:
		digout.values[0]=True
		angle.value = angle.up

	pub.publish(angle)
	command.publish(digout)
		


def main():
	rospy.Subscriber('camera/orientation/request', OrientationRequest, callback) 
	rospy.spin()

#Main function
if __name__ == '__main__':
	rospy.init_node('servo_motion', anonymous=True)
	main()
