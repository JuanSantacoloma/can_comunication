'''
Ben Katz
Motor Module Python API
Assumes the serial device is a nucleo running the firmware at:
Corresponding STM32F446 Firmware here:
https://os.mbed.com/users/benkatz/code/CanMaster/
'''
import serial
from struct import *
import time
import os
import can

class MotorModuleController():
    def __init__(self,id):
        try:
            self.p_min =-95.5
            self.p_max = 95.5
            self.v_min = -45.0
            self.v_max = 45.0
            self.kp_min = 0.0
            self.kp_max = 500.0
            self.kd_min = 0.0
            self.kd_max = 5.0
            self.i_min = -18.0
            self.i_max = 18.0
            self.id=int(id)
            print(os.name)
            os.system('sudo ip link set can0 type can bitrate 1000000')
            os.system('sudo ifconfig can0 up')
            self.can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes',fd=True)
            self.rx_msg = None
            print('connected to motor module controller')
        except:
            print('failed to connect to motor module controller')
            pass
    def send_data(self):
        pass
    def send_command(self, p_des, v_des, kp, kd, i_ff):
        """
        send_command(desired position, desired velocity, position gain, velocity gain, feed-forward current)
        Sends data over CAN, reads response, and populates rx_data with the response.
        """
        #     /// limit data to be within bounds ///
        p_des = self.fmin(self.fmaxf(self.p_min,p_des),self.p_max)
        v_des = self.fmin(self.fmaxf(self.v_min,v_des),self.v_max)
        kp = self.fmin(self.fmaxf(self.kp_min,kp),self.kp_max)
        kp = self.fmin(self.fmaxf(self.kd_min,kd),self.kd_max)
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
        print(b)
        # b=[0:7]
        # b[0]=p_des
        # =pack("e", ) + pack("e", v_des) + pack("e", kp) + pack("e", kd) + pack("e", i_ff)
        # m=b'b'
        msg_volt = can.Message(arbitration_id=self.id,
                        data=b,
                        extended_id=True)
        task = self.can0.send_periodic(msg_volt, 0.20)
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
        msg_can = can.Message(arbitration_id=self.id, data=b, extended_id=False)
        self.can0.send(msg_can)
        print("Enable motor", self.id)

    def disable_motor(self):
        """
        Removes motor with CAN ID "id" from torque-control mode.  2nd red LED will turn off
        """
        b = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFD'
        # id_b=bytes(bytearray([id]))
        msg_can = can.Message(arbitration_id=self.id, data=b, extended_id=False)
        self.can0.send(msg_can)
        self.rx_msg = self.can0.recv(30.0)
        print("Disable motor:",self.id)

    def get_data(self):
        self.rx_msg = self.can0.recv(30.0)
        return self.rx_msg

    def periodic_send(self,data):
        p_des = data[0]
        v_des = data[1]
        kp = data[2]
        kd = data[3]
        t_ff = data[4]
        #     /// limit data to be within bounds ///
        p_des = self.fmin(self.fmaxf(p_min,p_des),p_max)
        v_des = self.fmin(self.fmaxf(v_min,v_des),v_max)
        kp = self.fmin(self.fmaxf(kp_min,kp),kp_max)
        kp = self.fmin(self.fmaxf(kd_min,kd),kd_max)
        t_ff = self.fmin(self.fmaxf(i_min,t_ff),i_max)
        #     /// pack ints into the can buffer ///
        p_int =int( self.float_to_uint(p_des,p_min,p_max,16) )
        v_int = int(self.float_to_uint(v_des,v_min,v_max,12))
        kp_int = int(self.float_to_uint(kp,kp_min,kp_max,12))
        kd_int = int(self.float_to_uint(kd,kd_min,kd_max,12))
        t_int = int(self.float_to_uint(t_ff,i_min,i_max,12))

        #  /// pack ints into the can buffer ///
        b=[]

        b[0] = p_int>>8                                     
        b[1] = p_int&0xFF
        d[2] = v_int>>4
        d[3] = ((v_int&0xF)<<4)|(kp_int>>8)
        b[4] = kp_int&0xFF
        b[5] = kd_int>>4
        b[6] = ((kd_int&0xF)<<4)|(t_int>>8)
        b[7] = t_int&0xff

        msg_volt = can.Message(arbitration_id=self.id,
                        data=b,
                        extended_id=True)
        task = self.can0.send_periodic(msg, 0.20)
        assert isinstance(task, can.CyclicSendTaskABC)

        return task

    def float_to_uint(self,x, x_min, x_max, bits):
        # Converts a float to an unsigned int, given range and number of bits
        span = x_max - x_min
        offset = x_min
        return int ((x-offset)*(float(((1<<bits)-1))/span))

    def uint_to_float(self,x, x_min, x_max, bits):
        # Converts unsigned int to float, given range and number of bits
        span = x_max - x_min
        offset = x_min
        return (float(x_int))*span/(float(((1<<bits)-1))) + offset

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