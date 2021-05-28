#!/usr/bin/python

import rospy

from can_coms import can_com

if __name__ == '__main__':

    rospy.init_node('to_can_coms_node', anonymous=True)
    rospy.loginfo("Init node")

    can_com()
    
    rospy.spin()