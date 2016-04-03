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
		#French Notation lowercase
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

		# French Notation lower and uppercase
		'Do'  : 32.703 * (octave + 1),
                'Fo#' : 34.648 * (octave + 1),
                'Reb' : 34.648 * (octave + 1),
                'Re'  : 36.708 * (octave + 1),
                'Re#' : 38.891 * (octave + 1),
                'Mib' : 38.891 * (octave + 1),
                'Mi'  : 41.203 * (octave + 1),
                'Fa'  : 43.654 * (octave + 1),
                'Fa#' : 46.249 * (octave + 1),
                'Solb': 46.249 * (octave + 1),
                'Sol' : 48.999 * (octave + 1),
                'Sol#': 51.913 * (octave + 1),
                'Lab' : 51.913 * (octave + 1),
                'La'  : 55.000 * (octave + 1),
                'La#' : 58.270 * (octave + 1),
                'Sib' : 58.270 * (octave + 1),
                'Si'  : 61.735 * (octave + 1),

		# French notation uppercase
		'DO'  : 32.703 * (octave + 1),
                'DO#' : 34.648 * (octave + 1),
                'REb' : 34.648 * (octave + 1),
                'RE'  : 36.708 * (octave + 1),
                'RE#' : 38.891 * (octave + 1),
                'MIb' : 38.891 * (octave + 1),
                'MI'  : 41.203 * (octave + 1),
                'FA'  : 43.654 * (octave + 1),
                'FA#' : 46.249 * (octave + 1),
                'SOLb': 46.249 * (octave + 1),
                'SOL' : 48.999 * (octave + 1),
                'SOL#': 51.913 * (octave + 1),
                'LAb' : 51.913 * (octave + 1),
                'LA'  : 55.000 * (octave + 1),
                'LA#' : 58.270 * (octave + 1),
                'SIb' : 58.270 * (octave + 1),
                'SI'  : 61.735 * (octave + 1),
		
		#english notation
		'C'  : 32.703 * (octave + 1),
                'C#' : 34.648 * (octave + 1),
                'Db' : 34.648 * (octave + 1),
                'D'  : 36.708 * (octave + 1),
                'D#' : 38.891 * (octave + 1),
                'Db' : 38.891 * (octave + 1),
                'E'  : 41.203 * (octave + 1),
                'F'  : 43.654 * (octave + 1),
                'F#' : 46.249 * (octave + 1),
                'Gb': 46.249 * (octave + 1),
                'G' : 48.999 * (octave + 1),
                'G#': 51.913 * (octave + 1),
                'Ab' : 51.913 * (octave + 1),
                'A'  : 55.000 * (octave + 1),
                'A#' : 58.270 * (octave + 1),
                'Bb' : 58.270 * (octave + 1),
                'B'  : 61.735 * (octave + 1),
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
