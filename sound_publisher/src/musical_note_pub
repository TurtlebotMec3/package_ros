#!/usr/bin/env python

import roslib
import rospy
import time
from std_msgs.msg import String
from sound_publisher.msg import MusicalTones
from sound_publisher.msg import MusicalTonesArray
from sound_publisher.msg import Tones
from sound_publisher.msg import TonesArray


pub = rospy.Publisher("sound/tones", TonesArray, queue_size = 1)

# conversion real notes to frequency 
# All notes need to be write in lowercase
def conversion_musical_note_to_frequency(note, octave):
	return {
		'do'  : 32.703 * (octave + 1),
		'do#' : 34.648 * (octave + 1),
		'reb' : 34.648 * (octave + 1),
		're'  : 36.708 * (octave + 1),
		're#' : 38.891 * (octave + 1),
		'mib' : 38.891 * (octave + 1),
		'mi'  : 41.203 * (octave + 1), 
		'fa'  : 43.654 * (octave + 1),
		'fa#' : 46.249 * (octave + 1),
		'solb': 46.249 * (octave + 1), 
		'sol' : 48.999 * (octave + 1),
		'sol#': 51.913 * (octave + 1),
		'lab' : 51.913 * (octave + 1),
		'la'  : 55.000 * (octave + 1),
		'la#' : 58.270 * (octave + 1),
		'sib' : 58.270 * (octave + 1),
		'si'  : 61.735 * (octave + 1),
		'silence' : 1. * (octave + 1),
	}.get(note, 1.)


# When someone publish on the topic
# We convert the data, then publish it on the frequency tones publisher
def callback(data):
	global pub
	partition = TonesArray()
	
	for i in data.score:
		partition.score.append(Tones(conversion_musical_note_to_frequency(i.tone, i.octave), i.time_base))
	
	pub.publish(partition)


def main():
	rospy.Subscriber("sound/musical_note", MusicalTonesArray, callback)
	rospy.spin()
	


#Main function
if __name__ == '__main__':
	rospy.init_node('musical_node_publisher', anonymous=True)
	main()
