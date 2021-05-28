#!/usr/bin/python

import rospy
from can_msgs.msg import Frame
import std_msgs

import numpy as np 
# from rospy.numpy_msg import 
import binascii

class can_com:

    def __init__(self):

        self.nameTopicSub = "/received_messages"
        self.nameTopicPub = "/sent_messages"

        self.tx_msg = []
        self.rx_msg = []

        # Subscriptor

        rospy.Subscriber(self.nameTopicSub, Frame, self.can_clbk, queue_size=50)
        # Publicador

        self.pub = rospy.Publisher(self.nameTopicPub, Frame,queue_size=50)

        # while not rospy.is_shutdown():
                    
        new_can_msg = Frame()
        new_can_msg.id = 1
        new_can_msg.dlc = 8

        # buf = np.array([0,0,0,0,0,0,0,0], dtype=np.uint8)
        buf = [0,0,0,0,0,0,0,0]
        # buf = "\0\0\0\0\0\0\0\0"
        buf[0] = 0xff
        buf[1] = 0xff
        buf[2] = 0xff
        buf[3] = 0xff
        buf[4] = 0xff
        buf[5] = 0xff
        buf[6] = 0xff
        buf[7] = 0xfc
        aux_buf = bytearray(buf)
        # aux_buf = np.array([0,0,0,0,0,0,0,0], dtype=np.uint8)
        # aux_buf = bytearray(buf)
        # for x in len(buf):
        #     aux_buf[x] = hex(buf[x])
        
        new_can_msg.data = aux_buf
        print(new_can_msg)
        self.pub.publish(new_can_msg)

    def can_clbk(self, received_messages):
        # rec_msg_int = list(map(int, (received_messages.data).split(" \ ")))
        
        # rec_msg_int = bytes(received_messages.data)
        # print(rec_msg_int)
        payload = bytearray(received_messages.data)
        pay_array=[x for x in payload]

        print([pay_array[2]])
        # print(binascii.hexlify(received_messages.data))
        # print(binascii.hexlify(payload))
        # print(type((binascii.s.data,','))))
        # print(type(received_messages.data))
        # self.pub.publish(new_can_msg)