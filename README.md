# package_ros
This repository contain the package ros we made for our turtlebot

sound_publisher : 

	This package allowed you to play custom sound with the kobuki base
	To use it you must launch roslaunch sound_publisher sound_publisher.launch

	/!\ Song must not be played while the robot is moving,
	Because the custom sound aren't in the kobuki driver, 
	We open a new serial connection if the base.
 	If two entity are talking at the same time, there'll have data collisions on the serial bus !!!!
	
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


camera_detection : 

	This package can be used by anyone of you having an Asus Xtion Pro Live and can be adapted to any other 3D camera with a few modifications.

	This package determines with the depth camera if there is an obstacle near the robot (on the right, in front of, on the left, on the left and on the right, or nothing)

	It would publish it on a topic /camera/obstacle_detection/postion

	You can choose to enable or disable the video treatment when you have no use for it by publishing True or False on the following topic : 
	/camera/obstacle_detection/enable

	to launch it : roslaunch camera_detection depth_analysis.launch


turtlebot_scenario : 

	This package contains the scenario our turtlebot is playing
	to launch it : roslaunch turtlebot_scenario turtlebot_scenario.launch 

	Please be noticed that you can not use this one directly on your turtlebot, we have plug an home maid electronic card on the pin DO1, DO2 and DO3 of the kobuki base.
	This card allowed us to generate two pwm. One to control a servo-motor to change the orientation of the camera, the other one to control some led, just to make our Turtlebot nice ;).

	You can obvisouly simulate it by using an arduino =).
