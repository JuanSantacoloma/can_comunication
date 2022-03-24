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
    def __init__(self):
        try:
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
    def send_command(self, id, p_des, v_des, kp, kd, i_ff):
        """
        send_command(desired position, desired velocity, position gain, velocity gain, feed-forward current)
        Sends data over CAN, reads response, and populates rx_data with the response.
        """
        # id = int(id)
        # t = [p_des, v_des, kp, kd, i_ff]
        # b=pack("f",t)
        b = pack("f", p_des) + pack("f", v_des) + pack("f", kp) + pack("f", kd) + pack("f", i_ff)
        msg = can.Message(arbitration_id=id, data=b, extended_id=False)
        self.can0.send(msg)

    def enable_motor(self, id):
        """
        Puts motor with CAN ID "id" into torque-control mode.  2nd red LED will turn on
        """
        b = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFC'
        # id_b=bytes(bytearray([id]))
        msg_can = can.Message(arbitration_id=id, data=b, extended_id=False)
        self.can0.send(msg_can)
        self.rx_msg = self.can0.recv(30.0)
        print("Enable motor", id)

    def disable_motor(self, id):
        """
        Puts motor with CAN ID "id" into torque-control mode.  2nd red LED will turn on
        """
        b = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFD'
        # id_b=bytes(bytearray([id]))
        msg_can = can.Message(arbitration_id=id, data=b, extended_id=False)
        self.can0.send(msg_can)
        self.rx_msg = self.can0.recv(30.0)
        print("Disable motor:",id)

    def get_data(self):
        data =0
        data = self.rx_msg

        return data
    # def enable_motor(self, id):
    #     """
    #     Puts motor with CAN ID "id" into torque-control mode.  2nd red LED will turn on
    #     """
    #     b = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFD'
    #     id_b=bytes(bytearray([id])
    #     #b = b + bytes(bytearray([id]))
    #     msg = can.Message(arbitration_id=id_b, data=b, extended_id=False)
    #     can0.send(msg)
    #     #time.sleep(.1)
    #     #self.ser.flushInput()

    # def disable_motor(self, id):
    #     """
    #     Removes motor with CAN ID "id" from torque-control mode.  2nd red LED will turn off
    #     """
    #     b = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFD'
    #     b = b + bytes(bytearray([id]))
    #     self.ser.write(b)
    # def zero_motor(self, id):
    #     pass