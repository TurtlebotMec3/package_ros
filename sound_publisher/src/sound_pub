#!/usr/bin/env python
import roslib
import rospy
import time
import kobuki_serial
from std_msgs.msg import String
from sound_publisher.msg import Tones 
from sound_publisher.msg import TonesArray

robot = kobuki_serial.Kobuki('/dev/kobuki')
a = 0.00000275

def note(f, t=500):
        global robot
        global a
        for i in range (0, t/200):
                robot.send([kobuki_serial.BuildRequestData.sound(int(1./(f*a)), 120)])
                time.sleep(0.1)
        rospy.sleep(0.2)



def callback(data):
	for i in data.score:
		note(i.frequency, i.time)

def main():
	rospy.Subscriber("sound/tones", TonesArray , callback)
	rospy.spin()

#Main function
if __name__ == '__main__':
	#Initiate the node
	rospy.init_node('sound_pub', anonymous=True)
	main()
