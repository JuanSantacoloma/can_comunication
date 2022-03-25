
# b = [p_des,v_des,kp,kd,i_ff]
# t=bytearray(b)
# print(t)
import serial
import struct
import time
import os
import can

p_des=1
v_des=0
kp= 5
kd= 0
i_ff= 0
b = struct.pack("<e", p_des) + struct.pack("<e", v_des) + struct.pack("<e", kp) + struct.pack("<e", kd) + struct.pack("<e", i_ff)
# print(type(b))
rList = [1, 2, 3, 4, 5]

# arr = bytearray(b)
print(b)

# mmc.send_command(p_des , 0, 5, 0, 0)
# print(p_des)
while(p_des > .01):
    p_des = .9*p_des
    mmc.send_command(p_des , 0, 5, 0, 0)
    print(p_des)
    time.sleep(0.1)

mmc.disable_motor() # Disable motor with CAN ID 1