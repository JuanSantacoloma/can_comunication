'''
Ben Katz
Motor Module Python API
Assumes the serial device is a nucleo running the firmware at:
Corresponding STM32F446 Firmware here:
https://os.mbed.com/users/benkatz/code/CanMaster/
'''
# import serial
from struct import *
import struct
import time
import os
import can
from datetime import datetime, timezone
class MotorModuleController():
    def __init__(self,id):
        try:
            self.gr = 9.0
            self.p_min =-12.5 # -95.5 @ -56.5
            self.p_max = 12.5 # 95.5 @ 56.5
            self.v_min = -65.0
            self.v_max = 65.0
            self.kp_min = 0.0
            self.kp_max = 50.0
            self.kd_min = 0.0
            self.kd_max = 5.0
            self.i_min = -2.7
            self.i_max = 2.7
            self.id=int(id)
            self.rx_values = []

            print(os.name)
            # os.system("sudo ifconfig can0 txqueuelen 1000")
            os.system('sudo ip link set can0 type can bitrate 1000')
            os.system('sudo ifconfig can0 up')
            self.can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan',is_extended_id=False)
            self.rx_msg = None
            print('connected to motor module controller')
        except:
            print('failed to connect to motor module controller')
            pass
    def send_data(self):
        pass
    def send_command_periodic(self, p_des, v_des, kp, kd, i_ff):
        """
        send_command(desired position, desired velocity, position gain, velocity gain, feed-forward current)
        Sends data over CAN, reads response, and populates rx_data with the response.
        """
        #     /// limit data to be within bounds ///
        p_des = self.fmin(self.fmaxf(self.p_min,p_des),self.p_max)
        v_des = self.fmin(self.fmaxf(self.v_min,v_des),self.v_max)
        kp = self.fmin(self.fmaxf(self.kp_min,kp),self.kp_max)
        kd = self.fmin(self.fmaxf(self.kd_min,kd),self.kd_max)
        t_ff = self.fmin(self.fmaxf(self.i_min,i_ff),self.i_max)
        #     /// pack ints into the can buffer ///
        p_int =int( self.float_to_uint(p_des,self.p_min,self.p_max,16) )
        v_int = int(self.float_to_uint(v_des,self.v_min,self.v_max,12))
        kp_int = int(self.float_to_uint(kp,self.kp_min,self.kp_max,12))
        kd_int = int(self.float_to_uint(kd,self.kd_min,self.kd_max,12))
        t_int = int(self.float_to_uint(t_ff,self.i_min,self.i_max,12))

        #  /// pack ints into the can buffer ///
        b=[]
        
        b.append(p_int>>8)                                     
        b.append(p_int&0xFF)
        b.append(v_int>>4)
        b.append(((v_int&0xF)<<4)|(kp_int>>8))
        b.append(kp_int&0xFF)
        b.append(kd_int>>4)
        b.append(((kd_int&0xF)<<4)|(t_int>>8))
        b.append(t_int&0xff)
        # print("datasend =",b)

        msg_volt = can.Message(arbitration_id=self.id,
                        data=b,is_extended_id=False)
        task = self.can0.send_periodic(msg_volt, 0.00001)
        assert isinstance(task, can.CyclicSendTaskABC)
        return task
        # msg = can.Message(arbitration_id=self.id, data=b, extended_id=False)
        # self.can0.send_periodic(msg,0.3)
        # print("Sending",msg, "to:",id)
        # print(msg)

    def enable_motor(self):
        """
        Puts motor with CAN ID "id" into torque-control mode.  2nd red LED will turn on
        """
        b = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFC'
        # id_b=bytes(bytearray([id]))
        msg_can = can.Message(arbitration_id=self.id, data=b, is_extended_id=False)
        self.can0.send(msg_can)
        print("Enable motor", self.id)

    def disable_motor(self):
        """
        Removes motor with CAN ID "id" from torque-control mode.  2nd red LED will turn off
        """
        b = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFD'
        # id_b=bytes(bytearray([id]))
        msg_can = can.Message(arbitration_id=self.id, data=b, is_extended_id=False)
        self.can0.send(msg_can)
        self.rx_msg = self.can0.recv(2.0)
        print("Disable motor:",self.id)

    def get_data(self):
        msg_recv = self.can0.recv(2.0)
        b_driver = msg_recv.data
        # print("b_driver",b_driver)
        id = b_driver[0]
        p_int_r = (b_driver[1]<<8)|b_driver[2]
        v_int_r = (b_driver[3]<<4)|(b_driver[4]>>4)
        t_int_r = ((b_driver[4]&0xF)<<8)|b_driver[5]
        self.rx_msg =[]
        self.rx_msg.append(msg_recv.timestamp)
        self.rx_msg.append(self.uint_to_float(p_int_r, self.p_min, self.p_max, 16))
        self.rx_msg.append(self.uint_to_float(v_int_r, self.v_min, self.v_max, 12))
        self.rx_msg.append(self.uint_to_float(t_int_r, self.i_min, self.i_max, 12))
        return self.rx_msg

    def send_command(self, p_des, v_des, kp, kd, i_ff):
        #     /// limit data to be within bounds ///
        p_des = self.fmin(self.fmaxf(self.p_min,p_des),self.p_max)
        v_des = self.fmin(self.fmaxf(self.v_min,v_des),self.v_max)
        kp = self.fmin(self.fmaxf(self.kp_min,kp),self.kp_max)
        kd = self.fmin(self.fmaxf(self.kd_min,kd),self.kd_max)
        t_ff = self.fmin(self.fmaxf(self.i_min,i_ff),self.i_max)
        #     /// pack ints into the can buffer ///
        p_int =int( self.float_to_uint(p_des,self.p_min,self.p_max,16) )
        v_int = int(self.float_to_uint(v_des,self.v_min,self.v_max,12))
        kp_int = int(self.float_to_uint(kp,self.kp_min,self.kp_max,12))
        kd_int = int(self.float_to_uint(kd,self.kd_min,self.kd_max,12))
        t_int = int(self.float_to_uint(t_ff,self.i_min,self.i_max,12))

        #  /// pack ints into the can buffer ///
        b=[]
        
        b.append(p_int>>8)                                     
        b.append(p_int&0xFF)
        b.append(v_int>>4)
        b.append(((v_int&0xF)<<4)|(kp_int>>8))
        b.append(kp_int&0xFF)
        b.append(kd_int>>4)
        b.append(((kd_int&0xF)<<4)|(t_int>>8))
        b.append(t_int&0xff)
        # print("datasend =",b)

        msg = can.Message(arbitration_id=self.id,
                        data=b,is_extended_id=False)
        self.can0.send(msg)
        return [p_des, v_des, kp, kd, t_ff]

    def float_to_uint(self,x, x_min, x_max, bits):
        # Converts a float to an unsigned int, given range and number of bits
        span = x_max - x_min
        offset = x_min
        return int ((x-offset)*(float(((1<<bits)-1))/span))

    def uint_to_float(self,x, x_min, x_max, bits):
        # Converts unsigned int to float, given range and number of bits
        span = x_max - x_min
        offset = x_min
        return ((float(x))*span/(float(((1<<bits)-1))) )+ offset

    def fmin(self,x,y):
        if x<y:
            return x
        else:
            return y
    def fmaxf(self,x,y):
        if x>y:
            return x
        else:
            return y

    def fminf3(self,x,y,z):
        numeros =[x,y,z]
        menor = numeros[0]
        for numero in numeros:
            if numero < menor:
                menor = numero
        return menor

    def fmaxf3(self,x,y,z):
        numeros =[x,y,z]
        menor = numeros[0]
        for numero in numeros:
            if numero > menor:
                menor = numero
        return menor