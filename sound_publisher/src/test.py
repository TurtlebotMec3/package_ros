#!/usr/bin/env python
import roslib
import rospy
import time
import kobuki_serial
from sound_publisher.msg import Tones
from sound_publisher.msg import TonesArray
from sound_publisher.msg import SongTitle

def main():
	pub = rospy.Publisher('sound/play_song', SongTitle, queue_size = 1)
	son = SongTitle() 
#	pub = rospy.Publisher('Sound/tones', TonesArray, queue_size=4)
#	partition = TonesArray() 
#	note0 = Tones(1000, 500)
#	note1 = Tones(2000, 500)
#	note2 = Tones(500, 2000)
#        rate = rospy.Rate(0.01)
	
	while not rospy.is_shutdown():
		son.song = son.Star_Wars
		#partition.score = [note0, note1, note2]
		#pub.publish(partition)
		pub.publish(son)
		rospy.sleep(10)
		son.song = son.Indiana_Jones
		pub.publish(son)
		rospy.sleep(10)
		rospy.spin()

#Main function
if __name__ == '__main__':
        #Initiate the node
        rospy.init_node('sound_test', anonymous=True)
        main()

