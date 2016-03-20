#!/usr/bin/env python

import rospy

from dynamic_reconfigure.server import Server
from dynamic_tutorials.cfg import depth_analysis_config

def callback(config, level):
    rospy.loginfo("""Reconfigure Request: {double_param}""".format(**config))
    return config

if __name__ == "__main__":
    rospy.init_node("camera_detection", anonymous = True)

    srv = Server(depth_analysis_config, callback)
    rospy.spin()

