#!/usr/bin/python

import rospy
from can_msgs.msg import Frame
import std_msgs

# import numpy as np 
# from rospy.numpy_msg import 

class can_coms:

    def __init__(self):

        self.nameTopicSub = "/received_messages"
        self.nameTopicPub = "/sent_messages"

        self.tx_msg = []
        self.rx_msg = []

        # Subscriptor

        # rospy.Subscriber(self.nameTopicSub, can_msgs, self.can_clbk, queue_size=10)
        # Publicador

        self.pub = rospy.Publisher(self.nameTopicPub, Frame,queue_size=50)

        while not rospy.is_shutdown():
                
            new_can_msg = Frame()
            new_can_msg.id = 1
            new_can_msg.dlc = 8
            new_can_msg.data = [0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xfd]
            
            self.pub.publish(new_can_msg)

    # def can_clbk(self, can_msg):

    #     new_can_msg = can_msgs
    #     new_can_msg.
    #     new_can_msg.data = [0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xfd]
        
    #     self.pub.publish(new_can_msg)