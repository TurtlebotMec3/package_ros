#!/usr/bin/env python
import roslib
import rospy
import time
import kobuki_serial
from std_msgs.msg import String
#from std_msgs.msg import Int8
from sound_publisher.msg import Tones
from sound_publisher.msg import TonesArray
from sound_publisher.msg import MusicalTones
from sound_publisher.msg import MusicalTonesArray
from sound_publisher.msg import SongTitle

pub_frequency_tones = rospy.Publisher('sound/tones', TonesArray, queue_size = 1)
pub_musical_tones = rospy.Publisher('sound/musical_note', MusicalTonesArray, queue_size =1)

def callback(data):
	global pub_frequency_tones
	global pub_musical_tones

	# Def of the playing scores
	partition = TonesArray()		# scores in frequency
	music_score = MusicalTonesArray()	# score with real note (do, re, mi, fa, sol, la si)

	#we should choose the good topic to publish ;)

	if data.song == data.Star_Wars:
		partition.score=[Tones(880, 500),
				Tones(880, 500),
				Tones(880, 500),
				Tones(698.5, 376),
				Tones(1046.5, 200),
        			Tones(880, 500),
        			Tones(698.5, 376),
        			Tones(1046.5, 200),
        			Tones(880, 1000),
        			Tones(1318.5, 500),
        			Tones(1318.5, 500),
        			Tones(1318.5, 500),
        			Tones(1397, 376),
        			Tones(1046.5, 200),
        			Tones(831, 500),
				Tones(698.5, 376), 
				Tones(1046.5, 200),
				Tones(880, 1000)]
		
		pub_frequency_tones.publish(partition)

	elif data.song == data.Indiana_Jones:
		partition.score=[Tones(659,750),
			        Tones(698.5,250),
        			Tones(784,1000),
        			Tones(1046.5,2000),
			        Tones(587,750),
        			Tones(659,250),
        			Tones(698.5,2000),
        			Tones(784,750),
        			Tones(880,250),
        			Tones(988,1000),
        			Tones(1397,2000),
        			Tones(880,750),
        			Tones(988,250),
        			Tones(1046.5,1000),
        			Tones(1175,1000),
        			Tones(1318.5,1000),
        			Tones(659,750),
        			Tones(698.5,250),
        			Tones(784,1000),
        			Tones(1046.5,2000),
        			Tones(1175,750),
        			Tones(1318.5,250),
        			Tones(1397,3000)]

		pub_frequency_tones.publish(partition)

	elif data.song == data.Au_Clair_De_La_Lune:
		music_score.score=[MusicalTones('do', 5, 500),
				MusicalTones('do', 5, 500),
				MusicalTones('do', 5, 500),
				MusicalTones('re', 5, 500),
				MusicalTones('mi', 5, 1000),
				MusicalTones('re', 5, 1000),
				MusicalTones('do', 5, 500),
				MusicalTones('mi', 5, 500),
				MusicalTones('re', 5, 500),
				MusicalTones('re', 5, 500),
				MusicalTones('do', 5, 2000)]
		
		pub_musical_tones.publish(music_score)
	
	elif data.song == data.La_Marseillaise:
		music_score.score=[MusicalTones('sol',5, 500),
				MusicalTones('sol',5, 500),
				MusicalTones('la',5, 500),
				MusicalTones('la',5, 500),
				MusicalTones('re',6, 750),
				MusicalTones('si',5, 250),
				MusicalTones('sol',5, 250),
				MusicalTones('sol',5, 250),
				MusicalTones('si',5, 250),
				MusicalTones('sol',5, 250),
				MusicalTones('silence',5, 500),
				MusicalTones('do',6, 1000),
				MusicalTones('la',5, 250),
				MusicalTones('fa#',5, 250),
				MusicalTones('sol',5, 1500),
				MusicalTones('sol',5, 250),
				MusicalTones('la',5, 250),
				MusicalTones('si',5, 500),
				MusicalTones('si',5, 500),
				MusicalTones('si',5, 500),
				MusicalTones('do',6, 250),
				MusicalTones('si',5, 250),
				MusicalTones('si',5, 250),
				MusicalTones('la',5, 1000)]

		pub_musical_tones.publish(music_score)
 
						
	elif data.song == data.J1:
		music_score.score=[MusicalTones('sol',4,1000),
				MusicalTones('sol',4,1000),    
                                MusicalTones('mi',4,1000),
                                MusicalTones('mi',4,1000),
                                MusicalTones('sol',4,500),
                                MusicalTones('fa#',4,500),
                                MusicalTones('mi',4,500),
                                MusicalTones('si',4,500),
                                MusicalTones('do#',4,1000),
                                MusicalTones('do#',4,1000),
                                MusicalTones('sol',4,1000),
                                MusicalTones('sol',4,1000),
                                MusicalTones('fa#',4,1000),
                                MusicalTones('fa#',4,1000),
                                MusicalTones('si',4,500),
                                MusicalTones('sol',4,500),
                                MusicalTones('fa#',4,500),
                                MusicalTones('si',4,500),
                                MusicalTones('do',5,1000), 
                                MusicalTones('do',5,1000)]
		pub_musical_tones.publish(music_score)

	elif data.song == data.J2:
	
                music_score.score=[MusicalTones('re#',5,1000),  
                                MusicalTones('re',5,500),
                                MusicalTones('re#',5,500),
                                MusicalTones('la#',5,2000),
                                MusicalTones('re',5,1000),
                                MusicalTones('re#',5,500),
                                MusicalTones('fa',5,500),
                                MusicalTones('sol',5,2000),
                                MusicalTones('do',5,1500),
                                MusicalTones('do',5,500),
                                MusicalTones('sol',5,1000),
                                MusicalTones('fa',5,1000),
                                MusicalTones('fa',5,1000),
                                MusicalTones('fa#',5,1000),
                                MusicalTones('re',5,1000)]
		pub_musical_tones.publish(music_score)
	

	
def  main():
	rospy.Subscriber("sound/play_song", SongTitle, callback)
        rospy.spin()

#Main function
if __name__ == '__main__':
        #Initiate the node
        rospy.init_node('song_publisher', anonymous=True)
        main()
