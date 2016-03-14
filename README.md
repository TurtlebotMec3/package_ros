# package_ros
This repository contain the package ros we made for our turtlebot

sound_publisher : 

	This package allowed you to play custom sound with the kobuki base
	To use it you must launch roslaunch sound_publisher test.launch
	
	You'll find different mode :
		- you can play a tone by giving its frequency and the duration
		- you can also play a tone by giving its name, the octave and the duration (the names are as follow : do, do#, reb, re, re#, mib, mi, fa, fa#, solb, sol, sol#, lab, la, la#, sib, si)
		- And you can play predefined song

	- To use them you can publish an array with your frequency tones at
		/sound/tones
		The array is as follow TonesArray=[Tones(freq, duration), ...]
		You'll find the definitions in sound_publisher/msg/TonesArray.msg and soud_publisher/msg/Tones.msg

	- You can also publish an array with your musical tones at 
		/sound/musical_note
		The array is as follow : MusicalTonesArray=[MusicalTones(tone, octave, duration), ...]
		You'll find the definitions in sound_publisher/msg/MusicalTonesArray and sound_publisher/msg/MusicalTones

	- At last you can play a predifined song b publishing the number of the song at 
		/sound/play_song
		The definition of the song list is in sound_publisher/msg/SongTitle

		You can obsvioulsy add some. You must add them in the file sound_publisher/src/song_pub and in the msg definition sound_publisher/msd/SongTitle
		
		/!\ Don't forget to run catkin_make again after adding data to the msg file



turtlebot_scenario : 

	This package contains the scenario our turtlebot is playing
	to launch it : roslaunch turtlebot_scenario turtlebot_scenario.launch 
